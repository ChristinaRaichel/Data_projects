Twitter-airflow project

Python version: 3.10.6
Airflow version: 2.5.1


1. Create twitter api, generate keys, get json data and format it using tweepy and store it in csv using pandas
2. Create ec2 instance, and ssh to the running instance from local machine using key pair
3. install packages on EC2 machine

sudo apt-get update
sudo apt install python3-pip
sudo pip  install apache-airflow
sudo pip install pandas s3fs tweepy


sudo pip install s3fs
sudo pip install tweepy


4. Run airflow server
airflow standalone

4. Login to airflow using the url 'public dns :8080'
edit security grp inbound rules if not connecting

5. create s3 bucket 

6.edit airflow config

sudo nano airflow.cfg  --> twitter_dag (folder name)

mkdir twitter_dag # create folder 
	
sudo nano twitter_dag.py

restart server

7.edit IAM role of EC2 instance for s3 and ec2 full access


8. Trigger the DAG to run
