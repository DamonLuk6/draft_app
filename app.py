from flask import Flask, render_template, url_for, request, flash
import pandas as pd
from forms import TierForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'e6958684b626fad00305cd8a24d73b9d'

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


@app.route("/tier", methods = ['GET', 'POST'])
def tier():
    form = TierForm()
    if form.validate_on_submit():
        flash('Tier cutoffs submitted', 'success')
        tier_cutoff = {
            "Man/Boy": {"tier_1": form.mmpOneCutOff.data, "tier_2": form.mmpTwoCutOff.data},
            "Woman/Girl": {"tier_1": form.wmpOneCutOff.data, "tier_2": form.wmpTwoCutOff.data}
        }
        print(tier_cutoff)

    return render_template('tier.html', title = 'Tiers', form = form)

@app.route("/draftsheet")
def draftsheet():
    return render_template("draft-sheet.html", title = 'Draft Sheet')

@app.route("/draftboard")
def draftboard():
    return render_template("draft-board.html", title = "Draft Board")

if __name__ == "__main__":
    app.run(debug=True)