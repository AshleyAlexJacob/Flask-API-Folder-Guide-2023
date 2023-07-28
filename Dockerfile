# specifying which python environment to use
FROM python:3.9-slim

# create a main app directory in the container
RUN mkdir /app

# set the app directory as the main directory
WORKDIR /app

# copying all the files within project source directory
ADD . ./

# install dependencies for mysql client
RUN apt update -y && apt install default-libmysqlclient-dev -y 
RUN apt-get --assume-yes install gcc

# installing python packages for our usecase
RUN pip3 install --no-cache-dir --upgrade -r /app/requirements.txt

# main command to spin up the server
CMD ["python", "app.py"]

