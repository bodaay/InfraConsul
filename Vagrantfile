# -*- mode: ruby -*-
# vi: set ft=ruby :

$script = <<SCRIPT
echo "Installing dependencies ..."
sudo apt-get update
sudo apt-get install -y unzip curl jq dnsutils
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
sudo chmod +x consul
sudo mv consul /usr/bin/consul
sudo mkdir /etc/consul.d
sudo chmod a+w /etc/consul.d
SCRIPT

# Specify a Consul version
CONSUL_DEMO_VERSION = ENV['CONSUL_DEMO_VERSION']

# Specify a custom Vagrant box for the demo
DEMO_BOX_NAME = "ubuntu/bionic64"

# Vagrantfile API/syntax version.
# NB: Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = DEMO_BOX_NAME
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "512"
    vb.cpus = "2"
  end
  config.vm.define "openvpn" do |openvpn|
    openvpn.vm.hostname = "openvpn"
    openvpn.vm.network "private_network", type: "dhcp"
    openvpn.vm.network "public_network"
  end
  config.vm.define "consul01" do |consul01|
    consul01.vm.hostname = "consul01"
    consul01.vm.network "private_network", type: "dhcp"
  end

  config.vm.define "consul02" do |consul02|
    consul02.vm.hostname = "consul02"
    consul02.vm.network "private_network", type: "dhcp"
  end
  
  config.vm.define "consul03" do |consul03|
    consul03.vm.hostname = "consul03"
    consul03.vm.network "private_network", type: "dhcp"
  end

  config.vm.define "consul04" do |consul04|
    consul04.vm.hostname = "consul04"
    consul04.vm.network "private_network", type: "dhcp"
  end
  config.vm.define "consul05" do |consul05|
    consul05.vm.hostname = "consul05"
    consul05.vm.network "private_network", type: "dhcp"
  end
  config.vm.define "vault01" do |vault01|
    vault01.vm.hostname = "vault01"
    vault01.vm.network "private_network", type: "dhcp"
  end
  config.vm.define "vault02" do |vault02|
    vault02.vm.hostname = "vault02"
    vault02.vm.network "private_network", type: "dhcp"
  end
  config.vm.define "vault03" do |vault03|
    vault03.vm.hostname = "vault03"
    vault03.vm.network "private_network", type: "dhcp"
  end
  config.vm.define "samba01" do |samba01|
    samba01.vm.hostname = "samba01"
    samba01.vm.network "private_network", type: "dhcp"
  end
  config.vm.define "samba02" do |samba02|
    samba02.vm.hostname = "samba02"
    samba02.vm.network "private_network", type: "dhcp"
  end
  config.vm.define "nginx01" do |nginx01|
    nginx01.vm.hostname = "nginx01"
    nginx01.vm.network "private_network", type: "dhcp"
  end
  config.vm.define "nginx02" do |nginx02|
    nginx02.vm.hostname = "nginx02"
    nginx02.vm.network "private_network", type: "dhcp"
  end
end
