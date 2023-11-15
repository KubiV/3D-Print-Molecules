import requests

def fetch_pdb_data_with_graphql(pdb_code):
    graphql_url = "https://data.rcsb.org/graphql"  # Updated base URL
    graphql_query = """
    query ($id: String!) {
        entry(entry_id: $id) {
            struct {
                title
            }
            rcsb_entry_info {
                molecular_weight
            }
            # Add any other fields you need
        }
    }
    """

    variables = {"id": pdb_code}

    headers = {
        "Content-Type": "application/json",
        # Add any other headers if needed
    }

    try:
        response = requests.post(graphql_url, json={"query": graphql_query, "variables": variables}, headers=headers)
        response.raise_for_status()

        data = response.json()["data"]["entry"]
        protein_name = data["struct"]["title"]
        molecular_mass = data["rcsb_entry_info"]["molecular_weight"]
        # Add any other relevant properties you need

        # Update your table or display the fetched data as needed
        print(f"Protein Name: {protein_name}")
        print(f"Molecular Mass: {molecular_mass} Da")
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"An unexpected error occurred: {err}")

# Example usage:
pdb_code_to_search = "1CGO"  # Replace with the desired PDB code
fetch_pdb_data_with_graphql(pdb_code_to_search)
