from sklearn.externals import joblib
import pandas as pd
from flask import Flask, jsonify
from flask import request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
@app.route("/getWinProbablity_LR", methods=["POST"])
def calculateProbability():
    data = request.get_json()
    print(data)
    team1 = data['myTeam']
    team2 = data['opponentTeam']
    filename = 'finalized_model.sav'
    loaded_model = joblib.load(filename)
    df = pd.DataFrame([[int(team1[0]),int(team1[1]),int(team1[2]),int(team1[3]),int(team1[4]),int(team2[0]),int(team2[1]),int(team2[2]),int(team2[3]),int(team2[4])]],
                      columns=['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10'])
    result = {
        "result":  loaded_model.predict_proba(df)[0][1] * 100
    }

    return jsonify(
        result
    )

@app.route("/getWinProbablity_RF", methods=["POST"])
def calculateProbability_rf():
    data = request.get_json()
    print(data)
    team1 = data['myTeam']
    team2 = data['opponentTeam']
    filename = 'finalized_model_rf.sav'
    loaded_model = joblib.load(filename)
    df = pd.DataFrame([[int(team1[0]),int(team1[1]),int(team1[2]),int(team1[3]),int(team1[4]),int(team2[0]),int(team2[1]),int(team2[2]),int(team2[3]),int(team2[4])]],
                      columns=['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10'])
    result = {
        "result":  loaded_model.predict_proba(df)[0][1] * 100
    }

    return jsonify(
        result
    )
if __name__ == '__main__':
    app.run()