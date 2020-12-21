# Projecte de Tecnologies de la Informació

## Environment

### Add SSH Key to the ssh-agent
```
eval $(ssh-agent -s)
ssh-add ~/.ssh/id_rsa_pti_server
```

### Fetch a single file from Github
```
git fetch && git checkout origin/master -- ./webserver/Dockerfile_WEBSERVER
git fetch && git checkout origin/master -- ./blockchain/Dockerfile_BLOCKCHAIN
git fetch && git checkout origin/master -- ./database/Dockerfile_DATABASE
git fetch && git checkout origin/master -- ./frontend/Dockerfile_FRONTEND
```

## Build

```
docker build -f ./webserver/Dockerfile_WEBSERVER --no-cache --progress=plain --secret id=id_rsa_pti_server,src=/home/jquintana/.ssh/id_rsa_pti_server -t pti_webserver . | more
```
```
docker build -f ./blockchain/Dockerfile_BLOCKCHAIN --no-cache --progress=plain -t pti_blockchain . | more
```
```
docker build -f ./database/Dockerfile_DATABASE --no-cache --progress=plain -t pti_database . | more
```
```
docker build -f ./frontend/Dockerfile_FRONTEND --no-cache --progress=plain -t pti_frontend . | more
```

## Run

```
docker run --name pti_webserver -d -p 80:80 pti_webserver
```
```
docker run --name pti_blockchain -d -p 8545:8545 pti_blockchain
```
```
docker run --name pti_database -d -p 27017:27017 pti_database
```
```
docker run --name pti_frontend -d -p 80:80 pti_frontend
```


## Enter Container interactively

```
docker run -it --entrypoint bash <containerName>
```

## Stop and Remove Container

```
docker stop <containerName>
docker rm <containerName>
```

## Check Docker logs

```
docker logs <containerName>
```

## Copy from docker container to host

```
docker cp <containerId>:/file/path/within/container /host/path/target
```

## Truffle Ganache Commands

```
truffle compile
truffle networks --clean
truffle migrate -f X --to Y
```

## Flutter WebApp

```
flutter channel beta
flutter upgrade
flutter config --enable-web

flutter devices

flutter create .
flutter build web
```

## Authors

- Josep Quintana
- Omar Elkassar
- Nil Tosar
- Josep Maria Canela


## TO DO

- [x] Dockerfile for Blockchain (truffle)
- [x] Simple API endpoint
- [x] Truffe Process start
- [x] web3js
- [x] Recompile contracts and get abi address
- [x] Create, block, unblock and delete Bids
- [x] Think how will user_2 approve SELL
- [x] Escrow.sol
- [x] User management
- [ ] Flutter
- [ ] Use Docker Hub
- [ ] IPFS
- [ ] Private Blockchain

