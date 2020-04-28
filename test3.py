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
		self.t = 0.1
		self.rsp_list = []
		self._transport = None
		self.lastingSSH = None
		self.retriesNum = 3		# 失败重试次数
		self.num = 0			# 次数

	def connect(self):
		try:
			transport = paramiko.Transport((self.host, self.port))
			transport.connect(username=self.username, password=self.pwd)
			# 20200426 添加，提供一个持久性的SSH连接实例
			self._transport = transport
			_instance = paramiko.SSHClient()
			_instance._transport = transport
			_instance.load_system_host_keys()
			_instance.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			self.lastingSSH = _instance.invoke_shell()
		except paramiko.AuthenticationException:
			if self.num < self.retriesNum:
				print("代码执行失败：第%s次重试" % self.num)
				with open(r'err.txt', 'a+') as f:
					f.write("%s 代码执行失败：第%d次重试\n" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),self.num))
				time.sleep(5)
				self.num += 1
				self.connect()
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

	# 单条命令切root用户操作 返回单个终端内容
	def send_command_lasting(self, command,t=0.1):
		try:
			# print("\n" * 2)
			# print('*********user exec command:{}'.format(command))
			# _instance = paramiko.SSHClient()
			# _instance._transport = self._transport
			# # 执行命令
			# chanelSSHOb = _instance.invoke_shell()
			#
			# self._transport = chanelSSHOb
			chanelSSHOb = self.lastingSSH
			self.t=t
			# print(chanelSSHOb)
			# print("\n"*2)
			chanelSSHOb.send(command)
			chanelSSHOb.send("\n")
			time.sleep(t)
			resp = chanelSSHOb.recv(9999).decode("utf8")
			return resp
		except paramiko.SSHException:
			raise SDCConnectException('raise exec command')

	# 切root用户进行进行批量liunx命令 返回终端内容列表 耗时命令得用单条命令
	def send_command_lasting_list(self, command):
		try:
			if not isinstance(command, (list,tuple)):
				raise TypeError
			self.send_command_lasting('y')
			rsp_end = None
			snap_bak = False		# 标记是否跳过循环
			password_sign = False		# 标记是否root密码错误
			for i in range(len(command)):
				if snap_bak:
					snap_bak = False
					continue
				if command[i].startswith('su'):
					if len(command) == i+1:
						raise SDCConnectException('没有输入密码')
					snap_bak = True
					self.rsp_list.append(self.send_command_lasting(command[i]))
					# print("正在执行%s命令\n"% command[i])
					# print(command[i+1])
					self.rsp_list.append(self.send_command_lasting(command[i+1], t=0.3))
					rsp_end = self.send_command_lasting("y")
					time_bak = 0.3
					if not rsp_end.endswith('root@Huawei:~# '):
						while time_bak < 1.5:
							if not rsp_end.endswith('root@Huawei:~# '):
								rsp_end = self.send_command_lasting("pwd", t=0.3)
								print("当前秒数%s,当前结果:\n%s\n"% (str(time_bak), rsp_end))
								password_sign = True
								time_bak += 0.3
							else:
								password_sign = False
								break
				else:
					rsp_end = self.send_command_lasting(command[i])
					self.rsp_list.append(rsp_end)

				if password_sign:
					raise SDCConnectException("password in error")
			print(self.rsp_list)
			return self.rsp_list
		except paramiko.SSHException:
			raise SDCConnectException('raise exec command')
		except TypeError:
			raise SDCConnectException('command type in (list,tuple)')
		except SDCConnectException:
			raise SDCConnectException('root and passwork err')

