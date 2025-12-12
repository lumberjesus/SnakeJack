"""Command to run the web server."""
from snakejack.web import app

def main():
    """Run the web server."""
    app.run(debug=True, host="0.0.0.0", port=5000)

if __name__ == "__main__":
    main()