import pandas as pd
from google.cloud import bigquery
from carb_calc.params import *



def co2_query(text:str):
    #Creating a dict to change format
    libary = {"orange":"ORANGE","banana":"BANANA","Granny Smith":"APPLE"}
    query = f"""
        SELECT *
        FROM {GCP_PROJECT}.{BQ_DATASET}.{TABLE}
        WHERE Food_commodity_ITEM LIKE "{libary[text]}%" AND FOOD_COMMODITY_GROUP = "CROPS"
        ORDER BY Carbon_Footprint_kg_CO2eq_kg_or_l_of_food_ITEM
    """
    client = bigquery.Client(project=GCP_PROJECT)
    query_job = client.query(query)
    result = query_job.result()
    df = result.to_dataframe()
    co2 = df.iloc[-1,-1]
    out = {text:co2}
    #Returning a Dict with the input text and the crabon value.
    #eg {orange:0.3}
    return out


if __name__ == '__main__':
    co2_query('orange')
    co2_query('banana')
    co2_query('Granny Smith')
