#!/bin/bash

kubectl apply -f pods/backend/deployment-react.yaml
kubectl apply -f pods/backend/service-react.yaml