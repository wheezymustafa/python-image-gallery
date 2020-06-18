#!/usr/bin/bash
# Base Package Install
yum -y update && yum install -y emacs-nox tree git gcc python3 python3-devel pip3 postgresql-devel.x86_64 postgresql.x86_64
amazon-linux-extras install -y nginx1
# Adding ext. ssh key
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCDldDiXWAdP9sq9KlxQaTVkF2DMFq9CQXk0pLqSY2jjaS1PQgj0Svf7RGSbMVlgSdd87Qdc534r26L6l+2GVQcMTClyFDZGdxf9vrfhJV8+Eyj5MFDMsBO9EDO9T+EAqfcz1+oXoGd7/slehHyQ9O12tcxNZmViWpHNrv9WAtBcpKR+M9k0PKydnH0GtSU4Ta33/fAagTUP2Q20J01qLwEW6R70xObQ+POmrhLWwHoQtpTtCy5DUP6ZV3To+JCSL7ZDbxNuR98P/awe7bdPiv0sXvC68a1GsAamBmt96mQFrCrS44GIcjgVCWdWSacBA8BGTQz5tmGahIXkcK3xbqH cpsc4973ta" >>${HOME}/.ssh/authorized_keys

#Install software
cd /home/ec2-user
git clone https://github.com/wheezymustafa/python-image-gallery.git
chown -R ec2-user:ec2-user python-image-gallery

systemctl stop postfix
systemctl disable postfix
