# About

docker image and docker compose for compiling and running WRF and WPS

# Building wrf-docker image

Build the image by using `docker-compose.yaml`

```sh
docker compose up -d
```

# Open command line interaction

To interact with WRF and WPS and run it in a docker instance

```sh
docker exec -it wrf-docker bash
```


# Inputs and Outpus

If not exists create the directory "home". It will be used to share files between the host and docker instance. 