if __name__ == "__main__":
	# 初始化实例
	ssh = SDCConnectBySSH(host='3.4.10.105', port=22, username='admin', pwd='ChangeMe123');
	ssh.connect()
	# # ssh = SDCConnectBySSH(host='3.5.23.50', port=22, username='admin', pwd='ChangeMe123')
	# # ssh.connect()
	# # print(ssh.send_command("su - root; HuaWei123;"))
	# a = ssh.send_command_lasting("y")
	# print("输出结果XX\n",a)
	# # ssh.close()
	# a = ssh.send_command_lasting("pwd")
	# print("输出结果YY\n",a)
	# print('输出结果X1\n',ssh.send_command_lasting("su -"))
	# # print(ssh.send_command_lasting("pwd"))
	# # time.sleep(0.5)
	# # time.sleep(0.5)
	# a=ssh.send_command_lasting("HuaWei123",t=0.1) # 测试环境输密码命令得延迟0.6秒起码才能稳定获取结果字符串
	# print('输出密码结果X2\n',a)
	# a = ssh.send_command_lasting("y", t=0.2)  # 测试环境输密码命令得延迟0.6秒起码才能稳定获取结果字符串
	# print('输出密码结果X3\n', a)
	# a = ssh.send_command_lasting("pwd", t=0.2)  # 测试环境输密码命令得延迟0.6秒起码才能稳定获取结果字符串
	# print('输出密码结果X4\n', a)
	# a = ssh.send_command_lasting("pwd", t=0.2)  # 测试环境输密码命令得延迟0.6秒起码才能稳定获取结果字符串
	# print('输出密码结果X5\n', a)
	# a = ssh.send_command_lasting("pwd", t=0.2)  # 测试环境输密码命令得延迟0.6秒起码才能稳定获取结果字符串
	# print('输出密码结果X6\n', a)
	# print( not a.endswith('root@Huawei:~# '))
	# a=ssh.send_command_lasting("pwd",t=0.1)
	# print('输出结果X3\n',a)
	# a=ssh.send_command_lasting("pwd",t=30)
	# print('输出结果X4\n',a)
	# if chanel_exe_cmd(chanelSSHOb, sshCmd).endswith(u"Password: "):
	#     sshCmd = "HuaWei123"
	#     print(chanel_exe_cmd(chanelSSHOb, sshCmd))
	# print(ssh.send_command_lasting("pwd"))
	# print (ssh.send_command("pwd"))
	# print(ssh.send_command("ls /"))
	# ssh.send_command("pwd")
	# ssh.close()

	## 多条命令

	a = ssh.send_command_lasting_list(['su -', 'HuaWei123', 'cd /usr/log'])
	b = ssh.send_command_lasting("find -name '*.dbg.tgz'",t=1)
	print('函数出来的结果\n', a)
	print("函数出来的结果X2\n", b.)




	## 测试输密码延迟稳定性A

	# for j in range(100000):
	# 	print("第%s个循环"%str(j))
	# 	file = r'test.txt'
	# 	with open(file, 'a+') as f:
	# 		print("写入")
	# 		f.write("%s\t\t第%s个循环" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),str(j)))
	# 	for i in range(1000):
	# 		print('循环次数：',str(i))
	# 		ssh = SDCConnectBySSH(host='3.4.10.105', port=22, username='admin', pwd='ChangeMe123');
	# 		ssh.connect()
	# 		a = ssh.send_command_lasting("y")
	# 		# print("输出结果XX\n", a)
	# 		a = ssh.send_command_lasting("pwd")
	# 		# print("输出结果YY\n", a)
	# 		a = ssh.send_command_lasting("su ")
	# 		# print('输出结果X1\n', a)
	# 		a = ssh.send_command_lasting("HuaWei123", t=1)  # 测试环境输密码命令得延迟0.8秒起码才能稳定获取结果字符串
	# 		# a = ssh.send_command_lasting("pwd", t=0.1)
	# 		# print('输出密码结果X2\n', a)
	# 		# a = ssh.send_command_lasting("y", t=0.7)  # 测试环境输密码命令得延迟0.7秒起码才能稳定获取结果字符串
	# 		# print('输出密码结果X3\n', a)
	# 		if not a.endswith('root@Huawei:~# '):
	# 			print("延迟时间不稳定")
	# 			with open(file, 'a+') as f:
	# 				print("写入")
	# 				f.write("\t\t循环次数%s次报错\n"%(str(i)))
	# 			break
	# 		ssh.close()
	# 	## 测试输密码延迟稳定性A


