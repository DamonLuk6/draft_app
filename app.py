#luk

from flask import Flask, render_template, url_for, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from forms import TierForm
from draft_sheet import generateDraftSheet

app = Flask(__name__)

app.config['SECRET_KEY'] = 'e6958684b626fad00305cd8a24d73b9d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

tier_cutoff = {
    "Man/Boy": {"tier_1": 0, "tier_2": 0},
    "Woman/Girl": {"tier_1": 0, "tier_2": 0}
}

class Tiers(db.Model):
    gender = db.Column(db.String, unique = True, primary_key = True, nullable = False)
    tier_1 = db.Column(db.Integer)
    tier_2 = db.Column(db.Integer)

    def __repr__(self):
        return f"gender: {self.gender}, tier 1: {self.tier_1}, tier 2: {self.tier_2}"
    


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
        flash('Manual adjustments saved!', 'success')
        
        return redirect(url_for('tier'))
    
    return render_template("scoring-sheet.html", title = 'Scoring Sheet', players = players, columns = columns)


@app.route("/tier", methods = ['GET', 'POST'])
def tier():
    df = pd.DataFrame()
    form = TierForm()
    if form.validate_on_submit():
        flash('Tier cutoffs saved!', 'success')
        #tier_cutoff = {
        #    "Man/Boy": {"tier_1": form.mmpOneCutOff.data, "tier_2": form.mmpTwoCutOff.data},
        #    "Woman/Girl": {"tier_1": form.wmpOneCutOff.data, "tier_2": form.wmpTwoCutOff.data}
        #}

        t_men = Tiers(gender = "Man/Boy", tier_1 = form.mmpOneCutOff.data, tier_2 = form.mmpTwoCutOff.data)
        t_women = Tiers(gender = "Woman/Girl", tier_1 = form.wmpOneCutOff.data, tier_2 = form.wmpTwoCutOff.data)
        db.session.add(t_men)
        db.session.add(t_women)
        db.commit()



    df = generateDraftSheet(tier_cutoff)
    df['rank by gender'] = df['rank by gender'].astype(int)
    df = df[['Name', 'rank by gender', 'gender_id', 'tier', 'final rating']].sort_values(by = ['tier', 'gender_id', 'final rating'], ascending = [True, True, False])

    players = df.to_dict('records')
    columns = df.columns.tolist()

    return render_template('tier.html', title = 'Tiers', form = form, players = players, columns = columns)

@app.route("/draftsheet")
def draftsheet():
    df = generateDraftSheet(tier_cutoff)
    players = df.to_dict('records')
    columns = df.columns.tolist()

    return render_template("draft-sheet.html", title = 'Draft Sheet', players = players, columns = columns)

@app.route("/draftboard")
def draftboard():
    return render_template("draft-board.html", title = "Draft Board")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        
    app.run(debug=True)