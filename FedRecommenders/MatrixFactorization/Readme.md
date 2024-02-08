EDA_data_processing.ipynb
-Contains EDA, data cleaning codes and final data is converted to an np array (reduced_data_np)
-Run EDA_data_processing.ipynb to generate reduced_data_np

Data_to_csv.ipynb
-Converts the np array obtained in previous step, to train,test,validation data sets and writes them as csv files in data/bookcrossings
-Run Data_to_csv.ipynb to generate the csv files


# For outputs:
run main.ipynb to generate the recommender ndcg and hr values.
main.ipynb integrates model training and evaluation

