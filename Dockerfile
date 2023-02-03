# Dockerfile
FROM python:3.8
WORKDIR /fastApiForTests
COPY . /fastApiForTests
RUN pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["./docker-entrypoint.sh"]
