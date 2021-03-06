# -*- coding: utf-8 -*-
'''
Riak Salt Module
'''
from __future__ import absolute_import

# Import salt libs
import salt.utils


def __virtual__():
    '''
    Only available on systems with Riak installed.
    '''
    if salt.utils.which('riak'):
        return True
    return False


def __execute_cmd(name, cmd):
    '''
    Execute Riak commands
    '''
    return __salt__['cmd.run_all'](
        '{0} {1}'.format(salt.utils.which(name), cmd)
    )


def start():
    '''
    Start Riak

    CLI Example:

    .. code-block:: bash

        salt '*' riak.start
    '''
    ret = {'comment': '', 'success': False}

    cmd = __execute_cmd('riak', 'start')

    if cmd['retcode'] != 0:
        ret['comment'] = cmd['stderr']
    else:
        ret['comment'] = cmd['stdout']
        ret['success'] = True

    return ret


def stop():
    '''
    Stop Riak

    .. versionchanged:: Beryllium

    CLI Example:

    .. code-block:: bash

        salt '*' riak.stop
    '''
    ret = {'comment': '', 'success': False}

    cmd = __execute_cmd('riak', 'stop')

    if cmd['retcode'] != 0:
        ret['comment'] = cmd['stderr']
    else:
        ret['comment'] = cmd['stdout']
        ret['success'] = True

    return ret


def cluster_join(username, hostname):
    '''
    Join a Riak cluster

    .. versionchanged:: Beryllium

    CLI Example:

    .. code-block:: bash

        salt '*' riak.cluster_join <user> <host>

    username - The riak username to join the cluster
    hostname - The riak hostname you are connecting to
    '''
    ret = {'comment': '', 'success': False}

    cmd = __execute_cmd(
        'riak-admin', 'cluster join {0}@{1}'.format(username, hostname)
    )

    if cmd['retcode'] != 0:
        ret['comment'] = cmd['stdout']
    else:
        ret['comment'] = cmd['stdout']
        ret['success'] = True

    return ret


def cluster_leave(username, hostname):
    '''
    Leave a Riak cluster

    .. versionadded:: Beryllium

    CLI Example:

    .. code-block:: bash

        salt '*' riak.cluster_leave <username> <host>

    username - The riak username to join the cluster
    hostname - The riak hostname you are connecting to
    '''
    ret = {'comment': '', 'success': False}

    cmd = __execute_cmd(
        'riak-admin', 'cluster leave {0}@{1}'.format(username, hostname)
    )

    if cmd['retcode'] != 0:
        ret['comment'] = cmd['stdout']
    else:
        ret['comment'] = cmd['stdout']
        ret['success'] = True

    return ret


def cluster_plan():
    '''
    Review Cluster Plan

    .. versionchanged:: Beryllium

    CLI Example:

    .. code-block:: bash

        salt '*' riak.cluster_plan
    '''
    cmd = __execute_cmd('riak-admin', 'cluster plan')

    if cmd['retcode'] != 0:
        return False

    return True


def cluster_commit():
    '''
    Commit Cluster Changes

    .. versionchanged:: Beryllium

    CLI Example:

    .. code-block:: bash

        salt '*' riak.cluster_commit
    '''
    ret = {'comment': '', 'success': False}

    cmd = __execute_cmd('riak-admin', 'cluster commit')

    if cmd['retcode'] != 0:
        ret['comment'] = cmd['stdout']
    else:
        ret['comment'] = cmd['stdout']
        ret['success'] = True

    return ret


def member_status():
    '''
    Get cluster member status

    .. versionchanged:: Beryllium

    CLI Example:

    .. code-block:: bash

        salt '*' riak.member_status
    '''
    ret = {'membership': {},
           'summary': {'Valid': 0,
                       'Leaving': 0,
                       'Exiting': 0,
                       'Joining': 0,
                       'Down': 0,
                       }}

    out = __execute_cmd('riak-admin', 'member-status')['stdout'].splitlines()

    for line in out:
        if line.startswith(('=', '-', 'Status')):
            continue
        if '/' in line:
            # We're in the summary line
            for item in line.split('/'):
                key, val = item.split(':')
                ret['summary'][key.strip()] = val.strip()

        if len(line.split()) == 4:
            # We're on a node status line
            (status, ring, pending, node) = line.split()

            ret['membership'][node] = {
                'Status': status,
                'Ring': ring,
                'Pending': pending
            }

    return ret


def status():
    '''
    Current node status

    .. versionadded:: Beryllium

    CLI Example:

    .. code-block:: bash

        salt '*' riak.status
    '''
    ret = {}

    cmd = __execute_cmd('riak-admin', 'status')

    for i in cmd['stdout'].splitlines():
        if ':' in i:
            (name, val) = i.split(':', 1)
            ret[name.strip()] = val.strip()

    return ret
