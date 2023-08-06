FROM python:3.8.13-slim-buster

# Install system tools
RUN apt-get update && apt-get -y install \
    git \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*
RUN apt update && apt -y install \
    build-essential \
    libpython-dev \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install poetry

# Copy over python dependency specifications
COPY pyproject.toml poetry.lock /

# Install python dependencies
RUN poetry config virtualenvs.create false && poetry install --no-dev -v && \
    pip install lap==0.4.0 cython_bbox==0.1.3 git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI

# WORKDIR /ByteTrack/pretrained
# RUN gdown --id "1P4mY0Yyd3PPTybgZkjMYhFri88nTmJX5"

# Install bytetrack
# TODO: Replace these lines by installing whatever is in the
# python setup.py develop step,
# and copying whatever is needed from the ByteTrack repo into
# the local fs
RUN git clone https://github.com/ifzhang/ByteTrack.git
WORKDIR /ByteTrack
RUN pip install -r requirements.txt && python setup.py develop

# Copy sample video
COPY friends-Scene-008.mp4 .
