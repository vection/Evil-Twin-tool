# Defence against evil twin attack

import requests
from requests.auth import HTTPBasicAuth
import json
from http.client import HTTPSConnection
from base64 import b64encode
import mysql.connector as mariadb
import urllib3
sql_host = 'root@localhost'

class Database():
     def __init__(self, table="Registered_APs"): 
          self.db = mariadb.connect(user='aviv', password='a',host='localhost', database='aps')
          self.connection = self.db.cursor()
          self.connection.execute("CREATE DATABASE IF NOT EXISTS aps")
          self.connection.execute("USE aps")
          self.table = table
          self.create_table()

     def create_table(self):
          sql = "CREATE TABLE IF NOT EXISTS %s (`MAC` VARCHAR(255), PRIMARY KEY (MAC));" % self.table
          self.connection.execute(sql) 

     def insert_mac(self,mac):
          sql = "INSERT INTO "+self.table+" VALUES ('%s');" % mac
          print(sql)
          self.connection.execute(sql)
          self.db.commit()

     def get_mac(self,mac):
          final_result = []
          sql = "SELECT * FROM "+self.table
          val = self.table
          self.connection.execute(sql)
          result = self.connection.fetchall()
          for x in result:
              if x[0] == mac:
                 return True
          return False
     
     def show_all_mac(self):
          final_result = []
          sql = "SELECT * FROM "+self.table
          val = self.table
          self.connection.execute(sql)
          result = self.connection.fetchall()
          for x in result:
              final_result.append(x[0])

          return final_result

if __name__ == "__main__":
    #connection()
    datab = Database()
    print(type(datab))
    print("Completed!")

