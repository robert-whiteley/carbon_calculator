import pandas as pd
from google.cloud import bigquery
from carb_calc.params import *



def co2_query(text:str):
    #Creating a dict to change format
    libary = {'Apple Braeburn': 'APPLE','Cantaloupe 1': 'MELON','Grape Blue': 'GRAPES',
            'Mangostan': 'MANGO','Pear Monster': 'PEAR','Potato White': 'POTATO',
            'Apple Crimson Snow': 'APPLE','Cantaloupe 2': 'MELON','Grape Pink': 'GRAPES',
            'Maracuja': 'EXOTIC FRUIT','Pear Red': 'PEAR','Quince': 'PEAR',
            'Apple Golden 1': 'APPLE','Carambula': 'EXOTIC FRUIT','Grape White': 'GRAPES',
            'Melon Piel de Sapo': 'MELON','Pear Stone': 'PEAR','Rambutan': 'EXOTIC FRUIT',
            'Apple Golden 2': 'APPLE','Cauliflower': 'CAULIFLOWER','Grape White 2': 'GRAPES',
            'Mulberry': 'BLACKBERRY','Pear Williams': 'PEAR','Raspberry': 'RASPBERRY',
            'Apple Golden 3': 'APPLE','Cherry 1': 'CHERRY','Grape White 3': 'GRAPES',
            'Nectarine': 'PEACH','Pepino': 'MELON','Redcurrant': 'CURRANT',
            'Apple Granny Smith': 'APPLE','Cherry 2': 'CHERRY','Grape White 4': 'GRAPES',
            'Nectarine Flat': 'PEACH','Pepper Green': 'PEPPER','Salak': 'EXOTIC FRUIT',
            'Apple Pink Lady': 'APPLE','Cherry Rainier': 'CHERRY','Grapefruit Pink': 'ORANGE',
            'Nut Forest': 'MIXED NUTS','Pepper Orange': 'PEPPER','Strawberry': 'STRAWBERRY',
            'Apple Red 1': 'APPLE','Cherry Wax Black': 'CHERRY','Grapefruit White': 'ORANGE',
            'Nut Pecan': 'WALNUT','Pepper Red': 'PEPPER','Strawberry Wedge': 'STRAWBERRY',
            'Apple Red 2': 'APPLE','Cherry Wax Red': 'CHERRY','Guava': 'GUAVA','Onion Red': 'ONION',
            'Pepper Yellow': 'PEPPER','Tamarillo': 'TOMATO','Apple Red 3': 'APPLE',
            'Cherry Wax Yellow': 'CHERRY','Hazelnut': 'HAZELNUT','Onion Red Peeled': 'ONION',
            'Physalis': 'CHERRY','Tangelo': 'ORANGE','Apple Red Delicious': 'APPLE',
            'Chestnut': 'CHESTNUT','Huckleberry': 'BLUEBERRY','Onion White': 'ONION',
            'Physalis with Husk': 'CHERRY','Tomato 1': 'TOMATO','Apple Red Yellow 1': 'APPLE',
            'Clementine': 'CLEMENTINE','Kaki': 'EXOTIC FRUIT','Orange': 'ORANGE',
            'Pineapple': 'PINEAPPLE','Tomato 2': 'TOMATO','Apple Red Yellow 2': 'APPLE','Cocos': 'COCONUT',
            'Kiwi': 'KIWI','Papaya': 'EXOTIC FRUIT','Pineapple Mini': 'PINEAPPLE',
            'Tomato 3': 'TOMATO','Apricot': 'APRICOT','Corn': 'MAIZE','Kohlrabi': 'TURNIP',
            'Passion Fruit': 'EXOTIC FRUIT','Pitahaya Red': 'EXOTIC FRUIT','Tomato 4': 'TOMATO',
            'Avocado': 'AVOCADO','Corn Husk': 'MAIZE','Kumquats': 'CLEMENTINE',
            'Peach': 'PEACH','Plum': 'PLUM','Tomato Cherry Red': 'TOMATO',
            'Avocado ripe': 'AVOCADO','Cucumber Ripe': 'CUCUMBER','Lemon': 'LEMON',
            'Peach 2': 'PEACH','Plum 2': 'PLUM','Tomato Heart': 'TOMATO',
            'Banana': 'BANANA','Cucumber Ripe 2': 'CUCUMBER','Lemon Meyer': 'LEMON',
            'Peach Flat': 'PEACH','Plum 3': 'PLUM','Tomato Maroon': 'TOMATO',
            'Banana Lady Finger': 'BANANA','Dates': 'DATE','Limes': 'LIME',
            'Pear': 'PEAR','Pomegranate': 'POMEGRANATE','Tomato Yellow': 'TOMATO',
            'Banana Red': 'BANANA','Eggplant': 'EGGPLANT','Lychee': 'EXOTIC FRUIT',
            'Pear 2': 'PEAR','Pomelo Sweetie': 'LEMON','Tomato not Ripened': 'TOMATO',
            'Beetroot': 'BEETROOT','Fig': 'FIG','Mandarine': 'MANDARIN',
            'Pear Abate': 'PEAR','Potato Red': 'POTATO','Walnut': 'WALNUT',
            'Blueberry': 'BLUEBERRY','Ginger Root': 'GINGER','Mango': 'MANGO',
            'Pear Forelle': 'PEAR','Potato Red Washed': 'POTATO','Watermelon': 'WATERMELON',
            'Cactus fruit': 'EXOTIC FRUIT','Granadilla': 'EXOTIC FRUIT','Mango Red': 'MANGO',
            'Pear Kaiser': 'PEAR','Potato Sweet': 'POTATO',"Granny Smith":"APPLE",'Banana':'BANANA'}
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
