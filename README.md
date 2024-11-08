# Leaders Data Extraction Project

This project is a didactic tool designed to demonstrate web scraping, data processing, and multiprocessing techniques using Python. The program retrieves information about world leaders from a provided API, scrapes biographical data from Wikipedia, and stores it in a structured JSON file. The updated version introduces **concurrent processing** using Python’s `multiprocessing` module to enhance performance when fetching and processing Wikipedia data.

## Features

- **Concurrent Processing:** Uses the `multiprocessing` library to fetch and process leader biographies from Wikipedia in parallel.
- **Web Scraping with BeautifulSoup:** Extracts the first paragraph of each leader's biography.
- **Dynamic Cookie Handling:** Automatically handles expired cookies when interacting with the API.
- **Regex Cleaning:** Cleans Wikipedia content using various regular expressions to remove unnecessary elements like footnote references, phonetics, and non-breaking spaces.
- **JSON Export:** Saves the structured data into a JSON file with customizable indentation.

## How It Works

1. **Fetch Country and Leader Data**  
   The program starts by fetching country data from the `https://country-leaders.onrender.com/countries` endpoint. It then retrieves leader information for each country.

2. **Handle Expired Cookies**  
   If the API returns a cookie expiration message, the program automatically fetches a new cookie and retries the request.

3. **Scrape Wikipedia in Parallel**  
   The `multiprocessing.Pool` is used to scrape each leader's Wikipedia page concurrently, significantly reducing runtime.

4. **Clean Biographical Data**  
   After extracting the first paragraph, several regex patterns are applied to clean the data.

5. **Save to JSON**  
   The final structured data is saved to `leaders.json` for later use.

## Installation

### Prerequisites

- Python 3.8+
- `requests` library
- `beautifulsoup4` library
- `lxml` parser (optional for BeautifulSoup)
- `multiprocessing` (part of Python standard library)

Install required packages:

```bash
pip install requests beautifulsoup4
```


File Structure
```bash
.
├── get_first_paragraph.py  # Contains the logic to extract and clean Wikipedia paragraphs
├── leaders_scraper.py  # Main script with multiprocessing logic
├── leaders.json  # Generated JSON file with leader data
└── .gitignore  # Ignores JSON and cache files
```

## Usage

Run the program from the command line:

```bash
python leaders_scraper.py
```

This will generate a leaders.json file containing biographical data for world leaders.

## Functions
```python
get_first_paragraph(wikipedia_url: str, regexes: List[str], session: requests.Session) -> str
```
Extracts and cleans the first relevant paragraph from the given Wikipedia URL.

```python
get_leaders() -> Dict
```

Fetches leader data for each country, retrieves their Wikipedia biographies using multiprocessing, and structures the data.

```python
save(leaders_per_country: Dict, file_name: str, indent: int = 4)
```
Saves the extracted data to a JSON file.

## Example Output

```bash
An excerpt from leaders.json:
{
  "us": [
          {
              "id": "Q23",
              "first_name": "George",
              "last_name": "Washington",
              "birth_date": "1732-02-22",
              "death_date": "1799-12-14",
              "place_of_birth": "Westmoreland County",
              "wikipedia_url": "https://en.wikipedia.org/wiki/George_Washington",
              "start_mandate": "1789-04-30",
              "end_mandate": "1797-03-04",
              "bio": "George Washington (February 22, 1732 December 14, 1799) was a Founding Father of the United States, military officer, and farmer who served as the first president of the United States from 1789 to 1797. Appointed by the Second Continental Congress as commander of the Continental Army in 1775, Washington led Patriot forces to victory in the American Revolutionary War and then served as president of the Constitutional Convention in 1787, which drafted the current Constitution of the United States. Washington has thus become commonly known as the Father of his Country."
          },
          ...
  ],
  ...
}
```
# Improvements in This Version

	•	Multiprocessing dramatically reduces the time needed to scrape and process Wikipedia data.
	•	Modular Structure: get_first_paragraph has been moved to a separate module for better organization.
	•	Error Handling: Enhanced exception handling for API and scraping failures.

# Future Improvements Ideas

	•	Unit Testing: Add unit tests for individual components.
	•	Asynchronous Requests: Use aiohttp for even faster concurrent HTTP requests.
	•	Dynamic Regex Configuration: Allow regex patterns to be configured externally.


