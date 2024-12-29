import requests
from typing import List, Dict, Union


# Define the SPARQL endpoint
sparql_endpoint = "http://localhost:3000/sparql.anything"


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
                SERVICE <x-sparql-anything:location=file:///home/gizachew/main/msc/SecondSemester/KG/project/dataset/Artists.json> {{
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
                        "wiki_qid": item.get("wikiQID", {}).get("value", "Not available")
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

    # Prepare the SPARQL query with the given keyword
    sparql_query = f"""
    PREFIX xyz: <http://sparql.xyz/facade-x/data/>
    PREFIX fx: <http://sparql.xyz/facade-x/ns/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT ?title ?medium ?dimensions ?creditLine ?date ?url ?imageURL ?artistName
    WHERE {{
        SERVICE <x-sparql-anything:location=file:///home/gizachew/main/msc/SecondSemester/KG/project/dataset/Artworks.json> {{
            ?artwork xyz:Title ?title ;
                     xyz:Artist ?artistNode ;
                     xyz:Medium ?medium ;
                     xyz:Dimensions ?dimensions ;
                     xyz:CreditLine ?creditLine ;
                     xyz:Date ?date ;
                     xyz:URL ?url ;
                     xyz:ImageURL ?imageURL .
            
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
