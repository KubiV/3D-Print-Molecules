import requests
import pandas as pd
from PIL import Image
from io import BytesIO

# Define the search query
query = "title:protein"

# Define the URL for the search API
url = "https://search.rcsb.org/rcsbsearch/v1/query"

# Define the parameters for the search API
params = {
    "json": {
        "query": {
            "type": "terminal",
            "service": "text",
            "parameters": {
                "operator": "exact_match",
                "value": query,
                "attribute": "rcsb_title"
            }
        },
        "return_type": "entry",
        "request_options": {
            "pager": {
                "start": 0,
                "rows": 10
            },
            "sort": [
                {
                    "sort_by": "score",
                    "direction": "desc"
                }
            ],
            "query_info": {
                "src": "rcsb_search",
                "query_id": "12345"
            }
        },
        "request_info": {
            "src": "rcsb_search",
            "query_id": "12345"
        }
    }
}

# Send the search request
response = requests.post(url, json=params)

# Parse the response JSON
results = response.json()["result_set"]

# Create a list to store the data
data = []

# Loop through the results and extract the data
for result in results:
    pdb_code = result["identifier"]
    molecular_mass = result["rcsb_polymer_entity_container_identifiers"]["rcsb_polymer_entity_container_molecular_weight"]
    full_title = result["rcsb_entry_info"]["title"]
    thumbnail_url = result["rcsb_entry_info"]["thumbnail"]
    
    # Download the thumbnail image
    response = requests.get(thumbnail_url)
    img = Image.open(BytesIO(response.content))
    
    # Add the data to the list
    data.append((pdb_code, molecular_mass, full_title, img))

# Create a Pandas DataFrame from the data
df = pd.DataFrame(data, columns=["PDB Code", "Molecular Mass", "Full Title", "Thumbnail"])

# Display the DataFrame
print(df)
