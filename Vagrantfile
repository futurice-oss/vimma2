# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "ubuntu/trusty64"

  config.vm.provision "shell", path: "vagrant/provision-root.sh"
  config.vm.provision "shell", privileged: false,
    path: "vagrant/provision-user.sh"
  config.vm.provision "shell", path: "vagrant/start-supervisor.sh"
  config.vm.provision "shell", run: "always", privileged: false,
    path: "vagrant/run.sh"

  config.vm.network "forwarded_port", guest: 443, host: 8081
end
