sudo apt update -y
#sudo apt install nginx=1.14.2-2+deb10u4 -y 
sudo apt install git -y
sudo apt install wget -y

mkdir /home/project
mkdir /home/project/pids

sudo apt install python3 -y
sudo apt install python3-pip -y
sudo apt-get install python3-venv -y

sudo apt-get install uwsgi -y

apt-get install uwsgi-plugin-python3 -y

#docker
sudo apt install apt-transport-https ca-certificates curl gnupg2 software-properties-common -y
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable" -y
sudo apt update -y
sudo apt install docker-ce -y
#

#python3 -m venv venv  #inside docker-django-ui dir
#pip3 install -r requirements.txt
#uwsgi  --ini uwsgi_settings.ini 


