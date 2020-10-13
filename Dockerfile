# syntax = docker/dockerfile:1.0-experimental

# First build stage, it will not persist in the final image
FROM debian as intermediate

# Me
MAINTAINER Josep Quintana

RUN echo "Log file: /docker-build.log"

# Install git
RUN DEBIAN_FRONTEND=noninteractive apt-get update > /docker-build.log 2>&1
RUN DEBIAN_FRONTEND=noninteractive apt-get install -qq git > /docker-build.log 2>&1

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
FROM debian AS final
RUN mkdir -p /srv/PTI
COPY --from=intermediate /PTI /srv/PTI

# Install dependencies
RUN DEBIAN_FRONTEND=noninteractive apt-get update > /docker-build.log 2>&1
RUN DEBIAN_FRONTEND=noninteractive apt-get install -qq curl apt-utils > /docker-build.log 2>&1
RUN DEBIAN_FRONTEND=noninteractive apt-get install -qq build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev curl libbz2-dev > /docker-build.log 2>&1

RUN DEBIAN_FRONTEND=noninteractive curl -O https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tgz
RUN DEBIAN_FRONTEND=noninteractive tar -xzf Python-3.9.0.tgz
WORKDIR Python-3.9.0
RUN DEBIAN_FRONTEND=noninteractive ./configure --enable-optimizations --quiet > /docker-build.log 2>&1
RUN DEBIAN_FRONTEND=noninteractive make -j 2 --quiet > /docker-build.log 2>&1
RUN DEBIAN_FRONTEND=noninteractive make altinstall > /docker-build.log 2>&1
RUN DEBIAN_FRONTEND=noninteractive curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN DEBIAN_FRONTEND=noninteractive python3.9 get-pip.py > /docker-build.log 2>&1

# Old Python Installation for Ubuntu
#   RUN DEBIAN_FRONTEND=noninteractive apt-get install -qq software-properties-common
#   RUN DEBIAN_FRONTEND=noninteractive add-apt-repository ppa:deadsnakes/ppa 
#   RUN DEBIAN_FRONTEND=noninteractive apt-get update 
#   RUN DEBIAN_FRONTEND=noninteractive apt-get install -qq python3.7

# Set working directory
WORKDIR /srv/PTI

RUN DEBIAN_FRONTEND=noninteractive pip3.9 install -q -r requirements.txt
RUN echo "Ready to start server"

# COPY server.py .

# Start the server command
EXPOSE 80
CMD ["python3.9", "/srv/PTI/server.py", "-p 80"]
