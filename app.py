from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/scoring")
def scoring():
    df = pd.read_csv("data/scoring.csv")
    return render_template("scoring-sheet.html", title = 'Scoring Sheet')

@app.route("/draftsheet")
def draftsheet():
    return render_template("draft-sheet.html", title = 'Draft Sheet')

@app.route("/draftboard")
def draftboard():
    return render_template("draft-board.html", title = "Draft Board")

if __name__ == "__main__":
    app.run(debug=True)