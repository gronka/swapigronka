#!/bin/sh
sudo docker rm myswapi
sudo docker build -t myswapi -f ./mysql.dockerfile ./
sudo docker run -p 3306:3306 --name myswapi myswapi
