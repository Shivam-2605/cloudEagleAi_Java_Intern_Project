import os
from flask import Flask, render_template
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask
# Flask automatically looks for HTML files in the 'templates' folder 
# and CSS/JS in the 'static' folder relative to this file.
app = Flask(__name__)

@app.route("/")
def index():
    """
    Serves the main dashboard HTML file.
    The actual data fetching is done client-side by app.js.
    """
    return render_template("index.html")

if __name__ == "__main__":
    # Pull the port from .env, defaulting to 5000
    port = int(os.getenv("FLASK_PORT", 5000))
    
    print(f"Starting Flask frontend server on http://localhost:{port}")
    
    # Run the Flask app
    app.run(host="0.0.0.0", port=port, debug=True)