# ALPINE
Created By: Timothy Clark

Version: 1.0.0

## Overview
Alpine is an open source tool-kit designed to utilize the Alpaca API in order to test, experiment, and 
implement basic algorithmic trading models. training models can be added to replace movingAverage.py

*Disclaimer: This application, and the models included are not to be considered financial advice. this application is 
purely for educational and experimental purposes only*

## Requirements
Along with the python packages listed in the requirements.txt file, an instance of redis needs to be running as well as
a running celery beat and worker.

An active Alpaca account is also required. It is reccomended to start with a paper trading account to ensure no 
accidental losses during setup.

### Redis:
for more info on installing and running Redis, visit https://redis.io/download 

### Celery:
with celery installed. in your terminal run the following command in an active terminal

*celery -A proj_name worker -l info -B*

## Setup
once all requirements are met, ensure all configurations are set in *constants.py*

Also, prior to the initial running, create initial buy orders in Alpaca. then run 
sqlUtils.addStock(ticker,qty) to match your alpaca account 

## Work Items
This as an ongoing project. feel free to give suggestions/pull requests to help contribute