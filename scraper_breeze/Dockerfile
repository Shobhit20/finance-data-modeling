FROM python:3.11.6
# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip 
# Remove existing geckodriver from PATH if present
RUN rm /usr/local/bin/geckodriver || true

# Install GeckoDriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux64.tar.gz \
&& tar -zxvf geckodriver-v0.35.0-linux64.tar.gz \
&& mv geckodriver /usr/local/bin/ \
&& rm geckodriver-v0.35.0-linux64.tar.gz

RUN apt update && apt install -y firefox-esr


WORKDIR /app


COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./ /app



