import joblib
import pandas as pd
model_young_gr=joblib.load("artifacts/model_young_gr.joblib")
model_rest_gr=joblib.load("artifacts/model_rest_gr.joblib")
scaler_young_gr=joblib.load("artifacts/scaler_young_gr.joblib")
scaler_rest_gr=joblib.load("artifacts/scaler_rest_gr.joblib")

def handle_scaling(age,df):
    if age<25:
        scaler_object=scaler_young_gr
    else:
        scaler_object=scaler_rest_gr
    cols_toscale=scaler_object["cols_to_scale"]  
    scaler=scaler_object["scaler"] 
    df[cols_toscale]=scaler.transform(df[cols_toscale])
    return df
def preprocess_input(input_dict):
    # store input in the form of dataframe
    """
    Index(['age', 'region', 'number_of_dependants', 'bmi_category', 'income_lakhs',
       'insurance_plan', 'genetical_risk', 'total_risk_score', 'gender_Male',
       'smoking_status_Occasional', 'smoking_status_Regular',
       'employment_status_Salaried', 'employment_status_Self-Employed'],
      dtype='object')
    """
    df_columns=[
        "age",
    "region",
    "number_of_dependants",
    "bmi_category",
    "income_lakhs",
    "insurance_plan",
    "genetical_risk",
    "total_risk_score",
    "gender_Male",
    'smoking_status_Occasional',
      'smoking_status_Regular',
'employment_status_Salaried', 
'employment_status_Self-Employed'
    
    ]

    df=pd.DataFrame(0,columns=df_columns,index=[0])
    # numerical data storing in the input dataframe
    df["age"]=input_dict["age"]
    df["number_of_dependants"]=input_dict["number_of_dependants"]
    df["income_lakhs"]=input_dict["income_lakhs"]
    df["genetical_risk"]=input_dict["genetical_risk"]
    df["total_risk_score"]=input_dict["total_risk_score"]
    
    # storing categorical data in the input dataframe

    # convert categorical data into numerical data 
    region_encoded={'Northwest':1, 'Southeast':2, 'Northeast':0, 'Southwest':4}
    bmi_category_encoded={'Normal':0, 'Obesity':1, 'Overweight':2, 'Underweight':3}
    insurance_plan_encoded={'Bronze':0, 'Silver':1, 'Gold':2}
    



    df["region"]=region_encoded.get(input_dict["region"],0)
    df["bmi_category"]=bmi_category_encoded.get(input_dict["bmi_category"],0)
    df["insurance_plan"]=insurance_plan_encoded.get(input_dict["insurance_plan"],0)
    
    if input_dict["gender"]=="Male":
        df["gender_Male"]=1
    if input_dict["smoking_status"]=="Occasional":
        df["smoking_status_Occasional"]=1
    if input_dict["smoking_status"]=="Regular": 
        df["smoking_status_Regular"]=1
    if input_dict["employment_status"]=="Salaried": 
        df["employment_status_Salaried"]=1
    if input_dict["employment_status"]=="Self-Employed":
        df["employment_status_Self-Employed"]=1   

    df=handle_scaling(input_dict["age"],df) 
    return df          
   

def predict(input_dict):
    processed_data=preprocess_input(input_dict)
    if input_dict["age"]<25:
        print(processed_data)
        print(type(processed_data))
        print(processed_data.shape)
        final_premium=model_young_gr.predict(processed_data)
    else:
        final_premium=model_rest_gr.predict(processed_data)
    return final_premium        