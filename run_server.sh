sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get install -y python3-pip
sudo apt-get install build-essential libssl-dev libffi-dev python-dev

sudo apt-get install -y python3-venv
python3 -m venv my_env


source my_env/bin/activate
source my_env/bin/postactivate
pip3 install -r requirements.txt
cd src
python server.py