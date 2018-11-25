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

  config.vm.define "consul01" do |consul01|
    consul01.vm.hostname = "consul01"
    # Forward Consul web and api port 8500
    consul01.vm.network "forwarded_port", guest: 8500, host: 8511
      # n1.ssh.username = "root"
      # n1.ssh.password = "P@ssw0rd"
      # n1.ssh.keys_only = false
    #   n1.vm.provision "shell", inline: $script, env: {'CONSUL_DEMO_VERSION' => CONSUL_DEMO_VERSION}
    consul01.vm.network "private_network", ip: "172.20.20.11"
  end

  config.vm.define "consul02" do |consul02|
    consul02.vm.hostname = "consul02"
    # Forward Consul web and api port 8500
    consul02.vm.network "forwarded_port", guest: 8500, host: 8512
      # n2.ssh.username = "root"
      # n2.ssh.password = "P@ssw0rd"
      # n2.ssh.keys_only = false
    #   n2.vm.provision "shell", inline: $script, env: {'CONSUL_DEMO_VERSION' => CONSUL_DEMO_VERSION}
    consul02.vm.network "private_network", ip: "172.20.20.12"
  end
  
  config.vm.define "consul03" do |consul03|
    consul03.vm.hostname = "consul03"
    # Forward Consul web and api port 8500
    consul03.vm.network "forwarded_port", guest: 8500, host: 8513
      # n3.ssh.username = "root"
      # n3.ssh.password = "P@ssw0rd"
      # n3.ssh.keys_only = false
    #   n3.vm.provision "shell", inline: $script, env: {'CONSUL_DEMO_VERSION' => CONSUL_DEMO_VERSION}
    consul03.vm.network "private_network", ip: "172.20.20.13"
  end

  config.vm.define "consul04" do |consul04|
    consul04.vm.hostname = "consul04"
    # Forward Consul web and api port 8500
    consul04.vm.network "forwarded_port", guest: 8500, host: 8514
      # n4.ssh.username = "root"
      # n4.ssh.password = "P@ssw0rd"
      # n4.ssh.keys_only = false
    #   n4.vm.provision "shell", inline: $script, env: {'CONSUL_DEMO_VERSION' => CONSUL_DEMO_VERSION}
    consul04.vm.network "private_network", ip: "172.20.20.14"
  end


  config.vm.define "consul05" do |consul05|
    consul05.vm.hostname = "consul05"
    # Forward Consul web and api port 8500
    consul05.vm.network "forwarded_port", guest: 8500, host: 8515
      # n5.ssh.username = "root"
      # n5.ssh.password = "P@ssw0rd"
      # n5.ssh.keys_only = false
    #   n5.vm.provision "shell", inline: $script, env: {'CONSUL_DEMO_VERSION' => CONSUL_DEMO_VERSION}
    consul05.vm.network "private_network", ip: "172.20.20.15"
  end

  config.vm.define "vault01" do |vault01|
    vault01.vm.hostname = "vault01"
    # Forward Vault web and api port 8200
    vault01.vm.network "forwarded_port", guest: 8200, host: 8516
    # n6.ssh.username = "root"
    # n6.ssh.password = "P@ssw0rd"
    # n6.ssh.keys_only = false
    # n6.vm.provision "shell", inline: $script, env: {'CONSUL_DEMO_VERSION' => CONSUL_DEMO_VERSION}
    vault01.vm.network "private_network", ip: "172.20.20.16"
  end

  config.vm.define "vault02" do |vault02|
    vault02.vm.hostname = "vault02"
    # Forward Vault web and api port 8200
    vault02.vm.network "forwarded_port", guest: 8200, host: 8517
    # n7.ssh.username = "root"
    # n7.ssh.password = "P@ssw0rd"
    # n7.ssh.keys_only = false
    # n7.vm.provision "shell", inline: $script, env: {'CONSUL_DEMO_VERSION' => CONSUL_DEMO_VERSION}
    vault02.vm.network "private_network", ip: "172.20.20.17"
  end
  
  config.vm.define "vault03" do |vault03|
    vault03.vm.hostname = "n8"
    # Forward Vault web and api port 8200
    vault03.vm.network "forwarded_port", guest: 8200, host: 8518
    # n8.ssh.username = "root"
    # n8.ssh.password = "P@ssw0rd"
    # n8.ssh.keys_only = false
    # n8.vm.provision "shell", inline: $script, env: {'CONSUL_DEMO_VERSION' => CONSUL_DEMO_VERSION}
    vault03.vm.network "private_network", ip: "172.20.20.18"
  end
end
