FROM python:3.12-slim

# Install dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Setup package
COPY . /src/module
WORKDIR /src/module
RUN pip install -e .