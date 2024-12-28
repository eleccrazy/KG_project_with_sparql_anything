from flask import Flask, request, render_template
import requests  # Assuming you're using this to make HTTP requests for your SPARQL query, etc.

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    # Initialize the results variable
    results = None
    
    if request.method == 'POST':
        # Get the user input from the form
        object_name = request.form.get('object_name')
        # Here we can run the sparql anything query based on the object_name
        results = f"Results for: {object_name}"  # Replace this with actual query logic
        
    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
