#!/bin/bash

jsdoc \
    -r ../../../../../Backend/microservices/app/APIWS/v1 \
    -d docs \
    -t ./node_modules/docdash
    