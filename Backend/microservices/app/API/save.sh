#!/bin/bash

git checkout app/api

git add .
git commit -m "changes"

git merge app/api
git checkout develop