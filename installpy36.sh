sudo cp ./sources/sources.list.aliyun /etc/apt/sources.list
sudo apt-get update
sudo apt-get -y install software-properties-common
sudo add-apt-repository ppa:jonathonf/python-3.6
sudo apt-get -y install build-essential libpq-dev libssl-dev openssl libffi-dev zlib1g-dev
sudo apt-get -y install python3-pip python3-dev libpython3.6-dev
## sudo apt-get -y install wget
cd ~/
wget https://www.python.org/ftp/python/3.6.2/Python-3.6.2.tgz
tar -xvf Python-3.6.2.tgz
cd Python-3.6.2
sudo ./configure --enable-optimizations --enable-shared
sudo make -j8
sudo make install

#### modify soft link
# python3 --version
# mv /usr/bin/python3 /usr/bin/python3_bak
# ln -s /usr/local/bin/python3.6 /usr/bin/python3
# python3 --version

#### ModuleNotFoundError: No module named 'lsb_release'
# ll /usr/lib/python3/dist-packages/lsb_release.py
# ln -s /usr/lib/python3/dist-packages/lsb_release.py /usr/local/lib/python3.6/site-packages/lsb_release.py


#### ERROR!
# dpkg: error processing package unattended-upgrades (--configure):
#  dependency problems - leaving unconfigured
# Processing triggers for libc-bin (2.23-0ubuntu10) ...
# Errors were encountered while processing:
#  python3-apt
#  python3-dbus
#  python3-gi
#  python3-pycurl
#  python3-software-properties
#  software-properties-common
#  unattended-upgrades
# E: Sub-process /usr/bin/dpkg returned an error code (1)
#### SOLUTION
# sudo mv /var/lib/dpkg/info /var/lib/dpkg/info.bak
# sudo mkdir /var/lib/dpkg/info
# sudo apt-get update
# apt-get -f install xxx
# sudo mv /var/lib/dpkg/info/* /var/lib/dpkg/info.bak
# sudo rm -rf /var/lib/dpkg/info
# sudo mv /var/lib/dpkg/info.bak /var/lib/dpkg/info