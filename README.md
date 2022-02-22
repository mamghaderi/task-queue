## Description


In this code, I used mqtt as inbound and outbound of the ortools library. The server subscribes to settings.MQTT_REQUEST_TOPIC, to receive messages from the client. Message data protocol is list of lat and lons as follow:

```python
data = [[2, 3], [4, 6], [7, 8]]
```

The server calculate distance matrix and send it to ortools, to get answer. Server print out ortools's answer in
settings.MQTT_RESULT_TOPIC for client to pick. Server publishes answer with retain sets to True, so client in each
subscription, will get last answer, even if messages published when it was disconnected.

## What should client do?

Client should publish its questions in mentioned format to settings.MQTT_REQUEST_TOPIC topic, and subscribe to
settings.MQTT_RESULT_TOPIC topic to get results.


## Run Server locally

run example.sh file for server running

## Client example

There is a client example publish and subscribe in src/client.py file.

## Run in docker:

First create image:

```bash
sudo docker build -t task_queue:latest .
```

Then run docker compose:

```bash
sudo docker-compose up
```
