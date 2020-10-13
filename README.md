# Projecte de Tecnologies de la Informació

## Build

```
docker build -f Dockerfile --no-cache --progress=plain --secret id=id_rsa_pti_server,src=/home/jquintana/.ssh/id_rsa_pti_server -t pti_server . | more

```


## Run

```
docker run --name pti_server -d -p 80:80 pti_server
```


## Enter Container

```
docker run -it --entrypoint bash pti_server
```

## Authors

- Josep Quintana
- Omar Elkassar
- Nil Tosar
- Josep Maria Canela
