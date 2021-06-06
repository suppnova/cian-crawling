# Cian crawler

App for visualizing real estate prices.
<hr/>

## Setup

### Dependencies

```bash
pip install -r requirements.txt
```

### Configurate
```ini
[APP]
REGION=ekb
```
- Should be one of `[msk, ekb, spb]`

```ini
[STORAGE]
PATH=results 
```
- Folder name for recording received files
```ini
[CRAWL]
URL=http://cian.ru/cat.php
PROXY_FILE=socks.csv
PROXY_TYPE=socks5
```
- For many requests to `cian.ru`, can use a proxy. `PROXY_FILE` contains entries of the form `<ip>:<port>`


## Usage

App consists of 4 parts (4 script files):

- Data crawler
- Geoparser
- Heatmap builder
- Histogram builder


### Data crawler

```
crawl_flats.py
```

Crawl cian.ru and write results to `<STORAGE_PATH>/flats/*.csv`. The results are divided by districts.

File contains address, main_price, price_per_m2, area.


### Geoparser

```
parse_addresses.py
```
Getting coordinates from addresses received by a crawler and write results to `<STORAGE_PATH>/coords/<REGION>/*.csv`.

File contains latitude, longitude, price.

### Heatmap builder

```
build_heatmap.py
```

Build html with heatmap for `<REGION>` used Geoparser results. Write heatmaps to `<STORAGE_PATH>/heatmaps/<REGION>/map.html`.

### Histogram builder

```
build_histograms.py
```

Build Histograms with mean prices and areas by districts used Crawler results and save it as .png to `<STORAGE_PATH>/histograms/*.png`.
