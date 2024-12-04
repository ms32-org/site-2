from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Vercel! This is a basic Flask app."

if __name__ == '__main__':
    app.run(debug=True)
