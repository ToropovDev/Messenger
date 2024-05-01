FROM ubuntu:latest
LABEL authors="Arseniy"

ENTRYPOINT ["top", "-b"]