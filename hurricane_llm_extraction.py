import openai, os, json, pandas as pd
from dotenv import load_dotenv
from datetime import datetime

# Load env and API key
def load_env():
    load_dotenv()
    return os.getenv("OPENAI_API_KEY")

# Load JSON data
def load_json(file_path):
    with open(file_path) as file:
        return json.load(file)

# Prepare LLM message
def prepare_messages(hurricane, fields):
    fields_list = "\n".join([f"- '{field}': {desc}" for field, desc in fields.items()])
    return [
        {"role": "system", "content": "You help to extract structured data."},
        {"role": "user", "content": f"""
        Extract these fields from the hurricane data:
        {fields_list}
        For 'areas_affected', try hard to extract any mentioned locations, geographical areas, or regions from the text, even if they are not directly labeled as affected areas. If no areas are found at all, return 'not known'. 
        Example: If the text mentions regions like 'Baja California Peninsula' or 'Acapulco', extract those as 'areas_affected'.
        Input: {json.dumps(hurricane, indent=2)}
        Return valid JSON with these fields only.
        """}
    ]


# LLM request
def query_llm(api_key, hurricane, fields):
    messages = prepare_messages(hurricane, fields)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages, max_tokens=1000, temperature=0
    )
    return json.loads(response['choices'][0]['message']['content'].strip())

# Extract data
def extract_data(output, hurricane_name, extracted_data):
    if hurricane_name == 'N/A' or isinstance(output.get('hurricane_storm_name'), list):
        return 
    append_data(output, hurricane_name, extracted_data)

# Append hurricane data
def append_data(data, hurricane_name, extracted_data):
    extracted_data['hurricane_storm_name'].append(hurricane_name)
    extracted_data['start_date'].append(format_date(data.get('start_date', 'N/A')))
    extracted_data['end_date'].append(format_date(data.get('end_date', 'N/A')))
    deaths = data.get('deaths', 0)
    if isinstance(deaths, str) or deaths is None:
        deaths = 0
    extracted_data['number_of_deaths'].append(deaths)
    areas_affected = data.get('areas_affected', 'not known')
    if isinstance(areas_affected, list):
        areas_affected = ", ".join(areas_affected)
    extracted_data['list_of_areas_affected'].append(areas_affected if areas_affected else 'not known')

# Format dates
def format_date(date_str):
    try:
        return datetime.strptime(f"{date_str} 1975", "%B %d %Y").strftime("%d/%m/%Y")
    except:
        return 'N/A'

# Save to CSV
def save_to_csv(extracted_data, file_path):
    df = pd.DataFrame(extracted_data)
    df = df[['hurricane_storm_name', 'start_date', 'end_date', 'number_of_deaths','list_of_areas_affected' ]]
    df['start_date'] = df['start_date'].replace('N/A', None)
    df['end_date'] = df['end_date'].replace('N/A', None)
    df['number_of_deaths'] = pd.to_numeric(df['number_of_deaths'], errors='coerce').fillna(0).astype(int)
    df.to_csv(file_path, index=False)

# Main logic
def main():
    openai.api_key = load_env()
    hurricanes = load_json("hurricane_data.json")

    fields = {
        "hurricane_storm_name": "Hurricane/storm name",
        "start_date": "Start date",
        "end_date": "End date",
        "start_date": "Number of deaths",
        "areas_affected": "List of areas affected"
    }

    extracted_data = { 'hurricane_storm_name': [], 'start_date': [], 'end_date': [], 'list_of_areas_affected': [], 'number_of_deaths': [] }

    for hurricane in hurricanes:
        hurricane_name = hurricane.get('storm_name', 'N/A')
        output = query_llm(openai.api_key, hurricane, fields)
        extract_data(output, hurricane_name, extracted_data)

    save_to_csv(extracted_data, "hurricane_data.csv")

if __name__ == '__main__':
    main()
