from .app import app
import json
from flask import Blueprint , render_template , request
# from flask import jsonify
import requests
# from src.database import DB
from .app.models.report_data_model import DailyReport

route = Blueprint('route', __name__)

def get_blueprint():
    """Return the blueprint for the main app module"""
    return route

@app.route('/')
@app.route('/test')
def index():
    url = "https://api.coronavirus.data.gov.uk/v1/data?filters=areaType=overview;"
    x = requests.get(url)
    xJson = json.loads(x.text)
    # DB.insert(xJson[0])
    # list = []
    # for i in xJson:
    #     report = DailyReport(i)
    #     print(report.toString())
    #     list.append(report.toString())

    # print(xJson[0]["new_case"])
    # return json.dumps(list)
    return xJson
