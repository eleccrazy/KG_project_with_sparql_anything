import requests
from typing import Optional, Dict, Any

def fetch_wikidata_info(qid: str) -> Optional[Dict[str, Any]]:
    """
    Fetches structured information from Wikidata for a given entity using its QID.
    
    This function executes a SPARQL query on the Wikidata endpoint to fetch details like:
    - Nationality
    - Gender
    - Given name
    - Family name
    - Place of birth
    - Work period start and end
    - Occupations
    - Works in collection
    - Field of work
    - Awards received

    Args:
        qid (str): The Wikidata QID of the entity (e.g., Q1063584).

    Returns:
        Optional[Dict[str, Any]]: A dictionary containing the fetched information, or None if the request fails.
    """
    
    sparql_endpoint = "https://query.wikidata.org/sparql"
    
    sparql_query = f"""
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?nationality
           ?gender
           ?givenName
           ?familyName
           ?placeOfBirth
           ?workPeriodStart
           ?workPeriodEnd
           (GROUP_CONCAT(DISTINCT ?occupation; SEPARATOR=", ") AS ?occupations) 
           (GROUP_CONCAT(DISTINCT ?workInCollection; SEPARATOR=", ") AS ?worksInCollection)
           (GROUP_CONCAT(DISTINCT ?fieldOfWork; SEPARATOR=", ") AS ?fieldsOfWork)
           (GROUP_CONCAT(DISTINCT ?awardReceived; SEPARATOR=", ") AS ?awards)
    WHERE {{
        SERVICE <https://query.wikidata.org/sparql> {{
            wd:{qid} wdt:P27 ?nationalityEntity .
            ?nationalityEntity rdfs:label ?nationality .
            FILTER(LANG(?nationality) = "en")

            OPTIONAL {{ 
                wd:{qid} wdt:P106 ?occupationEntity .
                ?occupationEntity rdfs:label ?occupation .
                FILTER(LANG(?occupation) = "en")
            }}

            OPTIONAL {{ 
                wd:{qid} wdt:P6379 ?workInCollectionEntity .
                ?workInCollectionEntity rdfs:label ?workInCollection .
                FILTER(LANG(?workInCollection) = "en")
            }}

            OPTIONAL {{
                wd:{qid} wdt:P21 ?genderEntity .
                ?genderEntity rdfs:label ?gender .
                FILTER(LANG(?gender) = "en")
            }}

            OPTIONAL {{
                wd:{qid} wdt:P735 ?givenNameEntity .
                ?givenNameEntity rdfs:label ?givenName .
                FILTER(LANG(?givenName) = "en")
            }}

            OPTIONAL {{
                wd:{qid} wdt:P734 ?familyNameEntity .
                ?familyNameEntity rdfs:label ?familyName .
                FILTER(LANG(?familyName) = "en")
            }}

            OPTIONAL {{
                wd:{qid} wdt:P19 ?placeOfBirthEntity .
                ?placeOfBirthEntity rdfs:label ?placeOfBirth .
                FILTER(LANG(?placeOfBirth) = "en")
            }}

            OPTIONAL {{
                wd:{qid} wdt:P101 ?fieldOfWorkEntity .
                ?fieldOfWorkEntity rdfs:label ?fieldOfWork .
                FILTER(LANG(?fieldOfWork) = "en")
            }}

            OPTIONAL {{
                wd:{qid} wdt:P2031 ?workPeriodStart .
            }}

            OPTIONAL {{
                wd:{qid} wdt:P2032 ?workPeriodEnd .
            }}

            OPTIONAL {{
                wd:{qid} wdt:P166 ?awardReceivedEntity .
                ?awardReceivedEntity rdfs:label ?awardReceived .
                FILTER(LANG(?awardReceived) = "en")
            }}
        }}
    }}
    GROUP BY ?nationality ?gender ?givenName ?familyName ?placeOfBirth ?workPeriodStart ?workPeriodEnd
    """
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    # Send the query to Wikidata SPARQL endpoint
    response = requests.get(sparql_endpoint, params={"query": sparql_query, "format": "json"}, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        results = data.get("results", {}).get("bindings", [])
        
        if results:
            result = results[0]  # Since we're grouping by a single entity, expect one result
            return {
                "nationality": result.get("nationality", {}).get("value", "Unknown"),
                "gender": result.get("gender", {}).get("value", "Unknown"),
                "givenName": result.get("givenName", {}).get("value", "Unknown"),
                "familyName": result.get("familyName", {}).get("value", "Unknown"),
                "placeOfBirth": result.get("placeOfBirth", {}).get("value", "Unknown"),
                "workPeriodStart": result.get("workPeriodStart", {}).get("value", "Unknown"),
                "workPeriodEnd": result.get("workPeriodEnd", {}).get("value", "Unknown"),
                "occupations": result.get("occupations", {}).get("value", "No occupations available"),
                "worksInCollection": result.get("worksInCollection", {}).get("value", "No works in collection"),
                "fieldsOfWork": result.get("fieldsOfWork", {}).get("value", "No field of work available"),
                "awards": result.get("awards", {}).get("value", "No awards received")
            }
        else:
            return {"error": "No data found for the given QID."}
    else:
        return {"error": f"Failed to fetch data: {response.status_code}"}
