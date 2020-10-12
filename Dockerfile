# First build stage, it will not persist in the final image
FROM ubuntu as intermediate

# Install git
RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -yq git

# Add credentials on this first build
ARG SSH_PRIVATE_KEY
RUN mkdir /root/.ssh/
RUN echo "${SSH_PRIVATE_KEY}" > /root/.ssh/id_rsa

# Make sure the Github domain is accepted
RUN touch /root/.ssh/known_hosts
RUN ssh-keyscan github.com >> /root/.ssh/known_hosts

# Clone the Github repository
RUN git clone git@github.com:josepquintana/PTI.git

# Final Image, where the repository from the previous image is copied to
FROM ubuntu AS pti
COPY --from=intermediate /PTI /srv/PTI

# Install dependencies
RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -yq software-properties-common
RUN DEBIAN_FRONTEND=noninteractive add-apt-repository ppa:deadsnakes/ppa 
RUN DEBIAN_FRONTEND=noninteractive apt-get update 
RUN DEBIAN_FRONTEND=noninteractive apt-get install -yq python3.7
RUN DEBIAN_FRONTEND=noninteractive pip3.7 install -q flask
RUN echo "Python3.7 has been installed"

# Set working directory
# RUN mkdir -p /usr/src/pti
WORKDIR /srv/PTI
# COPY server.py .

# Start the server command
EXPOSE 80
CMD ["python3.7", "./server.py --port 80"]
