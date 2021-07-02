# -*- coding: utf-8 -*-
# @Time : 2021/4/29 10:37
# @Author : Joey

import subprocess
import os

from ..utils import sshoperation


def sub_command(command):
    print("执行命令：\n%s" % command)

    p = subprocess.Popen(command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
    stout = p.stdout.read()

    if len(stout) > 0:
        result = stout.strip().decode()
        print("返回结果：\n%s" % result)
        return result

    stderr = p.stderr.read()

    if len(stderr) > 0:
        err = stderr.strip().decode()
        print("报错信息：\n%s" % err)
        return err


def os_system(command):
    print("执行命令：\n%s" % command)
    os.system(command)


def ssh_cmd(host, port, username):
    ssh = sshoperation.SSHConnection(host=host, port=port, username=username)
    return ssh
