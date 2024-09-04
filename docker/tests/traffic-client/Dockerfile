FROM debian:12.6-slim

# Install supervisor
RUN apt-get update && apt-get install -y curl && apt-get clean

CMD [ "sh", "-c", "echo 'traffic client started' && sleep 1000" ]