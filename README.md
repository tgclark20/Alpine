# ALPINE
Created By: Timothy Clark

Version: 1.3.0

## Overview
Alpine is an open source tool-kit designed to utilize the Alpaca API in order to test, experiment, and 
implement basic algorithmic trading models. training models can be added to replace movingAverage.py

*Disclaimer: This application, and the models included are not to be considered financial advice. this application is 
purely for educational and experimental purposes only*

**1.3.0 Changelog:** 
- Replaced Celery with APScheduler for scheduling tasks 
- Updated calls to Alpaca to use API V2 
- Updated requirements documentation (removing redis and celery dependencies)

## Requirements

An active Alpaca account is also required. It is reccomended to start with a paper trading account to ensure no accidental losses during setup.

## Setup
once all requirements are met, ensure all configurations are set in *constants.py*

Also, prior to the initial running, create initial buy orders in Alpaca. then run 
sqlUtils.addStock(ticker,qty) to match your alpaca account 

## Work Items
This as an ongoing project. feel free to give suggestions/pull requests to help contribute