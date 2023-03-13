

1. create iam user and iam group in aws (Log in to aws n.virginia)
create iam credentials, access and secret keys

2.install aws cli on pc

curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

to check for installation, try :
aws --version
aws-cli/2.11.0 Python/3.11.2 Linux/5.15.0-60-generic exe/x86_64.ubuntu.22 prompt/off

aws configure #config iam user

3. copy data to s3 from pc (copy json files recursively and csv files in partitions)
aws s3 cp . s3://de-on-ytube-raw-useast1-dev/youtube/raw_data/ --recursive --exclude "*" --include "*.json"
"

aws s3 cp CAvideos.csv  s3://de-on-ytube-raw-useast1-dev/youtube/raw_data/reg=ca/
aws s3 cp FRvideos.csv  s3://de-on-ytube-raw-useast1-dev/youtube/raw_data/reg=fr/
aws s3 cp INvideos.csv  s3://de-on-ytube-raw-useast1-dev/youtube/raw_data/reg=in/
aws s3 cp KRvideos.csv  s3://de-on-ytube-raw-useast1-dev/youtube/raw_data/reg=kr/
aws s3 cp RUvideos.csv s3://de-on-ytube-raw-useast1-dev/youtube/raw_data/reg=ru/
aws s3 cp DEvideos.csv  s3://de-on-ytube-raw-useast1-dev/youtube/raw_data/reg=de/
aws s3 cp GBvideos.csv  s3://de-on-ytube-raw-useast1-dev/youtube/raw_data/reg=gb/
aws s3 cp JPvideos.csv  s3://de-on-ytube-raw-useast1-dev/youtube/raw_data/reg=jp/
aws s3 cp MXvideos.csv  s3://de-on-ytube-raw-useast1-dev/youtube/raw_data/reg=mx/
aws s3 cp USvideos.csv s3://de-on-ytube-raw-useast1-dev/youtube/raw_data/reg=us/

4.Crawl data on s3 to databases using glue
create a crawler
give iam role to crawler with glue use case--s3fullaccess,glueservicerole permissions
crawl data to a table(db) and view data on athena

5.To avoid the issue with parsing json files on glue crawler use lambda function
give role to lambda-s3 full access
provide python code, configure env variables, deploy and test with s3 put event-edit bucket and file names to be tested in script

tackling errors:
error:"Unable to import module 'lambda_function': No module named 'awswrangler'"
if awswrangler not supported by lambda, create a lambda layer
(*downgraded runtime config to py3.8 from 3.9, in n virginia only contains wrangler supporting layer)
awswrangler is renamed as pysdk currently

if timeout error (15min) occurs, increase timeout in general config

Give glue permission to lambda if error says, there is a permission denied.

"errorMessage": "An error occurred (EntityNotFoundException) when calling the CreateTable operation: Database db_youtube_cleaned not found.",
  
 finally, create db in glue, try lambda function,final op is saved as parquet in s3

6.Crawling csv files
create glue crawler with iam role and input db and s3, run it and find the table created
  
7.Using athena-
  view the partitioned table, perform qeuries, try joining the 2 tables already created
  
SELECT a.title, b.kind FROM "de-on-ytube-raw-db"."raw_statistics" a
inner join "db_youtube_cleaned "."cleaned_raw_data" b
on a.category_id = cast(b.id as int);

to increase code efficiency, edit cleaned_raw_data table schema id-column to bigint and remove cast in athena program

tackling error: HIVE_BAD_DATA: Field id's type BINARY in parquet file s3://de-on-ytube-raw-cleansed-useast1/youtube/8e54960b86a341a394dd81256956349c.snappy.parquet is incompatible with type bigint defined in table schema
This happens because, parquet file keeps the schema metadata in the headers that doesnot change by the last action we did
To avoid the error from generating:
1.keep the data type change in glue
2.delete the parq created from json file (from cleaned s3 bucket)
3.confirm append in lambda
4.run test event in lambda ----parq is created again ...now check running inner join in athena

7.Glue job to create spark script for csv to parq conversion
move csv files after cleaning(conv to parq) to the cleaned s3 bucket(where json cleaned files are already kept) using glue job
create glue job in legacy etl--py 3 spark 2.4-enable job bookmark  
edit data source, target(Create a table in the Data Catalog and on subsequent runs, update the schema and add new partitions-option)
mapping edit--change dtypes
get the sparkscript

edit the spark code to create partitions in the target bucket

additions to the code:

from awsglue.dynamicframe import DynamicFrame

datasink1 = dropnullfields3.toDF().coalesce(1)
df_final_output = DynamicFrame.fromDF(datasink1,glueContext,'df_final_output')

add ,"partitionKeys":["region"] to datasink0


run the job
tackling error: unable to parse
This occurs due to the data containing other speaking lang in file--chinese
data should be converted to utf..but we filter out unnecessary data using the following lines in the code:


predicate_pushdown = "reg in ('ca','gb','us')"
,push_down_predicate = predicate_pushdown (ds0)	


8.create glue crawler to crawl csvs from cleaned bucket to clean db in glue
9.creating lambda trigger

lambda:
apply fns to all files + inorder to process every new json file entering the raw bucket to parq--a trigger is to be added
rovide key , suffix(.json) in trigger,  delete all json filesin raw for testing,  copy the json files from pc to s3 using aws cli

10. making the reporting layer using glue studio
etl pipeline for queries that has to be run on routine
 
sample etl pipeline:
 SELECT * FROM "db_youtube_cleaned "."cleaned_raw_data" a
inner join "db_youtube_cleaned "."raw_statistics" b 
on a.category_id = b.id;"cleaned_raw_data" 

 In the glue studio  create glue data catalog sources, inner join transform, apply condition
 create analytics bucket, set it as target in glue studio--parq,snappy compression
 create db_analytics in athena, add it to target of glue stdio
 (create database db_youtube_analytics;)
 give a tabke name to create, add partition keys
 give iam role
 
10. Visualising using quicksight-std version
create accnt--add s3 buckets to be visible
add dataset from athena
create visualizations

https://us-east-1.quicksight.aws.amazon.com/sn/dashboards/c5f4106f-3ebc-467a-a5a4-73eabe7b7d9a

