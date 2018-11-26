#!/usr/bin/python3
from classes.node import node
import json
import os
consulBinary = "/home/khalefa/Github/InfraConsul/automation/binaries/consul"
vaultBinary = "/home/khalefa/Github/InfraConsul/automation/binaries/vault"

Create_Service_Command = """
cat << EOM | sudo tee /etc/systemd/system/consul.service
[Unit]
Description="HashiCorp Consul - A service mesh solution"
Documentation=https://www.consul.io/
Requires=network-online.target
After=network-online.target
ConditionFileNotEmpty=/etc/consul.d/consul.hcl

[Service]
User=consul
Group=consul
ExecStart=/usr/local/bin/consul agent -config-dir=/etc/consul.d/
ExecReload=/usr/local/bin/consul reload
KillMode=process
Restart=on-failure
LimitNOFILE=65536

[Install]
WantedBy=multi
"""


Create_Consul_Server_Config_File = """
cat << EOM | sudo tee /etc/consul.d/consul.hcl
datacenter = "@@@DATACENTER_NAME@@@"
data_dir = "/opt/consul"
encrypt = "@@@GOSIP_ENC_KEY@@@"
ui = @@@CONSUL_UI@@@
server = @@@IS_SERVER@@@
@@@BOOTSTRAP@@@
@@@PERFORMANCE@@@
@@@RECURSORS@@@
connect = {
  enabled = true
}
acl = {
  enabled = true
  default_policy = "deny"
  down_policy = "extend-cache"
  
}
retry_join = ["172.20.20.11","172.20.20.12","172.20.20.13","172.20.20.14","172.20.20.15"]
@@@LOG_LEVEL@@@
enable_syslog = true
bind_addr = "{{ GetInterfaceIP \\"@@@INTERFACE@@@\\" }}"
@@@PORTS_CONFIG@@@
EOM
"""

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
    totalConsul = len(datacenter['consul_nodes'])
    if totalConsul < 3:
        print("Invalid number of consul nodes, minimum 3, recommened 5")
        exit(1)
    consul_nodes = datacenter['consul_nodes']
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
        # we have to create a real config.hcl string now
        # make a copy of the original string
        config_hcl = str(Create_Consul_Server_Config_File)
        config_hcl = config_hcl.replace(
            "@@@DATACENTER_NAME@@@", dc_name)
        config_hcl = config_hcl.replace(
            "@@@GOSIP_ENC_KEY@@@", dc_gosip_encryption_key)
        if n['UI']:
            config_hcl = config_hcl.replace(
                "@@@CONSUL_UI@@@", "true")
        else:
            config_hcl = config_hcl.replace(
                "@@@CONSUL_UI@@@", "false")

        if n['Server']:
            config_hcl = config_hcl.replace(
                "@@@IS_SERVER@@@", "true")
            config_hcl = config_hcl.replace(
                "@@@BOOTSTRAP@@@", "bootstrap_expect = %d" % len(consul_nodes))
            config_hcl = config_hcl.replace(
                "@@@PERFORMANCE@@@", "performance {  raft_multiplier = 1 }")
            recurosrs_string = ""
            for rc in datacenter['datacenter_default_dns_resolvers']:
                recurosrs_string += '"' + rc + '"' + ", "
            recurosrs_string = recurosrs_string[:-2]
            config_hcl = config_hcl.replace(
                "@@@RECURSORS@@@", "recursors=[%s]" % recurosrs_string)
        else:
            config_hcl = config_hcl.replace(
                "@@@IS_SERVER@@@", "false")
            config_hcl = config_hcl.replace(
                "@@@BOOTSTRAP@@@", "")
            config_hcl = config_hcl.replace(
                "@@@PERFORMANCE@@@", "")
            config_hcl = config_hcl.replace(
                "@@@RECURSORS@@@", "")
        if n['LogLevel']:
            config_hcl = config_hcl.replace(
                "@@@LOG_LEVEL@@@", "log_level=\"%s\"" % n['LogLevel'])
        else:
            config_hcl = config_hcl.replace(
                "@@@LOG_LEVEL@@@", "")

        config_hcl = config_hcl.replace(
            "@@@INTERFACE@@@", n['ethernet_interface_name'])
        if n['DNS_PORT_53']:
            config_hcl = config_hcl.replace(
                "@@@PORTS_CONFIG@@@", "ports = { dns = 53 }")
        else:
            config_hcl = config_hcl.replace(
                "@@@PORTS_CONFIG@@@", "")
        # End OF Generating Config.hcl string
        # print(config_hcl)
        RequiresReboot = False
        node.SendFile(consulBinary, "consul")
        print("Succesfully Copied Consul Binary to node:%s" % n['hostname'])
        node.ExecCommand("apt install -y unzip curl jq dnsutils uuid", True)
        result = node.ExecCommand("hostname")
        if result['out'][0].strip() != n['hostname']:
            print("Original hostname is: %s, Wanted Hostname: %s, We have to change it" % (
                result['out'][0].strip(), n['hostname']))
            node.ExecCommand("hostnamectl set-hostname %s" %
                             n['hostname'], True)
            RequiresReboot = True
        node.ExecCommand("systemctl stop consul", True)
        node.ExecCommand("hostnamectl set-hostname", True)
        node.ExecCommand("mkdir --parents /opt/consul", True)
        node.ExecCommand("chown --recursive consul:consul /opt/consul", True)
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
        node.ExecCommand(config_hcl, True)
        node.ExecCommand(Create_Service_Command, True)
        if n['DNS_PORT_53']:
            node.ExecCommand("systemctl stop systemd-resolved", True)
            node.ExecCommand("systemctl disable systemd-resolved", True)
            node.ExecCommand(
                "setcap 'cap_net_bind_service=+ep' /usr/local/bin/consul", True)
            node.ExecCommand("systemctl disable systemd-resolved", True)
        else:
            node.ExecCommand("systemctl start systemd-resolved", True)
            node.ExecCommand("systemctl enable systemd-resolved", True)
        node.ExecCommand("systemctl enable consul", True)
        node.ExecCommand("systemctl daemon-reload", True)
        node.ExecCommand("systemctl stop consul", True)
        if RequiresReboot:
            print("Node %s going to reboot now" % n['hostname'])
            node.ExecCommand("reboot", True)
        else:
            node.ExecCommand("systemctl start consul", True)
