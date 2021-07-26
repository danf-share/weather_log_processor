# Weather Log Processor

Parse a given log file for 5xx errors.

Return temperatures in the three countries with the highest numbers of errors.

Output is in the format

```
<Country Code #1> <Lines Matched> <Temperature in C>
<Country Code #2> <Lines Matched> <Temperature in C>
<Country Code #3> <Lines Matched> <Temperature in C>
```

## Running locally

### Clone the repo
```
git clone https://github.com/danf-share/weather_log_processor.git
cd weather_log_processor
```

### Build the Docker image
```
docker build --tag log_processor_weather --file log_processor_weather.Dockerfile .
```

### Run the container
Mount in the log file to be processed
Include the path and API key as arguments to the run command
```
docker run --rm -v (pwd)/sample.log:/tmp/sample.log log_processor_weather /tmp/sample.log API_KEY
```
