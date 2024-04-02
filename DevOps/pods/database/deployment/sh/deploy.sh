#!/bin/bash

kubectl apply -f ../service-mongo.yaml
kubectl apply -f ../volume-mongo.yaml
kubectl apply -f ../deployment-mongo.yaml
