from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import dummy_stock_market as dsm
from livereload import Server

last_close = dsm.last_close[0]
volume = dsm.volume[0]
current_price = dsm.current_price[0]
weeks52_data = dsm.weeks52_data

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():    
    return render_template('index.html', lastclose = last_close)

if __name__ == "__main__": 
    app.run(debug = True)
    server = Server(app.wsgi_app)
    server.serve()