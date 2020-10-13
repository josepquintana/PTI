# syntax = docker/dockerfile:1.0-experimental

# First build stage, it will not persist in the final image
FROM debian as intermediate

# Me
MAINTAINER Josep Quintana

# Install git
RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -qq git

# Add credentials on this first build
#   OLD: [--build-arg SSH_PRIVATE_KEY="$(cat ~/.ssh/id_rsa_pti_server)"]
#     ARG SSH_PRIVATE_KEY
#     RUN echo "${SSH_PRIVATE_KEY}" > /root/.ssh/id_rsa
#
RUN mkdir /root/.ssh/
RUN --mount=type=secret,id=id_rsa_pti_server cat /run/secrets/id_rsa_pti_server > /root/.ssh/id_rsa
RUN chmod 600 /root/.ssh/id_rsa

# Make sure the Github domain is accepted
RUN touch /root/.ssh/known_hosts
RUN ssh-keyscan github.com >> /root/.ssh/known_hosts

# Clone the Github repository
RUN git clone git@github.com:josepquintana/PTI.git

# Final Image, where the repository from the previous image is copied to
FROM debian AS pti
RUN mkdir -p /srv/PTI
COPY --from=intermediate /PTI /srv/PTI

# Set working directory
WORKDIR /srv/PTI

# Install dependencies
RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -qq curl apt-utils
RUN DEBIAN_FRONTEND=noninteractive apt-get install -qq build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev curl libbz2-dev

RUN DEBIAN_FRONTEND=noninteractive curl https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tgz
RUN DEBIAN_FRONTEND=noninteractive tar -xzf Python-3.9.0.tgz
RUN DEBIAN_FRONTEND=noninteractive cd Python-3.9.0
RUN DEBIAN_FRONTEND=noninteractive ./configure --enable-optimizations
RUN DEBIAN_FRONTEND=noninteractive make -j 2
RUN DEBIAN_FRONTEND=noninteractive make altinstall

#RUN DEBIAN_FRONTEND=noninteractive apt-get install -qq software-properties-common
#RUN DEBIAN_FRONTEND=noninteractive add-apt-repository ppa:deadsnakes/ppa 
#RUN DEBIAN_FRONTEND=noninteractive apt-get update 
#RUN DEBIAN_FRONTEND=noninteractive apt-get install -qq python3.7

RUN DEBIAN_FRONTEND=noninteractive curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN DEBIAN_FRONTEND=noninteractive python3.9 get-pip.py
RUN DEBIAN_FRONTEND=noninteractive rm get-pip.py
RUN DEBIAN_FRONTEND=noninteractive pip3.9 install -q flask
RUN echo $(python3.9 --version) "has been successfully installed"

# COPY server.py .

# Start the server command
EXPOSE 80
CMD ["python3.9", "/srv/PTI/server.py", "-p 80"]
