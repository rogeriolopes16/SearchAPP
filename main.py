from flask import Flask
from waitress import serve

app = Flask(__name__)
app.config.from_pyfile('modules/config.py')

from modules.views import *

if __name__ == '__main__':
    app.run(debug=True)
    serve(app, host='127.0.0.1', port=5000)
    #serve(app, host='172.33.6.147', port=5050)