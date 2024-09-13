# Amazing Forecast Tracker 🌧️ 🌞

## This application can:
- Monitor the 3-day forecast for a location given by latitude and longitude. 
- Return the minumum and maximum recorded temperature for a given location and hour.

## How to Install

### Pre-Requisites: 
- Docker

We will run the app using Docker Compose, which makes it very easy to get started without having to install any extra dependencies.

### Step 1: Build the docker image

    docker build . -t weather-app:latest

### Step 2: Update environment variables

- Open [deploy/docker-compose.yaml](/deploy/docker-compose.yaml)
- Replace the environment variable POSTGRES_PASSWORD with another password 🤫
- Update any of the following variables to update application settings:

Warning: I would not recommend changing VERSION, PG_HOST, or WEATHER_API_URL because it could cause issues in the application.

| name | description | example |
| -- | -- | -- |
| LATITUDE | latitude of location to monitor | 39.1031 |
| LONGITUDE | longitude of location to monitor | -39.1031 |
| INTERVAL | interval to pull forecast data (in minutes) | 60 |
| DAYS_AHEAD | number of days to look ahead for forecast data (weather API only can pull 7) | 3 |
| PG_USERNAME | username for postgres db | postgres_username |
| PG_PASSWORD | password for postgres db | postgres_password |


### Step 3. Run Docker Compose. 
```
docker compose -f deploy/docker-compose.yaml up
```

You should see some Postgres + FastAPI logs in the console along with the final success message "Application startup complete." If you see any errors in the console, the application may not have started correctly.

### Step 4: Explore the application

You can find swagger documentation at [http://localhost:8000/api/docs](http://localhost:8000/api/docs)

You can try:
- Configuring different latitude and longitudes to load data for multiple locations
- Configuring different intervals and explore how often the forecast changes
- Trying out the API to find the min and max temperatures recorded for a location

### Step 5: Stop the application

You can stop the application by running:

```
docker compose -f deploy/docker-compose.yaml stop
```

You can also run the following to stop the application and remove all services:

```
docker compose -f deploy/docker-compose.yaml down
```

## Assumptions:

While developing this application I came across a few unknowns. I took the following assumptions:

| Related To | Assumption |
| --- | --- |
| Requirement #3 | By next 72 hours I assume that is inclusive to the current hour as well as the end hour. For example, if it is 10:30 currently, we get data for 10:00 today, as well as for 10:00 on the 3rd day. 10:00 on the 3rd day would be the last hour we get data for. |
| Requirement #6 | We should only have one container that runs the application. If I were implementing this in real life I would likely have 1 container for the API and another container for the forecast data pull, but for the sake of the exercise I ran them as one app. |
| Requirement #1 | The app only needs to monitor one location. In the full system, multiple locations would be monitored. |
| Requirement #5 | By highest/lowest recorded forcast, this means we need to return the highest and lowest forecast in the database for the specified location, day and hour of day that was recorded. |
| Weather API Response | I assumed all units coming from the Weather API would be in Fahrenheit, but this might not always be the case |
