import base64
import paramiko  # pip3 install paramiko
import os


class node:
    def __init__(self, hostname, port, username, password=None, keyfile=None):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.keyfile = keyfile
        self.__isconnected = False
        self.__sshclient = None
        self.__sftpclient = None
        self.__connectedUsingPassword = False

    def Connect(self):
        if not self.__isconnected:
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            if self.keyfile is not None:
                # we have to check if file exists
                if os.path.exists(self.keyfile):
                    client.connect(self.hostname, port=self.port,
                                   username=self.username, key_filename=self.keyfile)

                    self.__sshclient = client
                    self.__connectedUsingPassword = False
                    self.__isconnected = True
                    print("Connected Successfully to node: %s" % self.hostname)
                    return True
                else:
                    print("KeyFile Does Not exists %s" % self.keyfile)
                return False
            elif self.password is not None:
                client.connect(self.hostname, port=self.port,
                               username=self.username, password=self.password)
                self.__sshclient = client
                self.__connectedUsingPassword = True
                self.__isconnected = True
                print("Connected Successfully to node: %s" % self.hostname)
                return True
            return False

    def ExecCommand(self, command, RequiresRoot=False, timeout=10):
        if not self.__isconnected:
            if not self.Connect():
                return None
        if RequiresRoot:
            com = "sudo -S -p '' %s" % command
            stdin, stdout, stderr = self.__sshclient.exec_command(
                com, timeout=timeout)
            # if we are connected using password, we have to pass the password, other wise no need if connected using keyfile
            if self.__connectedUsingPassword:
                stdin.write(self.password + "\n")
                stdin.flush()
            return {'out': stdout.readlines(),
                    'err': stderr.readlines(),
                    'retval': stdout.channel.recv_exit_status()}
        else:
            stdin, stdout, stderr = self.__sshclient.exec_command(
                command, timeout=timeout)
            return {'out': stdout.readlines(),
                    'err': stderr.readlines(),
                    'retval': stdout.channel.recv_exit_status()}
        return None

    def SendFile(self, SourceFile, RemoteFile):
        if not self.__isconnected:
            if not self.Connect():
                return None
        if self.__sftpclient is None:
            self.__sftpclient = self.__sshclient.open_sftp()
        return self.__sftpclient.put(SourceFile, RemoteFile, confirm=True)

    def GetFile(self, RemoteFile, SourceFile):
        if not self.__isconnected:
            if not self.Connect():
                return None
        if self.__sftpclient is None:
            self.__sftpclient = self.__sshclient.open_sftp()
        return self.__sftpclient.get(RemoteFile, SourceFile)
