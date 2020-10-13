# First build stage, it will not persist in the final image
FROM ubuntu as intermediate

# Me
MAINTAINER Josep Quintana

# Install git
RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -qq git

# Add credentials on this first build
ARG SSH_PRIVATE_KEY
RUN mkdir /root/.ssh/
RUN echo "${SSH_PRIVATE_KEY}" > /root/.ssh/id_rsa
RUN chmod 600 /root/.ssh/id_rsa

# Make sure the Github domain is accepted
RUN touch /root/.ssh/known_hosts
RUN ssh-keyscan github.com >> /root/.ssh/known_hosts

# Clone the Github repository
RUN git clone git@github.com:josepquintana/PTI.git

# Final Image, where the repository from the previous image is copied to
FROM ubuntu AS pti
RUN mkdir -p /srv/PTI
COPY --from=intermediate /PTI /srv/PTI

# Set working directory
WORKDIR /srv/PTI

# Install dependencies
RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -qq curl
RUN DEBIAN_FRONTEND=noninteractive apt-get install -qq apt-utils
RUN DEBIAN_FRONTEND=noninteractive apt-get install -qq software-properties-common
RUN DEBIAN_FRONTEND=noninteractive add-apt-repository ppa:deadsnakes/ppa 
RUN DEBIAN_FRONTEND=noninteractive apt-get update 
RUN DEBIAN_FRONTEND=noninteractive apt-get install -qq python3.7
RUN DEBIAN_FRONTEND=noninteractive curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN DEBIAN_FRONTEND=noninteractive python3.7 get-pip.py
RUN DEBIAN_FRONTEND=noninteractive rm get-pip.py
RUN DEBIAN_FRONTEND=noninteractive pip3.7 install -q flask
RUN echo "Python3.7 has been installed"

# COPY server.py .

# Start the server command
EXPOSE 80
CMD ["python3.7", "/srv/PTI/server.py", "-p 80"]
