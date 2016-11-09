FROM python:3-slim
RUN apt-get update -qq && apt-get install -qq git build-essential && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /script
RUN git clone https://github.com/mendersoftware/mender-backend-cli.git && cd mender-backend-cli && python3 setup.py install

ADD . /script
ENV DEVICE ${DEVICE}
ENV FAIL ${FAIL}
ENV GATEWAY ${GATEWAY}

ENTRYPOINT ["python3", "fake-update-client.py"]
