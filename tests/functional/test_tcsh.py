import pytest
from tests.functional.plots import with_confirmation, without_confirmation, \
    refuse_with_confirmation, select_command_with_arrows

containers = (('thefuck/ubuntu-python3-tcsh',
               u'''FROM ubuntu:latest
                   RUN apt-get update
                   RUN apt-get install -yy python3 python3-pip python3-dev git
                   RUN pip3 install -U setuptools
                   RUN ln -s /usr/bin/pip3 /usr/bin/pip
                   RUN apt-get install -yy tcsh''',
               u'tcsh'),
              ('thefuck/ubuntu-python2-tcsh',
               u'''FROM ubuntu:latest
                   RUN apt-get update
                   RUN apt-get install -yy python python-pip python-dev git
                   RUN pip2 install -U pip setuptools
                   RUN apt-get install -yy tcsh''',
               u'tcsh'))


@pytest.fixture(params=containers)
def proc(request, spawnu, run_without_docker):
    proc = spawnu(*request.param)
    if not run_without_docker:
        proc.sendline(u'pip install /src')
    proc.sendline(u'tcsh')
    proc.sendline(u'eval `thefuck --alias`')
    return proc


@pytest.mark.functional
@pytest.mark.once_without_docker
def test_with_confirmation(proc, TIMEOUT):
    with_confirmation(proc, TIMEOUT)


@pytest.mark.functional
@pytest.mark.once_without_docker
def test_select_command_with_arrows(proc, TIMEOUT):
    select_command_with_arrows(proc, TIMEOUT)


@pytest.mark.functional
@pytest.mark.once_without_docker
def test_refuse_with_confirmation(proc, TIMEOUT):
    refuse_with_confirmation(proc, TIMEOUT)


@pytest.mark.functional
@pytest.mark.once_without_docker
def test_without_confirmation(proc, TIMEOUT):
    without_confirmation(proc, TIMEOUT)

# TODO: ensure that history changes.
