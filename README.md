# Switchbot-dashboard

Dashboard for Switchbot using InfluxDB and Grafana.

## Basic usage

1.Write Switchbot API key and other information in the .env file.

```
SWITCHBOT_ACCESS_TOKEN=
SWITCHBOT_SECRET=
INFLUXDB_TOKEN=
```

2.Get your device list.

```
$ poetry install
$ poetry run python Switchbot.py
```

3.Start docker.

```
$ docker-compose up -d --build
```

4.Watch logs.

```
$ docker-compose logs -f
```
