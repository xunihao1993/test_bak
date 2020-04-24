
import time,paramiko

def chanel_exe_cmd(ChanelSSHOb, cmd, t=0.1):
    ChanelSSHOb.send(cmd)
    ChanelSSHOb.send("\n")
    time.sleep(t)
    resp = ChanelSSHOb.recv(9999).decode("utf8")
    return resp


def creatSShConnectOb(ip_remote, port_remote, username, password):
    print('---------- start to create SSH object')
    print('Remote SSH Info:\n\'ip:%s  port:%d  username:%s  password:%s\'\n' % (
    ip_remote, port_remote, username, password))
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip_remote, port_remote, username=username, password=password, timeout=60)  # timeout protection
        return ssh
    except:
        print('Warning:\nFist connect the ABC failed, now will retry!')
        ssh.connect(ip_remote, port_remote, username=username, password=password, timeout=60)  # timeout re-try
        print('Error:\nAttempt to connect ABC failed!!! Please check the IP / port/ account / password.')
    else:
        print('Info:\nConnect remote ABC success.')


if __name__ == '__main__':
    ssh = creatSShConnectOb('3.5.23.50', 22, 'admin', 'ChangeMe123')
    chanelSSHOb = ssh.invoke_shell()  # 建立交互式的shell
    # stdin, stdout, stderr = ssh.exec_command('pwd')
    sshCmd = 'y'
    a=chanel_exe_cmd(chanelSSHOb, sshCmd)
    # print(stdout.read().decode('utf-8'))
    print('输出结果:',a)
    sshCmd='echo "a"'
    # .endswith(u'a ')
    a=chanel_exe_cmd(chanelSSHOb, sshCmd)
    print("输出结果\n",a.endswith(u'a\r\nadmin@Huawei:~$ '))
    print("输出结果\n", list(a))
    # print(type(a))
    #
    sshCmd = 'su'
    # .endswith(u"Password: ")
    print('输出结果\n',list(chanel_exe_cmd(chanelSSHOb, sshCmd)))
    # if chanel_exe_cmd(chanelSSHOb, sshCmd).endswith(u"Password: "):
    #     sshCmd = "HuaWei123"
    #     print(chanel_exe_cmd(chanelSSHOb, sshCmd))

    # sshCmd = 'whoami'
    # chanel_exe_cmd(chanelSSHOb, sshCmd)
    #
    # sshCmd = r'docker ps | grep mp'
    # chanel_exe_cmd(chanelSSHOb, sshCmd)
    #
    # sshCmd = 'rm -rf ' + ABC_admin_remoteDir + '*'
    # chanel_exe_cmd(chanelSSHOb, sshCmd)
