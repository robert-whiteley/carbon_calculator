import pandas as pd
from google.cloud import bigquery
from carb_calc.params import *



def co2_query(text:str):
    libary = {"orange":"ORANGE","banana":"BANANA","Granny Smith":"APPLE"}
    query = f"""
        SELECT *
        FROM {GCP_PROJECT}.{BQ_DATASET}.{TABLE}
        WHERE Food_commodity_ITEM LIKE "{libary[text]}%" AND FOOD_COMMODITY_GROUP = "CROPS"
    """
    client = bigquery.Client(project=GCP_PROJECT)
    query_job = client.query(query)
    result = query_job.result()
    df = result.to_dataframe()
    print(df)
    return df


if __name__ == '__main__':
    co2_query('orange')
    co2_query('banana')
    co2_query('Granny Smith')
