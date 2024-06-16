#!/bin/bash

git checkout app/api

git add .
git commit -m "changes"

git push origin app/api
git merge app/api
git checkout develop