FROM python:3.9-slim-buster

WORKDIR /app

# Install dependencies for building SQLite
RUN apt-get update && apt-get install -y wget build-essential

# Download and compile SQLite from source
RUN wget https://www.sqlite.org/2022/sqlite-autoconf-3400000.tar.gz && \
    tar xvfz sqlite-autoconf-3400000.tar.gz && \
    cd sqlite-autoconf-3400000 && \
    ./configure && \
    make && make install && \
    ldconfig

# Install Python dependencies
ADD . /app
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5001
CMD ["python", "backend.py"]