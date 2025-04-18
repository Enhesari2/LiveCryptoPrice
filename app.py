from flask import Flask
app = Flask(__name__)

@app.route('/ping')
def ping():
    return "I'm alive!"

app.run(host='0.0.0.0', port=8080)
