#!/bin/sh
sudo docker rm myswapi
sudo docker build -t myswapi -f ./mysql.dockerfile ./
