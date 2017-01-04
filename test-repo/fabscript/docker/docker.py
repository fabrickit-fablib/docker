# coding: utf-8

from fabkit import task
from fablib.docker import Docker


@task
def setup():
    docker = Docker()
    docker.setup()

    return {'status': 1}
