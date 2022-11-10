FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt
RUN pip3 install mysql-connector-python

COPY . /app

EXPOSE 8090

ENTRYPOINT ["python3"]

CMD ["app.py"]