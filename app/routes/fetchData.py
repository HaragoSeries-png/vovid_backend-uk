from flask import Blueprint
import requests
import json
from flask_mongoengine import MongoEngine


daily_report = Blueprint('daily_report', __name__)
db = MongoEngine()

@daily_report.route('/s')
def show():
    url = "https://api.coronavirus.data.gov.uk/v1/data"
    x = requests.get(url)
    xJson = json.loads(x.content)
    data = xJson["data"][0]
    report = Daily_report2(date = data["date"],death=10,deathNew=50)
    report.save()
    return report.toJson()


class Daily_report2(db.Document):

   report_id = db.IntField()
   date = db.StringField()
   deathNew = db.IntField()
   death = db.IntField()


   def toJson(self):
      return {
         "date":self.date,
         "death":self.death,
         "deathNew":self.deathNew
      }
