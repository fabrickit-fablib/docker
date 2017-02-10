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
        filer.template('/etc/sysconfig/docker', data=data)
        filer.template('/etc/sysconfig/docker-network', data=data)
        filer.template('/etc/sysconfig/docker-storage', data=data)
        filer.template('/usr/lib/systemd/system/docker.service', data=data)

        sudo('systemctl daemon-reload')

        self.start_services()
