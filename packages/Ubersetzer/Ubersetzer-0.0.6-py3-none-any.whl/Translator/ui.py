from urllib import request
from flask import *

app = Flask(__name__)
from translator import eng_deu
t = eng_deu()
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=[ "GET","POST"])
def translate():
    if request.method == "POST":
        sent = request.form.get('sent')
        m = {'res': t.translate(sent)}
        return render_template('result.html',m=m)
