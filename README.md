# Weather Log Processor

Parse a given log file for 5xx errors
Return temperatures in top three countries with errors

## Running locally

### clone the repo
```
git clone https://github.com/danf-share/weather_log_processor.git
cd weather_log_processor
```

### build the Docker image
```
docker build --tag log_processor_weather --file log_processor_weather.Dockerfile .
```

### run the container
Mount in the log file to be processed
Include the path and API key as arguments to the run command
```
docker run --rm -v (pwd)/sample.log:/tmp/sample.log log_processor_weather /tmp/sample.log API_KEY
```
