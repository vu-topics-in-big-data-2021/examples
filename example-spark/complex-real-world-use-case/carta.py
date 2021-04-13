from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import UserDefinedFunction,isnan, when, count, col, isnull,month, hour,year,minute,second
from pyspark.sql.types import TimestampType, DateType
from pyspark.sql import DataFrame
from functools import reduce
import glob
import dateparser

spark = SparkSession.builder.master("spark://localhost:7077").appName("carta_data_prep").getOrCreate()
sqlContext = SQLContext(spark.sparkContext)
sc=spark.sparkContext("carta-raw-data/*.TXT.bz2")
dflist=[]

#we read a number of files and for each file infer schema, join and prepare the data
for file in listfiles:
    print("reading "+file)
    dftemp=sqlContext.read.csv(file,inferSchema=True, header=True)
    dftemp=dftemp.dropDuplicates(['TRIP_KEY','SURVEY_DATE','ROUTE_NUMBER','DIRECTION_NAME','STOP_ID','SORT_ORDER'])
    dflist.append(dftemp)

# join all data frame
df = reduce(DataFrame.unionAll, dflist)

def convertdate(x):
    try:
        out=dateparser.parse(str(x).split(" ")[0])
        return out
    except:
        return None
def convertstamp(x):
    try:
        out=dateparser.parse(str(x).split(" ")[1])
        return out
    except:
        return None

#user defined functions are cool for making data conversions
converttimeudf = UserDefinedFunction(lambda x: convertstamp(x), TimestampType())
convertdateudf = UserDefinedFunction(lambda x: convertdate(x), TimestampType())


#with column allows to introduce a new column keeping others in place.
df3=df.withColumn("TIME_SCHEDULED", converttimeudf(df['TIME_SCHEDULED']))\
    .withColumn("TRIP_START_TIME", converttimeudf(df['TRIP_START_TIME']))\
    .withColumn("TIME_ACTUAL_ARRIVE", converttimeudf(df['TIME_ACTUAL_ARRIVE']))\
    .withColumn("TIME_ACTUAL_DEPART", converttimeudf(df['TIME_ACTUAL_DEPART']))\
    .withColumn("SURVEY_DATE",convertdateudf(df["SURVEY_DATE"]).cast(DateType()))

df4=df3.withColumn("MONTH",month(df3["SURVEY_DATE"]))\
    .withColumn("YEAR",year(df3["SURVEY_DATE"]))\
    .withColumn("TIME_SCHEDULED_HOUR",hour(df3["TIME_SCHEDULED"]))\
    .withColumn("TIME_SCHEDULED_MIN",minute(df3["TIME_SCHEDULED"]))\
    .withColumn("TIME_SCHEDULED_SEC",second(df3["TIME_SCHEDULED"]))\
    .withColumn("TRIP_START_TIME_HOUR",hour(df3["TRIP_START_TIME"]))\
    .withColumn("TRIP_START_TIME_MIN",minute(df3["TRIP_START_TIME"]))\
    .withColumn("TRIP_START_TIME_SEC",second(df3["TRIP_START_TIME"]))\
    .withColumn("TIME_ACTUAL_ARRIVE_HOUR",hour(df3["TIME_ACTUAL_ARRIVE"]))\
    .withColumn("TIME_ACTUAL_ARRIVE_MIN",minute(df3["TIME_ACTUAL_ARRIVE"]))\
    .withColumn("TIME_ACTUAL_ARRIVE_SEC",second(df3["TIME_ACTUAL_ARRIVE"]))\
    .withColumn("TIME_ACTUAL_DEPART_HOUR",hour(df3["TIME_ACTUAL_DEPART"]))\
    .withColumn("TIME_ACTUAL_DEPART_MIN",minute(df3["TIME_ACTUAL_DEPART"]))\
    .withColumn("TIME_ACTUAL_DEPART_SEC",second(df3["TIME_ACTUAL_DEPART"]))

df5=df4.withColumn('DIRECTION_NAME',when(df4.DIRECTION_NAME=="OUTYBOUND" ,"OUTBOUND")\
    .when(df4.DIRECTION_NAME=="0" ,"OUTBOUND")\
        .when(df4.DIRECTION_NAME=="1" ,"INBOUND")\
            .otherwise(df4.DIRECTION_NAME))

#we should drop columns that we do not need to use.
columns_to_drop = ['TIME_ACTUAL_ARRIVE', 'TRIP_START_TIME','TIME_SCHEDULED','TIME_ACTUAL_DEPART','CHECKER_NAME']
df5 = df5.drop(*columns_to_drop)

statistics=df5.groupBy("YEAR","MONTH",'ROUTE_NUMBER','ROUTE_NAME',"DIRECTION_NAME","STOP_ID","TIME_ACTUAL_ARRIVE_HOUR","TRIP_KEY").count().sort(col("count").desc())

#write the output as compressed parquets. Note we repartition to reduce the number of final files.
df5.repartition(2)\
  .write\
        .option("mapreduce.fileoutputcommitter.algorithm.version", "2")\
        .partitionBy("YEAR","MONTH","ROUTE_NUMBER")\
        .mode("append")\
        .format("parquet")\
        .save("/Users/abhishek/spark/carta/processed")

statistics.repartition(1).write.format("csv").option("header","true").save("/Users/abhishek/spark/combinedcartastatistics.csv")