from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def dashboard():
    # Beispiel-Daten für Kampagnen
    campaigns = ["Kampagne 1", "Kampagne 2", "Kampagne 3"]
    return render_template('dashboard.html', campaigns=campaigns)

if __name__ == '__main__':
    app.run(debug=True)
