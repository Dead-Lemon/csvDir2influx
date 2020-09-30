FROM ubuntu:20.04

MAINTAINER Lemon

WORKDIR /app

RUN apt-get update && apt install python3-pip -y
RUN python3 -m pip install --upgrade pip

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "./importCSVfolder.py" ]
