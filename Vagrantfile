# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
	# Box
	config.vm.box = "ubuntu/trusty64"

	# Share extension
	config.vm.synced_folder ".", "/home/vagrant/extension"
	config.vm.synced_folder "./bin/user/pusher", "/home/weewx/bin/user/pusher"

	# Provision machine
	config.vm.provision "file", source: "./.provision/weewx.conf", destination: "/home/vagrant/weewx.conf"
	config.vm.provision "shell", path: "./.provision/bootstrap.sh"
end
