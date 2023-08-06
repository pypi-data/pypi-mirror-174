# For more information, please refer to https://aka.ms/vscode-docker-python
FROM jupyter/minimal-notebook

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
USER root
# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt
RUN pip install degiro_analytics
RUN mkdir /home/__pycache__

WORKDIR /home 
COPY Examples.ipynb /home
RUN chmod -R 777 /home
# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" user && chown -R user /home
USER user
