
# Hurricane Data Scraping and Extraction

This project focuses on scraping hurricane data from a Wikipedia page, extracting it into structured formats, and saving it as a CSV file. The data extraction is aided by an LLM (Large Language Model) via OpenAI's API. The project consists of two main scripts:

1. **hurricane_scraper.py**: Scrapes raw hurricane data from a Wikipedia page.
2. **hurricane_llm_extraction.py**: Uses the OpenAI API to extract and format the scraped data into structured CSV.

## Step-by-Step Instructions

### 1. Create a Local Virtual Environment

To keep your dependencies organized, it is recommended to create a virtual environment for the project.

#### For Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### For macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Required Libraries

Once your virtual environment is activated, install the required dependencies listed in the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

In order to use the OpenAI API, you need to add your API key. Create a `.env` file in the root directory and add the following line:

```
OPENAI_API_KEY=your_openai_api_key
```

Replace `your_openai_api_key` with your actual OpenAI API key.

### 4. Run the Web Scraper

The first step in the process is to scrape the hurricane data from Wikipedia. Run the `hurricane_scraper.py` script to do this:

```bash
python hurricane_scraper.py
```

This will output a `hurricane_data.json` file that contains the raw data scraped from the website.

### 5. Run the LLM Extraction Script

After scraping the raw data, the next step is to extract structured information using the LLM. Run the `hurricane_llm_extraction.py` script to process the JSON and create a CSV file:

```bash
python hurricane_llm_extraction.py
```

This will generate a CSV file named `hurricane_data.csv` containing the structured data.

---

## Methodology

The task of scraping, data extraction, and data quality assessment was approached systematically to ensure accurate and structured output.

For scraping, the requests library was utilized to fetch the HTML content from the target website. The BeautifulSoup library was employed to parse the HTML structure and extract relevant data such as hurricane names,
dates, areas affected, and number of deaths. Regular expressions were applied where necessary to clean and extract specific information from unstructured text.

For data extraction, the OpenAI API was used to help transform unstructured data into structured JSON format, specifically focusing on extracting hurricane-related information.
The extraction process ensured the correct identification of fields such as storm names, start/end dates, affected areas, and death counts, even when the data was embedded in descriptive paragraphs. Additional cleaning steps were taken to handle missing values and ensure consistent data formatting.

To assess the quality of the extracted data, a thorough review was conducted to ensure completeness and accuracy. This included cross-referencing extracted values with the original source content and implementing 
safeguards to handle missing or erroneous values (e.g., defaulting missing fields to "not known" or 0 for deaths). Overall, this approach provided a robust mechanism for gathering and structuring data from a dynamic webpage.