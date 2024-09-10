import logging
from app import create_app

app=create_app()



if __name__ == '__main__':
    logging.basicConfig(filename='flask_app.log', level=logging.DEBUG)
    app.run(debug=True)