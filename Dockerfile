FROM ubuntu:latest
LABEL authors="ajay"

ENTRYPOINT ["top", "-b"]