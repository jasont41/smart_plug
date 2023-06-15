FROM alpine:latest 

ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
run pip3 install protobuf
ADD protobuf_messages/ /home/protobuf_messages/
ADD python_src/ /home/python_src/ 
ENTRYPOINT ["python" , "/home/python_src/proxy.py"]
