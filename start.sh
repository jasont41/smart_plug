#!/bin/bash
pip install python-kasa==0.4.0.dev0
protoc -I=protobuf_messages/ --python_out=python_src/ protobuf_messages/power_msg.proto 
python python_src/get_ips.py 
docker build -f docker/kasa_python.Dockerfile -t metrics:latest . 
docker build -f docker/proxy.Dockerfile -t proxy:latest . 
docker-compose -f deployment/compose.yml up 