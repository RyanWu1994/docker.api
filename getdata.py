import json
import requests
import time
import pandas as pd

from fake_useragent import UserAgent
from sqlalchemy import create_engine
from collections import Counter


ua = UserAgent()
headers = {"User-Agent":ua.random}

def GetApi():

    url = "https://scapi.zanstartv.com/v1/pcnt/?appName=solar&Room="
    res = requests.get(url,headers=headers)
    api = json.loads(res.text)
    result = []
    localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    total = int(api["total"])
    result.append({"time": localtime,"total" : total})
    return result

def List_to_mysql(user,passwd,ip,db_name,table_name,result_list):

    engine = create_engine('mysql+mysqlconnector://'+ user +':'+ passwd +'@'+ip+'/'+ db_name +'?charset=utf8', encoding='utf-8')
    con = engine.connect() #建立連結
    
    for item in result_list:
        df = pd.DataFrame(item, index=[0])
        try:
            df.to_sql(name=table_name,con=con,if_exists='append',index=False) #假設table已存在 就自動往下加入data

        except Exception as e:
            if 'PRIMARY' in str(e):
                print("error")
                pass

    con.close() 
    engine.dispose()

user = "admin"
passwd = "Pn123456"
ip = "192.168.0.12:3306"
db_name = "Testdb"
table_name = "solartninc"

result_list = GetApi()
List_to_mysql(user,passwd,ip,db_name,table_name,result_list)

