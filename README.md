# deconz-repeater


### Install the service

```bash
# install the service
sudo cp repeater.service /etc/systemd/system/repeater.service

# test the service
sudo systemctl start repeater.service

# stop & enable if everything works
sudo systemctl stop repeater.service
sudo systemctl enable repeater.service
```


#### Create a new app with the deconz hub

> Documentation: https://dresden-elektronik.github.io/deconz-rest-doc

All of the requests are also available in Postman (collection name: deCONZ).

### Discover the gateway

```
$ curl https://phoscon.de/discover
[
    {
        "id": "00212EFFFF06212B",
        "internalipaddress": "192.168.0.214",
        "macaddress": "00212EFFFF06212B",
        "internalport": 8081,
        "name": "Phoscon-GW",
        "publicipaddress": "176.199.208.246"
    }
]
```


### Retrieve API key

```
$ curl --location --request POST '192.168.0.214:8081/api' \
--header 'Content-Type: text/plain' \
--data-raw '{ "devicetype": "deconz-repeater"}'
[
    {
        "success": {
            "username": "2907919579"
        }
    }
]
```



### Get all lights

```
$ curl --location --request GET '192.168.0.214:8081/api/2907919579/lights'
{
    ...
}
```


### Turn something on

```
$ curl --location --request PUT '192.168.0.214:8081/api/68C70334AD/lights/2/state' \
--header 'Content-Type: text/plain' \
--data-raw '{ "on": true }'
[
    {
        "success": {
            "/lights/2/state/on": true
        }
    }
]
```
