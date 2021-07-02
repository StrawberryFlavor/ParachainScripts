# -*- coding: utf-8 -*-
# @Time : 2021/4/29 10:21
# @Author : Joey

import paramiko
import os
import json


config_path = os.path.dirname(os.path.abspath('..')) + '/../config.json'
config = json.loads(open(config_path).read())


class SSHConnection(object):
    """
    由于环境上都是指定了私钥登陆，就在基础上写死了
    每次实例化都建立连接
    """

    def __init__(self, host, port, username):
        self._host = host
        self._port = port
        self._username = username
        self._transport = None
        self._sftp = None
        self._client = None
        keypath = config['private_key_path']
        self.privatepath = paramiko.RSAKey.from_private_key_file(keypath)
        self._connect()  # 建立连接

    def _connect(self):
        try:
            transport = paramiko.Transport((self._host, self._port))
            transport.connect(username=self._username, pkey=self.privatepath)
            sftp = paramiko.SFTPClient.from_transport(transport)

            self._sftp = sftp
            self._transport = transport
            print("SSH 连接到服务器：%s,端口为：%s,用户名为：%s" % (self._host, self._port, self._username))
        except Exception as e:
            print(e)

    # 下载文件
    def download_file(self, remote_path, local_path):
        try:
            if self._sftp is None:
                self._sftp = paramiko.SFTPClient.from_transport(self._transport)
            self._sftp.get(remote_path, local_path)
            print("已经将 %s 下载到 %s" % (remote_path, local_path))
        except Exception as e:
            print(e)

    # 下载文件夹
    def download_dir(self, remote_path, local_path):
        try:
            if self._sftp is None:
                self._sftp = paramiko.SFTPClient.from_transport(self._transport)

            try:
                os.mkdir(local_path)
            except:
                pass

            for item in self._sftp.listdir(remote_path):
                self._sftp.get((remote_path + "/" + item), local_path + "/" + item)
                print("%s 文件 已经从%s 已经下载到 %s " % (item, remote_path, local_path))
        except Exception as e:
            print(e)

    # 上传文件
    def put_file(self, local_path, remote_path):
        try:
            if self._sftp is None:
                self._sftp = paramiko.SFTPClient.from_transport(self._transport)
            self._sftp.put(local_path, remote_path)
            print("已经将 %s 上传到 %s" % (local_path, remote_path))
        except Exception as e:
            print(e)

    # 上传文件夹
    def put_dir(self, local_path, remote_path):
        try:
            if self._sftp is None:
                self._sftp = paramiko.SFTPClient.from_transport(self._transport)

            try:
                self._sftp.mkdir(remote_path)
            except:
                pass

            for item in os.listdir(local_path):
                self._sftp.put(local_path=local_path + "/" + item, remote_path=remote_path + "/" + item)
                print("%s 文件 已经从%s 已经上传到 %s " % (item, local_path, remote_path))
        except Exception as e:
            print(e)

    # 执行命令
    def exec_command(self, command):
        try:
            if self._client is None:
                self._client = paramiko.SSHClient()
                self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self._client._transport = self._transport
            stdin, stdout, stderr = self._client.exec_command(command)
            print("输入命令： %s" % command)
            data = stdout.read()
            if len(data) > 0:
                print("返回：\n%s" % data.strip().decode())  # 打印正确结果
                return data.strip().decode()
            err = stderr.read()
            if len(err) > 0:
                print("返回：\n%s" % err.strip().decode())  # 输出错误结果
                return err.strip().decode()
        except Exception as e:
            print(e)

    def close(self):
        if self._transport:
            self._transport.close()
            print("文件传输服务关闭")
        if self._client:
            self._client.close()
            print("SSH 命令服务关闭")


if __name__ == "__main__":
    ssh = SSHConnection(host="81.68.196.106", port=22, username="root")
    resp = ssh.exec_command("pwd")
