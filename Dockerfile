#use python 3.7 image
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

# Set up Goocle Chrome
# Adding trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# Adding Google Chrome to the repositories
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
# Updating apt to see and install Google Chrome
RUN apt-get -y update
# Magic happens
RUN apt-get install -y google-chrome-stable

# Install Chrome Driver
# Installing Unzip
RUN apt-get install -yqq unzip
# Download the Chrome Driver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
# Unzip the Chrome Driver into /usr/local/bin directory
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
# Set display port as an environment variable
ENV DISPLAY=:99

#set the working directory
WORKDIR /snr

#install Project requirements
COPY requirements.txt .
RUN pip3 install -r requirements.txt

#copy contents to container automatic-forensic-tool
ADD . .

#start app
WORKDIR /snr/AggregateDatabases
CMD uvicorn app:app --host 0.0.0.0 --port 8080
