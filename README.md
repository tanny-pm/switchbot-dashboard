# Switchbot-dashboard

Dashboard for Switchbot using InfluxDB and Grafana.

## Basic usage

1.Write Switchbot API key and other information in the `.env` file.
note) Enter `INFLUXDB_TOKEN` after completing step 2.

```
SWITCHBOT_ACCESS_TOKEN=
SWITCHBOT_SECRET=
INFLUXDB_TOKEN=
```

2.Start docker.

```
$ docker-compose up -d --build
```

Obtain `INFLUXDB_TOKEN` from `/docker/influxdb/config/influx-configs` and write it in the `.env` file.

3.Watch logs.

```
$ docker-compose logs -f
```
