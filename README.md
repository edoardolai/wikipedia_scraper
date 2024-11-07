# Leaders Data Scraper

## Project Overview

This project is a didactic web scraping tool designed to extract information about country leaders and their biographies from an online API and Wikipedia. The data is processed, cleaned using regular expressions, and stored in a JSON file for further use.

## Features

- **Fetch Leaders Data**: Retrieves leader names and related information from the `country-leaders.onrender.com` API.
- **Extract Wikipedia Paragraphs**: Uses BeautifulSoup to scrape the first relevant paragraph from a leader's Wikipedia page.
- **Data Cleaning**: Applies several regular expressions to clean the scraped data:
  - Removes phonetic notations.
  - Removes footnote references.
  - Removes non-breaking spaces.
  - Filters out non-meaningful or irrelevant characters.
- **JSON Export**: Saves the cleaned data in a structured JSON file.

## Installation

### Prerequisites

- Python 3.8+
- Required Python packages:
  - `requests`
  - `beautifulsoup4`

### Install Dependencies

Run the following command to install the required libraries:
```bash
pip install requests beautifulsoup4