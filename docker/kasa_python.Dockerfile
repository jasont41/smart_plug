FROM alpine:latest 

ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
# RUN apt-get update 
# RUN apt-get install -y python3 
# RUN apt-get install -y iputils-ping
# RUN apt install -y python3-pip
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
RUN pip3 install python-kasa==0.4.0.dev0
run pip3 install protobuf
# COPY . . 
ADD protobuf_messages/ /home/protobuf_messages/
ADD python_src/ /home/python_src/ 
ENTRYPOINT ["python" , "/home/python_src/main.py"]
