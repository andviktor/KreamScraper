# Kream Store Scraper

## Description
The Kream Store Scraper is a straightforward, yet versatile, web scraping tool designed to extract data from the Kream online store. With two distinct versions—simple and concurrent—and powered by Zenrows API, this scraper empowers you to access all products from Kream's online store and efficiently obtain only the latest additions to their inventory.

![kream-output-csv-demo](https://github.com/andviktor/KreamScraper/assets/20559261/42f01f78-b40b-434d-a5ca-f0dae1582010)

## Key Features
- **Simple and Concurrent Versions:** Choose between the simple and concurrent versions of the scraper to suit your specific needs. The simple version is available in the `main.py` file, while the concurrent version can be found in `concurrency.py`.

- **Zenrows API Integration:** The scraper seamlessly integrates with Zenrows API to provide a reliable and efficient data extraction process.

- **Complete Product Data:** Gather detailed information about products, including names, prices, descriptions, sizes, and availability, enabling you to stay informed about Kream's offerings.

- **New Product Detection:** Easily identify and extract only the latest products added to the Kream online store, helping you stay ahead in the world of fashion, sneakers, and streetwear.

## Installation
To get started, follow these simple steps:
1. Clone this repository.
2. Set up a virtual environment.
3. Install the required dependencies using `pip install -r requirements.txt`.
4. At the beginning of the chosen `.py` file (either `main.py` or `concurrency.py`), paste your Zenrows API token to enable seamless integration.
