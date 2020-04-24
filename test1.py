# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------
@author  :30000367
@time    :2020/03/30
@file    :sdc_connect_by_ssh.py
@desc    :连接carrier客户端
@license :(c) Copyright 2020, SDC.
-----------------------------------------------------------------------
"""
import socket
import paramiko
import time


class SDCConnectException(Exception):
	pass


class SDCConnectBySSH:
	def __init__(self, host, username, pwd, port=22):
		self.host = host
		self.port = port
		self.username = username
		self.pwd = pwd
		self._transport = None

	def connect(self):
		try:
			transport = paramiko.Transport((self.host, self.port))
			transport.connect(username=self.username, password=self.pwd)
			self._transport = transport
		except paramiko.AuthenticationException:
			raise SDCConnectException("Authentication failed when connecting to " + self.host)
		except paramiko.ssh_exception.NoValidConnectionsError:
			raise SDCConnectException("please check ssh switch, Unable to connect to port 22 on " + self.host)
		except socket.error:
			raise SDCConnectException("SSHException please Check the net link to server " + self.host)

	def close(self):
		self._transport.close()

	def upload(self, local_path, target_path):
		# 连接，上传
		# file_name = self.create_file()
		sftp = paramiko.SFTPClient.from_transport(self._transport)
		# 将location.py 上传至服务器 /tmp/test.py
		sftp.put(local_path, target_path)

	def download(self, remote_path, local_path):
		sftp = paramiko.SFTPClient.from_transport(self._transport)
		sftp.get(remote_path, local_path)

	# 不能切换root
	def send_command(self, command):
		try:
			print('user exec command:{}'.format(command))
			_instance = paramiko.SSHClient()
			_instance._transport = self._transport

			# 执行命令
			stdin, stdout, stderr = _instance.exec_command(command)
			print(stdin, stdout, stderr)
			# 执行失败
			exit_status = stdout.channel.recv_exit_status()

			if exit_status != 0:
				stderr_result = stderr.readlines()
				return False, stderr_result
			# 获取命令结果
			stdout_result = stdout.readlines()
			return True, stdout_result
		except paramiko.SSHException:
			raise SDCConnectException('raise exec command')
	def send_command(self, command):
		try:
			print('user exec command:{}'.format(command))
			_instance = paramiko.SSHClient()
			_instance._transport = self._transport

			# 执行命令
			chanelSSHOb = _instance.invoke_shell(command)
			print(chanelSSHOb)
			# 执行失败
			exit_status = stdout.channel.recv_exit_status()

			if exit_status != 0:
				stderr_result = stderr.readlines()
				return False, stderr_result
			# 获取命令结果
			stdout_result = stdout.readlines()
			return True, stdout_result
		except paramiko.SSHException:
			raise SDCConnectException('raise exec command')


# 当SDCConnectBySSH无法满足基本需求时可调用该类，主要对SSH进行持久连接
# 交互式SSH 需切换root用户执行操作或涉及到root权限时使用
class InteractiveSSH(SDCConnectBySSH):
	def __init__(self, host, username, pwd, port=22):
		SDCConnectBySSH.__init__(self, host, username, pwd, port=22)
		self.rsp_list = []
		self.rsp_str = ''

	def connect(self):
		ssh = paramiko.SSHClient()
		ssh.load_system_host_keys()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		try:
			ssh.connect(self.host, self.port, username=self.username, password=self.pwd, timeout=60)  # timeout protection
			return ssh
		except:
			print('Warning:\nFist connect the ABC failed, now will retry!')
			ssh.connect(self.host, 22, username=self.username, password=self.pwd, timeout=60)  # timeout re-try
			print('Error:\nAttempt to connect ABC failed!!! Please check the IP / port/ account / password.')
		else:
			print('Info:\nConnect remote ABC success.')
	#
	# def chanel_exe_cmd(_transport, cmd, t=0.1):
	# 	ChanelSSHOb.send(cmd)
	# 	ChanelSSHOb.send("\n")
	# 	time.sleep(t)
	# 	resp = ChanelSSHOb.recv(9999).decode("utf8")
	# 	return resp
	#


if __name__ == "__main__":
	ssh = InteractiveSSH(host='3.5.23.50', port=22, username='admin', pwd='ChangeMe123');
	ssh.connect()
	# ssh = SDCConnectBySSH(host='3.5.23.50', port=22, username='admin', pwd='ChangeMe123')
	# ssh.connect()
	# print(ssh.send_command("su - root; HuaWei123;"))
	# print(ssh.send_command("pwd"))
	# print(ssh.send_command("ls /"))
	# ssh.send_command("pwd")
	# ssh.close()
