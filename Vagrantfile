# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
	# Box
	config.vm.box = "ubuntu/bionic64"

	# Share extension
	config.vm.synced_folder "./bin/user", "/home/vagrant/weewx-pusher/bin/user"

	# Provision machine
	config.vm.provision "file", source: "./.provision/weewx.conf", destination: "/home/vagrant/weewx.conf"
	config.vm.provision "shell", path: "./.provision/bootstrap.sh", privileged: false
end
