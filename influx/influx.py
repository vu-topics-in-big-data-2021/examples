#Simple script which stores the random number generated into influxdb

import time
from influxdb.client import InfluxDBClientError
from influxdb import client as influxdb

def main():
        for i in range (0,100):
            lists = [{                           #Writing data into influxDB using json format
            'measurement':'random_number_generator',            #Measurement tells what data we are collecting
            'tags':{'data':'random_number'},
            'time':time.strftime('%Y-%m-%d %H:%M:%S'),
            'fields':{
                 'value':str(i)
                 },
            }]
            print(lists)
            mydb.write_points(lists)#eriting data into influx
            time.sleep(5)

if __name__=="__main__":
    #Setting up InfluxDB for data write
    mydb= influxdb.InfluxDBClient('127.0.0.1',8086,'rds','2018','random')#Config for the database
    mydb.create_database('random')#Creating the database
    retention_policy='awesome_policy'#Retention policy which can be custom made
    mydb.create_retention_policy('retention_policy','10d',10,default=True)#Here I store the data in my database for 10days, this can be changed
    main()
