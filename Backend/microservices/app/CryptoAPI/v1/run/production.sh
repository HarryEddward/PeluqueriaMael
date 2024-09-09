#!/bin/bash

export PYTHONPATH=/peluqueriamael; gunicorn -c ../gunicorn.py server_fastapi:app