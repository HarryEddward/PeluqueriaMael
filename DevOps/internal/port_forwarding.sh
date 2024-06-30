#!/bin/bash

# Variables de configuración
ROUTER_IP="192.168.1.1"
USER="mael"
INTERNAL_IP="192.168.1.144"
EXTERNAL_PORT="2222"
INTERNAL_PORT="22"

# Conectar y ejecutar comandos en el router
ssh $USER@$ROUTER_IP << EOF
iptables -t nat -A PREROUTING -p tcp --dport $EXTERNAL_PORT -j DNAT --to-destination $INTERNAL_IP:$INTERNAL_PORT
iptables -A FORWARD -p tcp -d $INTERNAL_IP --dport $INTERNAL_PORT -j ACCEPT
EOF
