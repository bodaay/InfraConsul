#!/usr/bin/python3
import base64
import paramiko  # pip3 install paramiko
import inquirer  # pip3 install inquirer
import os

consulBinary = "./binaries/consul"
vaultBinary = "./binaries/vault"

questions = [
    inquirer.Text('hostname', message="Hostname or ip: "),
    inquirer.Text('port', message="Port: ", default='22'),
    inquirer.Checkbox('software', message="Software To Install?",
                      choices=['consul', 'vault', 'ass'], default='consul'),
    inquirer.Text('username', message="Username: "),
    inquirer.List('authMethod', message="Authentication Method?",
                  choices=['password', 'key', 'Key-FilePath'], default='password')
]


def GetSSHClient(hostname, port, username, authMethod, password="", key="", keyfile=""):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    if authMethod == 'password':
        client.connect(hostname, port=port,
                       username=username, password=password)
    elif authMethod == 'key':
        client.connect(hostname, port=port,
                       username=username, pkey=key)
    elif authMethod == 'Key-FilePath':
        client.connect(hostname, port=port,
                       username=username, key_filename=keyfile)

    return client


answers = inquirer.prompt(questions)
subanswers = ""

client = None
if answers['authMethod'] == 'password':
    subanswers = inquirer.prompt(
        [inquirer.Password('password', message="Password: ")])
    client = GetSSHClient(answers['hostname'],
                          answers['port'], answers['username'], answers['authMethod'], password=subanswers['password'])
elif answers['authMethod'] == 'key':
    subanswers = inquirer.prompt([inquirer.Text('key', message="Key: ")])
    client = GetSSHClient(answers['hostname'],
                          answers['port'], answers['username'], answers['authMethod'], key=subanswers['key'])
elif answers['authMethod'] == 'Key-FilePath':
    subanswers = inquirer.prompt([inquirer.Path(
        'keyfile', message="Key file path: ", path_type=inquirer.Path.FILE)])
    client = GetSSHClient(answers['hostname'],
                          answers['port'], answers['username'], answers['authMethod'], keyfile=subanswers['keyfile'])

if client:
    sftp = client.open_sftp()
    print(sftp.put(consulBinary, "consulBinary", confirm=True))
    stdin, stdout, stderr = client.exec_command("sudo apt update")
    print(stdout.read())
