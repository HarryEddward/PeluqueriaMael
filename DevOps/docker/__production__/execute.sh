#!/bin/bash

cd ./db
sudo ./execute.sh
cd ../

cd ./proxy/tor
sudo ./execute.sh
cd ../../

cd ./app/API
sudo ./execute.sh
cd ../../

cd ./app/CryptoAPI/
sudo ./execute.sh
cd ../../