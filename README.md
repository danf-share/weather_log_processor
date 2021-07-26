

## build the Docker image
docker build --tag log_processor_weather --file log_processor_weather.Dockerfile .

# run the container, mounting in the log to be processed and passing it as an argument
docker run --rm -v (pwd)/sample.log:/tmp/sample.log log_processor_weather /tmp/sample.log
