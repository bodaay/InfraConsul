#!/usr/bin/python3
from classes.node import node
import json
import os
import time
import copy
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
@@@PRIMARY_DATACENTER_NAME@@@
acl = {
  enabled = true
  default_policy = "deny"
  down_policy = "extend-cache"

}
@@@RETRY_JOIN@@@
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


UpDateConfigFileWhenFinished = False

for datacenter in config:
    if datacenter['gosip_encryption_key'] == "":
        print("No Consul Gosip Key specified for datacenters %s, generating new one" %
              datacenter['datacenter_name'])
        datacenter['gosip_encryption_key'] = os.popen(
            consulBinary + " keygen").read().strip()
        UpDateConfigFileWhenFinished = True

# make a copy of the original config, we need this later for re-wrting nodes.config.json
# we have to do this now, before we start adding extra shit into original config variable

config_backUp = copy.deepcopy(config)


primaryDataCenterIsSet = False
primary_dc_name = ""
for datacenter in config:
    dc_name = datacenter['datacenter_name']
    print("Datancenter Named: %s will be assumed to be the master datacenter" % dc_name)
    if not primaryDataCenterIsSet:
        primary_dc_name = dc_name
        primaryDataCenterIsSet = True
    dc_domain = datacenter['domain']
    dc_gosip_encryption_key = datacenter['gosip_encryption_key']
    totalConsul = len(datacenter['consul_nodes'])
    if totalConsul < 3:
        print("Invalid number of consul nodes, minimum 3, recommened 5")
        exit(1)
    consul_nodes = datacenter['consul_nodes']
    # create retry join string array
    retry_join_string = ""
    for cn in consul_nodes:
        retry_join_string += '"' + cn['ip_address'] + '"' + ", "
    retry_join_string = retry_join_string[:-2]
    for n in consul_nodes:
        newNode = None
        if n['ssh_password']:
            newNode = node(n['ip_address'], n['ssh_port'],
                           n['ssh_username'], password=n['ssh_password'])
        elif n['ssh_keyfile']:
            newNode = node(n['ip_address'], n['ssh_port'],
                           n['ssh_username'], keyfile=n['ssh_keyfile'])
        print("Testing Connection Node: %s" % n['hostname'])
        if newNode:
            if newNode.Connect():
                n['node_client'] = newNode
                print('Stopping Consul Service on node: %s' % n['hostname'])
                newNode.ExecCommand("service consul stop", True)
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
            config_hcl = config_hcl.replace(
                "@@@RETRY_JOIN@@@", "retry_join=[%s]" % retry_join_string)
        else:
            config_hcl = config_hcl.replace(
                "@@@IS_SERVER@@@", "false")
            config_hcl = config_hcl.replace(
                "@@@BOOTSTRAP@@@", "")
            config_hcl = config_hcl.replace(
                "@@@PERFORMANCE@@@", "")
            config_hcl = config_hcl.replace(
                "@@@RECURSORS@@@", "")
            config_hcl = config_hcl.replace(
                "@@@RETRY_JOIN@@@", "")
        if n['LogLevel']:
            config_hcl = config_hcl.replace(
                "@@@LOG_LEVEL@@@", "log_level=\"%s\"" % n['LogLevel'])
        else:
            config_hcl = config_hcl.replace(
                "@@@LOG_LEVEL@@@", "")

        config_hcl = config_hcl.replace(
            "@@@PRIMARY_DATACENTER_NAME@@@", "primary_datacenter=\"%s\"" % primary_dc_name)
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
        print("Succesfully Coppied Consul Binary to node:%s " % n['hostname'])
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
            print(
                "DNS on port 53 for node \"%s\" selected, disabling systemd-resolved service" % n['hostname'])
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
        node.ExecCommand("service consul stop", True)
        if RequiresReboot:
            print("Node %s going to reboot now" % n['hostname'])
            node.ExecCommand("reboot", True)

    for n in consul_nodes:
        node = n['node_client']
        print('Starting Consul Service on node: %s' % n['hostname'])
        node.ExecCommand("service consul start", True)
    print("Sleeping for 5 seconds")
    time.sleep(5)
    print("running ACT bootstrap on first server node")
    for n in consul_nodes:
        if n['Server']:
            node = n['node_client']
            result = node.ExecCommand(
                "consul acl bootstrap | tee Master.Token")
            with open('Master.token', 'w') as the_file:
                the_file.writelines(result['out'])
                print("Saved Master.Token locally")
            print(''.join(result['out']))
            print("Saved on node: %s file Master.Token" % n['hostname'])
            break

if UpDateConfigFileWhenFinished:
    print("updating original nodes.config.json with updated configurations")
    with open('nodes.new.config.json', 'w') as the_file:
        the_file.write(json.dumps(config_backUp, indent=2))
