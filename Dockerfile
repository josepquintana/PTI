# Build Image
FROM ubuntu AS pti

#Install Python
RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -qq software-properties-common
RUN DEBIAN_FRONTEND=noninteractive add-apt-repository ppa:deadsnakes/ppa 
RUN DEBIAN_FRONTEND=noninteractive apt-get update 
RUN DEBIAN_FRONTEND=noninteractive apt-get install -qq python3.7
RUN DEBIAN_FRONTEND=noninteractive apt-get install -qq curl
RUN DEBIAN_FRONTEND=noninteractive curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN DEBIAN_FRONTEND=noninteractive python3.7 get-pip.py
RUN DEBIAN_FRONTEND=noninteractive rm get-pip.py
RUN DEBIAN_FRONTEND=noninteractive pip3.7 install -q flask
RUN echo "Python3.7 has been installed"

# Set working directory
RUN mkdir -p /srv/PTI
WORKDIR /srv/PTI
ADD . /srv/PTI
#COPY server.py .

# Start the server command
EXPOSE 80
CMD ["python3.7", "/srv/PTI/server.py --port 80"]
