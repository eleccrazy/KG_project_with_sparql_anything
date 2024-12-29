from flask import Flask, request, render_template
import requests # Import the requests library to send and receive HTTP requests
from app.logic.query import query_artist_by_name

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
    artist_details = None
    if wiki_qid:
        # Placeholder artist details for demonstration purposes
        artist_details = {
            "name": "Vincent van Gogh",
            "artist_bio": "Vincent Willem van Gogh was a Dutch post-impressionist painter who is among the most famous and influential figures in the history of Western art.",
            "nationality": "Dutch",
        }

    # Render the artist details page, passing the artist data
    return render_template("artist_details.html", artist=artist_details)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
