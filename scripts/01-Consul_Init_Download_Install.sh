#!/bin/bash
# you can always generate new key if you want using: consul keygen
ENCRYPTION_KEY="9hQ23lBrz96EAlbeddSsUQ=="
NETWORK_INTERFACE="enp0s8"
# MASTER_TOKEN_NAME="khalefa"
sudo apt-get update
sudo apt-get install -y unzip curl jq dnsutils uuid
echo "Determining Consul version to install ..."
CHECKPOINT_URL="https://checkpoint-api.hashicorp.com/v1/check"
if [ -z "$CONSUL_DEMO_VERSION" ]; then
    CONSUL_DEMO_VERSION=$(curl -s "${CHECKPOINT_URL}"/consul | jq .current_version | tr -d '"')
fi
echo "Fetching Consul version ${CONSUL_DEMO_VERSION} ..."
cd /tmp/
curl -s https://releases.hashicorp.com/consul/${CONSUL_DEMO_VERSION}/consul_${CONSUL_DEMO_VERSION}_linux_amd64.zip -o consul.zip
echo "Installing Consul version ${CONSUL_DEMO_VERSION} ..."
unzip consul.zip
# now we can just do same whether we have downloaded the file or copied it, just make sure the binary name same as "consul"
sudo chmod +x consul
sudo mv consul /usr/local/bin/consul
sudo mkdir /etc/consul.d
sudo chmod a+w /etc/consul.d
sudo useradd --system --home /etc/consul.d --shell /bin/false consul
sudo chown --recursive consul:consul /etc/consul.d
consul -autocomplete-install
complete -C /usr/local/bin/consul consul
sudo mkdir --parents /opt/consul
sudo chown --recursive consul:consul /opt/consul
echo "Creating Consul Service File..."
sudo systemctl stop consul
echo "Sleeping for 5 seconds"
sleep 5
# Deleting Old data folder
echo "Deleting old data folder files"
sudo rm -rf /opt/consul/*
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
WantedBy=multi-user.target 
EOM
cat << EOM | sudo tee /etc/consul.d/consul.hcl
datacenter = "dc1"
data_dir = "/opt/consul"
encrypt = "$ENCRYPTION_KEY"
server = true
ui = true
bootstrap_expect = 5
performance {
  raft_multiplier = 1
}
connect = {
  enabled = true
}
acl = {
  enabled = true
  default_policy = "deny"
  down_policy = "extend-cache"
  
}
enable_syslog = true
bind_addr = "{{ GetInterfaceIP \"$NETWORK_INTERFACE\" }}"
retry_join = ["172.20.20.11","172.20.20.12","172.20.20.13","172.20.20.14","172.20.20.15"]
EOM
sudo systemctl enable consul
sudo systemctl daemon-reload
sudo systemctl stop consul

sudo systemctl stop start