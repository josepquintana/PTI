# Projecte de Tecnologies de la Informació

## Environment

### Add SSH Key to the ssh-agent
```
eval $(ssh-agent -s)
ssh-add ~/.ssh/id_rsa_pti_server
```

### Fetch a single file from Github
```
git fetch && git checkout origin/master -- Dockerfile_WEBSERVER
git fetch && git checkout origin/master -- Dockerfile_BLOCKCHAIN
git fetch && git checkout origin/master -- Dockerfile_DATABASE
```

## Build

```
docker build -f Dockerfile_WEBSERVER --no-cache --progress=plain --secret id=id_rsa_pti_server,src=/home/jquintana/.ssh/id_rsa_pti_server -t pti_webserver . | more
```
```
docker build -f Dockerfile_BLOCKCHAIN --no-cache --progress=plain --secret id=id_rsa_pti_server,src=/home/jquintana/.ssh/id_rsa_pti_server -t pti_blockchain . | more
```
```
docker build -f Dockerfile_DATABASE --no-cache --progress=plain --secret id=id_rsa_pti_server,src=/home/jquintana/.ssh/id_rsa_pti_server -t pti_database . | more
```

## Run

```
docker run --name pti_webserver -d -p 80:80 pti_webserver
```
```
docker run --name pti_blockchain -d -p 9999:9999 pti_blockchain
```
```
docker run --name pti_database -d -p 27017:27017 pti_database
```


## Enter Container

```
docker run -it --entrypoint bash pti_webserver
```
```
docker run -it --entrypoint bash pti_blockchain
```
```
docker run -it --entrypoint bash pti_database
```


## Authors

- Josep Quintana
- Omar Elkassar
- Nil Tosar
- Josep Maria Canela


## TO DO

- [x] Dockerfile for Blockchain (truffle)
- [] Simple API endpoint
- [] Truffe Process start
- [] Use Docker Hub
- [] IPFS
- [] Private Blockchain

