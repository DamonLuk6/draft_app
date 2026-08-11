from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route("/scoring")
def scoring():
    df = pd.read_csv("data/scoring.csv")
    return render_template(
        "scoring.html",
        players=df.to_dict("records"),
        columns=df.columns.tolist()   # <-- send the column names too
    )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)