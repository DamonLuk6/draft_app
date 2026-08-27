from flask import Flask, render_template, url_for, request
import pandas as pd

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/scoring", methods = ['GET', 'POST'])
def scoring():
    df = pd.read_csv("data/scoring.csv")
    df['manual adjustment'] = df['manual adjustment'].astype(float)
    players = df.to_dict("records")
    columns = df.columns.tolist()

    if request.method == "POST":
        for key, value in request.form.items():
                print(key)
                df.loc[df['USAU_member_id'].astype(str) == key, 'manual adjustment'] = float(value)
        df.to_csv("data/scoring.csv", index=False)

    return render_template("scoring-sheet.html", title = 'Scoring Sheet', players = players, columns = columns)

@app.route("/draftsheet")
def draftsheet():
    return render_template("draft-sheet.html", title = 'Draft Sheet')

@app.route("/draftboard")
def draftboard():
    return render_template("draft-board.html", title = "Draft Board")

if __name__ == "__main__":
    app.run(debug=True)