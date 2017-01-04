# coding: utf-8

from fabkit import *  # noqa
from fablib.base import SimpleBase


class Docker(SimpleBase):
    def __init__(self):
        self.data_key = 'docker'

        self.packages = {
            'CentOS .*': [
                'git',
                'vim',
                'wget',
                'docker-engine',
            ]
        }

        self.services = {
            'CentOS .*': [
                'docker'
            ]
        }

    def setup(self):
        data = self.init()

        sudo('setenforce 0')
        filer.Editor('/etc/selinux/config').s('SELINUX=enforcing', 'SELINUX=disable')
        Service('firewalld').stop().disable()

        filer.template('/etc/yum.repos.d/docker.repo', data=data)
        self.install_packages()
        self.start_services()
