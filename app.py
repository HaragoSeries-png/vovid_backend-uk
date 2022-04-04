from email.policy import default
import os
from requests import get
import json
from flask import Flask, make_response ,request
from flask_mongoengine import MongoEngine
from flask_apscheduler import APScheduler
from datetime import date,datetime,timedelta
from flask_cors import CORS

project_root = os.path.dirname(__file__)
app = Flask(__name__)
CORS(app)

database_name = "vovid-uk"
DB_URI = "mongodb+srv://chanon:132231@cluster0.broqy.mongodb.net/vovid-uk?authSource=admin&replicaSet=Cluster0-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true"
app.config["MONGODB_HOST"] = DB_URI
db = MongoEngine()
db.init_app(app)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

@app.route("/daily",methods=['POST'])
def dailyFunc():
   args = request.args
   initer = args.get("opt", default='', type=str)
   structure = '{"date":"date","newCases":"newCasesByPublishDate","location":"areaName","totalCase":"cumCasesByPublishDate","newDeath":"newDeathsByDeathDate","totalDeath":"cumDeathsByDeathDate"}'
   today = date.today()

   today_date = today.isoformat()

   curr_date = today
   query_date = curr_date.isoformat()
   # find last date
   

   if initer=="start":
      temp_date = today-timedelta(days=30)
      url = "https://api.coronavirus.data.gov.uk/v1/data?filters=areaType=nation;date>"+temp_date.isoformat()+"&structure="+structure
   else:
      while True:

         if Daily_report.objects(date= curr_date.isoformat()):
            query_date = curr_date.isoformat()
            # print("currdate is : "+query_date)
            break
         curr_date = curr_date-timedelta(days=1)
      url = "https://api.coronavirus.data.gov.uk/v1/data?filters=areaType=nation;date>"+query_date+"&structure="+structure
   response = get(url)
   if not response.text:
      print("nodata")
      return "empty"
   jsonText = json.loads(response.text)["data"]

   # jsonText = jsonText["data"] 
   recent_date = jsonText[0]["date"]



   if Daily_report.objects(date= recent_date):
      print("alredy update")
      print("end daily fuc")
      return "end"
   for i in range(len(jsonText)):
      content = jsonText[i]
      # print(content)
      report  = Daily_report(
         date = content["date"],
         newCase = content["newCases"],
         totalCase = content["totalCase"],
         newDeath = content["newDeath"],
         death = content["totalDeath"],
         location = content["location"]
      )
      report.save()
   return json.dumps(jsonText)

@app.route("/api/weekly-cases",methods=['get'])
def todayCases2():
   today = date.today()
   curr_date = today-timedelta(days=1)
   date_arr = []
   exc_field = ["id","created_at"]
   data_arr = []
  
   while len(date_arr)<7:
      today_date = curr_date.isoformat()
      date_arr.append(today_date)      
      qData = Daily_report.objects(date=today_date).exclude(*exc_field).order_by("location").to_json()
      reData ={"date":today_date,"result":json.loads(qData)}
      curr_date = curr_date-timedelta(days=1)   
      data_arr.append(reData)

   return json.dumps(data_arr)

@app.route("/api/cases",methods=['get'])
def Cases2():
   args = request.args
   
   today = date.today()
   yesterday = today-timedelta(days=1) 
   qdate = args.get("date", default=yesterday.isoformat(), type=str)

   exc_field = ["id","created_at"]
   data_arr = []
  
     
   qData = Daily_report.objects(date=qdate).exclude(*exc_field).order_by("location").to_json()
   reData ={"date":qdate,"result":json.loads(qData)}  
   data_arr.append(reData)

   return json.dumps(data_arr)

class Daily_report(db.Document):

   date = db.StringField()
   newCase = db.IntField(default=0)
   totalCase = db.IntField(default=0)
   newDeath = db.IntField(default=0)
   death = db.IntField(default=0)
   location = db.StringField()
   created_at = db.DateTimeField(default=datetime.now)


   def toJson(self):
      return {
         "date":self.date,
         "death":self.death,
         "deathNew":self.deathNew
      }


if __name__ == "__main__":
   app.run()
   print("hoho")
