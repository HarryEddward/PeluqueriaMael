#!bin/bash

pm2 start app.js --name "mi-servidor" --watch --instances max
