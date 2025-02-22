#this file is used to run the app with Gunicorn
from app import app


if __name__ == "__main__":
    app.run(debug=True)