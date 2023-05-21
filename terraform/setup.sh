#!/bin/bash

#Docker dependencies
sudo apt update
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu  $(lsb_release -cs)  stable"

#Installing Docker
sudo apt update
sudo apt-get install -y docker-ce
sudo apt install -y docker-compose
sudo systemctl start docker
sudo systemctl enable docker

mkdir metabase
cd metabase
curl -LfO 'https://raw.githubusercontent.com/gabriel-barata/data-pipeline-for-web-scraped-data/main/metabase/docker-compose.yaml'
sudo docker-compose up