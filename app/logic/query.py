import requests
from typing import List, Dict, Union
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Fetch variables from .env
SPARQL_ENDPOINT = os.getenv("SPARQL_ENDPOINT")
ARTISTS_JSON_PATH = os.getenv("ARTISTS_JSON_PATH")
ARTWORKS_JSON_PATH = os.getenv("ARTWORKS_JSON_PATH")


# Define the SPARQL endpoint
sparql_endpoint = SPARQL_ENDPOINT


def query_artist_by_name(keyword: str) -> Union[List[Dict[str, str]], Dict[str, str]]:
    """
    Queries the SPARQL endpoint for artists based on the given name keyword.
    Returns a list of formatted artist data if successful, or an error message if the request fails.

    Args:
        keyword (str): The name or part of the name of the artist to search for.

    Returns:
        Union[List[Dict[str, str]], Dict[str, str]]: 
            - A list of dictionaries with artist details (name, artist bio, begin date, end date, nationality, wiki QID) 
              if artists are found.
            - A dictionary containing an error message if the query fails or no results are found.
    """

    # Check if the SPARQL endpoint is provided
    if not SPARQL_ENDPOINT:
        return {"error": "SPARQL endpoint is not provided in the environment variables."}

    # Check if the Artists JSON file path is provided
    if not ARTISTS_JSON_PATH:
        return {"error": "Artists JSON file path is not provided in the environment variables."}

    # Prepare the SPARQL query with the given keyword
    sparql_query = f"""
    PREFIX xyz: <http://sparql.xyz/facade-x/data/>
    PREFIX fx: <http://sparql.xyz/facade-x/ns/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT ?source ?name ?ArtistBio ?BeginDate ?EndDate ?Nationality ?wikiQID
    WHERE {{
        {{
            # Subquery for artists based on DisplayName from the JSON dataset (Artists.json)
            SELECT ?source ?name ?ArtistBio ?BeginDate ?EndDate ?Nationality ?wikiQID
            WHERE {{
                SERVICE <x-sparql-anything:location={ARTISTS_JSON_PATH}> {{
                    ?artist xyz:DisplayName ?name ;
                            xyz:ArtistBio ?ArtistBio ;
                            xyz:BeginDate ?BeginDate ;
                            xyz:EndDate ?EndDate ;
                            xyz:Nationality ?Nationality ;
                            OPTIONAL {{ ?artist xyz:wikiQID ?wikiQID }} .

                    # Filter for the artist's name based on a keyword (case insensitive)
                    FILTER(CONTAINS(LCASE(?name), LCASE("{keyword}")))
                    BIND("JSON" AS ?source)
                }}
            }}
        }}
    }}
    """
    try:
     # Send the POST request to the SPARQL-Anything server
        response = requests.post(
            sparql_endpoint,
            data={"query": sparql_query, "format": "json"}
        )

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()  # Get the results as a JSON object
            results = data.get("results", {}).get("bindings", [])
        
            # Format the results into a more readable structure
            formatted_results = []
            if results:
                for item in results:
                    artist_info = {
                        "name": item.get("name", {}).get("value", "Unknown"),
                        "artist_bio": item.get("ArtistBio", {}).get("value", "No bio available"),
                        "begin_date": item.get("BeginDate", {}).get("value", "Unknown"),
                        "end_date": item.get("EndDate", {}).get("value", "Unknown"),
                        "nationality": item.get("Nationality", {}).get("value", "Unknown"),
                        "wiki_qid": item.get("wikiQID", {}).get("value", "None")
                    }
                    formatted_results.append(artist_info)
            else:
                return {"message": "No matching artists found."}
            return formatted_results
        else:
            return {"error": f"Error: {response.status_code}, {response.text}"}
    except:
        return {"error": "Sparql Anything server is not runinning"}

    
def query_artworks_by_artist_name(keyword: str) -> Union[List[Dict[str, str]], Dict[str, str]]:
    """
    Queries the SPARQL endpoint for artworks based on the given artist's name keyword.
    Returns a list of formatted artwork data if successful, or an error message if the request fails.

    Args:
        keyword (str): The name or part of the name of the artist to search for.

    Returns:
        Union[List[Dict[str, str]], Dict[str, str]]: 
            - A list of dictionaries with artwork details (title, medium, dimensions, credit line, date, url, image URL, artist name)
            - A dictionary containing an error message if the query fails or no results are found.
    """
    
    # Check if the SPARQL endpoint is provided
    if not SPARQL_ENDPOINT:
        return {"error": "SPARQL endpoint is not provided in the environment variables."}

    # Check if the Artworks JSON file path is provided
    if not ARTWORKS_JSON_PATH:
        return {"error": "Artworks JSON file path is not provided in the environment variables."}

    # Prepare the SPARQL query with the given keyword
    sparql_query = f"""
    PREFIX xyz: <http://sparql.xyz/facade-x/data/>
    PREFIX fx: <http://sparql.xyz/facade-x/ns/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT ?title ?medium ?dimensions ?date ?url ?imageURL ?artistName ?dateAquired ?creditLine
    WHERE {{
        SERVICE <x-sparql-anything:location={ARTWORKS_JSON_PATH}> {{
            ?artwork xyz:Title ?title ;
                     xyz:Artist ?artistNode ;
                     xyz:Medium ?medium ;
                     xyz:Dimensions ?dimensions ;
                     xyz:Date ?date ;
                     xyz:URL ?url ;
                     xyz:ImageURL ?imageURL .
                     
                     OPTIONAL {{ ?artwork xyz:CreditLine ?creditLine }}
                     OPTIONAL {{ ?artwork xyz:DateAcquired ?dateAquired }}
            
            # Extract the name of the artist from the blank node
            ?artistNode <http://www.w3.org/1999/02/22-rdf-syntax-ns#_1> ?artistName .

            # Filter for the artist's name based on the keyword (case insensitive)
            FILTER(CONTAINS(LCASE(?artistName), LCASE("{keyword}")))
        }}
    }}
    """
    
    try:
        # Send the POST request to the SPARQL-Anything server
        response = requests.post(
            sparql_endpoint,
            data={"query": sparql_query, "format": "json"}
        )

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()  # Get the results as a JSON object
            results = data.get("results", {}).get("bindings", [])
        
            # Format the results into a more readable structure
            formatted_results = []
            if results:
                for item in results:
                    # Create a dictionary in the desired structure
                    artwork_info = {
                        "Title": item.get("title", {}).get("value", "Unknown"),
                        "Medium": item.get("medium", {}).get("value", "Unknown"),
                        "Dimensions": item.get("dimensions", {}).get("value", "Unknown"),
                        "CreditLine": item.get("creditLine", {}).get("value", "Unknown"),
                        "Date": item.get("date", {}).get("value", "Unknown"),
                        "DateAquired": item.get("dateAquired", {}).get("value", "Unknown"),
                        "URL": item.get("url", {}).get("value", "Unknown"),
                        "ImageURL": item.get("imageURL", {}).get("value", "Unknown"),
                        "Artist": item.get("artistName", {}).get("value", "Unknown"),
                    }
                    formatted_results.append(artwork_info)
            else:
                return {"message": "No matching artworks found for the artist."}
            return formatted_results
        else:
            return {"error": f"Error: {response.status_code}, {response.text}"}
    
    except Exception as e:
        return {"error": f"Sparql Anything server is not running. Error: {str(e)}"}
