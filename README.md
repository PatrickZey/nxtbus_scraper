# NXTBUS Scraper

## A tool to detail all the bus stops in Canberra

Please check the releases tab to find the csv this program builds.

It is unnecessary to run this program and strain public APIs when the resulting data is readily available.

### Why?

Action hosts a full list of Canberra bus stops on [their site](https://www.transport.act.gov.au/__data/assets/file/0006/1249692/AllStops.csv)

This data is not suitable to utilise the public facing nxtbus API. It was last updated in 2019 at the time of writing, and doesn't contain the internal stop IDs used to poll bus arrivals. In addition, the public facing API that provides a list of all stops within lat/long boundaries has bugs that make some stops intermittently not return when a large boundary is polled (such as the whole of canberra).

These APIs and their corresponding data are publicly funded and for public use, and so this repo intends to expose this public data in a useable format and provide the method to reproduce it from Action public use APIs.

### Usage

Run scraper.py. That's it.
This will output the stops.csv file in the same folder.
