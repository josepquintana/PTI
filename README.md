# Projecte de Tecnologies de la Informació

## Build

```
docker build -f Dockerfile_WEBSERVER --no-cache --progress=plain --secret id=id_rsa_pti_server,src=/home/jquintana/.ssh/id_rsa_pti_server -t pti_webserver . | more
```
```
docker build -f Dockerfile_BLOCKHAIN --no-cache --progress=plain --secret id=id_rsa_pti_server,src=/home/jquintana/.ssh/id_rsa_pti_server -t pti_blockchain . | more
```


## Run

```
docker run --name pti_webserver -d -p 80:80 pti_webserver
```
```
docker run --name pti_blockchain -d -p 9999:9999 pti_blockchain
```


## Enter Container

```
docker run -it --entrypoint bash pti_webserver
```

```
docker run -it --entrypoint bash pti_blockchain
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