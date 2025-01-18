from flask import Flask, request, render_template
from app.logic.query import query_artist_by_name, query_artworks_by_artist_name
from app.logic.wiki_data_query import fetch_wikidata_info

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Handle requests for the home page of the web application.

    :return: A rendered HTML template displaying the home page.
    """
    # Initialize the results variable
    results = None
    
    if request.method == 'POST':
        # Get the user input from the form
        object_name = request.form.get('artist_name')
        results = query_artist_by_name(object_name)
        if type(results) == dict:
            return render_template('error.html', message=results.get('error'))
    return render_template('index.html', results=results)

@app.route("/artist_details", methods=["GET", "POST"])
def artist_details():
    """
    Handle requests for displaying artist details from Wikidata using their Wiki QID.

    :return: A rendered HTML template displaying artist details.
    """
    wiki_qid = request.args.get("wiki_qid")  # Get the Wiki QID from the URL parameters
    artist_name = request.args.get("artist_name") # Get the artist name from the URL parameters
    artist_details = None  # Initialize the artist details variable
    # Get the artworks done by the artist from the Artworks.json file using it's name
    artworks = query_artworks_by_artist_name(artist_name)
    artworks = [] if type(artworks) == dict else artworks
    # artworks = [{'Title': 'Railing', 'Medium': 'Painted cast-iron', 'Dimensions': '28 1/4 x 46 1/2 x 3" (72.4 x 117.5 x 7.6 cm)', 'CreditLine': 'Dorothy Cullman Purchase Fund', 'Date': '1899', 'URL': 'https://www.moma.org/collection/works/82125', 'ImageURL': 'https://www.moma.org/media/W1siZiIsIjQ5MzI0OCJdLFsicCIsImNvbnZlcnQiLCItcmVzaXplIDEwMjR4MTAyNFx1MDAzZSJdXQ.jpg?sha=1240179ade9097f2', 'Artist': 'Otto Wagner'}, {'Title': 'Armchair', 'Medium': 'Bent beechwood and aluminum', 'Dimensions': '30 7/8 x 22 1/4 x 20 1/4" (78.5 x 56.5 x 51.5 cm), seat h. 18 5/8" (47.3 cm)', 'CreditLine': 'Estée and Joseph Lauder Design Fund', 'Date': '1902', 'URL': 'https://www.moma.org/collection/works/4023', 'ImageURL': 'https://www.moma.org/media/W1siZiIsIjIyOTgzNyJdLFsicCIsImNvbnZlcnQiLCItcmVzaXplIDEwMjR4MTAyNFx1MDAzZSJdXQ.jpg?sha=022d146ca9d75fd8', 'Artist': 'Otto Wagner'}, {'Title': 'Ferdinandsbrücke Project, Vienna, Austria (Elevation, preliminary version)', 'Medium': 'Ink and cut-and-pasted painted pages on paper', 'Dimensions': '19 1/8 x 66 1/2" (48.6 x 168.9 cm)', 'CreditLine': 'Fractional and promised gift of Jo Carole and Ronald S. Lauder', 'Date': '1896', 'URL': 'https://www.moma.org/collection/works/2', 'ImageURL': 'https://www.moma.org/media/W1siZiIsIjUyNzc3MCJdLFsicCIsImNvbnZlcnQiLCItcmVzaXplIDEwMjR4MTAyNFx1MDAzZSJdXQ.jpg?sha=712ac0fd74ea5bd5', 'Artist': 'Otto Wagner'}, {'Title': 'Stool', 'Medium': 'Bent beechwood, molded plywood, and aluminum', 'Dimensions': '18 1/2 x 16 x 16" (47 x 40.6 x 40.6 cm)', 'CreditLine': 'Estée and Joseph Lauder Design Fund', 'Date': '1904', 'URL': 'https://www.moma.org/collection/works/4026', 'ImageURL': 'https://www.moma.org/media/W1siZiIsIjUyMDM2NyJdLFsicCIsImNvbnZlcnQiLCItcmVzaXplIDEwMjR4MTAyNFx1MDAzZSJdXQ.jpg?sha=d4986e9ca0b6dc4c', 'Artist': 'Otto Wagner'}]
    if wiki_qid and wiki_qid != "None":
        artist_details = fetch_wikidata_info(wiki_qid)  # Fetch artist details from Wikidata using the Wiki QID
        artist_details["wiki_qid"] = wiki_qid

    # Render the artist details page, passing the artist data
    return render_template("artist_details.html", artist_name=artist_name, artist=artist_details, artworks=artworks, total_artworks=len(artworks))


if __name__ == '__main__':
    app.run(port=5000, debug=True)
