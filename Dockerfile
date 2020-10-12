FROM ubuntu AS pti
RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -yq software-properties-common
RUN DEBIAN_FRONTEND=noninteractive add-apt-repository ppa:deadsnakes/ppa 
RUN DEBIAN_FRONTEND=noninteractive apt-get update 
RUN DEBIAN_FRONTEND=noninteractive apt-get install -yq python3.7
RUN echo "Python3.7 has been installed"


RUN mkdir -p /usr/src/pti
WORKDIR /usr/src/pti
COPY server.py .
#RUN apt-get install somedependency
RUN pip3.7 install flask
EXPOSE 80
EXPOSE 443
CMD ["python3.7", "./server.py"]
