#!/usr/bin/python3
from classes.node import node
import json
import os
consulBinary = "/home/khalefa/Github/InfraConsul/automation/binaries/consul"
vaultBinary = "/home/khalefa/Github/InfraConsul/automation/binaries/vault"

config = None
with open("nodes.config.json") as f:
    config = json.loads(f.read())

if config is None:
    print("kiss my ass")
    exit(1)

for datacenter in config:
    dc_name = datacenter['datacenter_name']
    dc_domain = datacenter['domain']
    dc_gosip_encryption_key = datacenter['gosip_encryption_key']
    totalConsul = len(datacenter['consul_server_nodes'])
    if totalConsul < 3:
        print("Invalid number of consul nodes, minimum 3, recommened 5")
        exit(1)
    consul_nodes = datacenter['consul_server_nodes']
    for n in consul_nodes:
        newNode = None
        if n['ssh_password']:
            newNode = node(n['ip_address'], n['ssh_port'],
                           n['ssh_username'], password=n['ssh_password'])
        elif n['ssh_keyfile']:
            newNode = node(n['ip_address'], n['ssh_port'],
                           n['ssh_username'], keyfile=n['ssh_keyfile'])
        if newNode:
            if newNode.Connect():
                n['node_client'] = newNode
                # print(n['node_client'])
                # print(newNode.ExecCommand("apt update", True))
                # exit(0)
    # Copy Consul Binary for each node
    for n in consul_nodes:
        node = n['node_client']
        'node type: node'
        if not os.path.exists(consulBinary):
            print("Cannot find consul binary")
        node.SendFile(consulBinary, "consul")
        print("Succesfully Copied Consul Binary to node:%s" % n['hostname'])
        node.ExecCommand("apt install -y unzip curl jq dnsutils uuid", True)
        node.ExecCommand("service consul stop", True)
        node.ExecCommand("rm -rf /opt/consul/*", True)
        node.ExecCommand("chmod a+x consul")
        node.ExecCommand("mv consul /usr/local/bin", True)
        node.ExecCommand("mkdir /etc/consul.d", True)
        node.ExecCommand("chmod a+w /etc/consul.d", True)
        node.ExecCommand(
            "useradd --system --home /etc/consul.d --shell /bin/false consul", True)
        node.ExecCommand(
            "chown --recursive consul:consul /etc/consul.d", True)
        node.ExecCommand(
            "consul -autocomplete-install", True)
        node.ExecCommand(
            "complete -C /usr/local/bin/consul consul", True)
