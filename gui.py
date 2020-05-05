from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')



#conda activate my_flask_env
#set FLASK_APP=gui.py
#-m flask run