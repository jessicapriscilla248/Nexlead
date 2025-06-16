import numpy as np
from catboost import Pool
import pickle
import streamlit as st

# ========================================================== 
# FUNCTION PROCESSING, PREDICT UNTUK DATA YANG BARU DIINPUT
# ==========================================================

# Membuat ketentuan apakah pegawai layak dipromosikan atau tidak
def promotionScore(row):
    score = 0

    # KPI mendapatkan lebih dari 80 dapat score +3 karena bisa dibilang sulit
    if row['KPIs_met_more_than_80'] == 1:
        score += 3

    # Awards pernah didapatkan +3 karena bisa dibilang sulit
    if row['awards_won'] == 1:
        score += 3

    # Previous Year Rating memiliki mean, yaitu 3. 
    # Sehingga 3 mendapatkan +1, lebih dari itu +2
    if row['previous_year_rating'] >= 4:
        score += 2
    elif row['previous_year_rating'] == 3:
        score += 1
    
    # Average Training Score memiliki mean 63. 
    # Sehingga >= 63 mendapatkan +1, >= 80 (jarang didapatkan pegawai) mendapatkan +2
    if row['avg_training_score'] >= 80:
        score += 2
    elif 63 <= row['avg_training_score'] < 80:
        score += 1
    
    # Length of Service 
    if row['length_of_service'] >= 5:
        score += 0.5
    
    # Number of Training
    if row['no_of_trainings'] > 1:
        score += 0.5

    return score

def promotion(row):
    if row['promotion_score'] >= 7:
        return 1
    else:
        return 0

# Preprocessing
def preprocessing(new_employee):
    # Hitung promotion score
    new_employee['promotion_score'] = new_employee.apply(promotionScore, axis=1)

    # Kategorikan training
    new_employee['training_category'] = np.where(
        new_employee['no_of_trainings'] == 1, 'Basic',
        np.where(
            new_employee['no_of_trainings'].isin([2,3]), 'Intermediate',
            np.where(
                new_employee['no_of_trainings'].isin([4,5]), 'Advanced',
                'Expert'
            )
        )
    ).astype(str)  

    new_employee['is_promoted'] = new_employee.apply(promotion, axis=1)

    # Apa saja yang menjadi kolom kategori
    categorical_features = ['department', 'region', 'education', 'gender', 'recruitment_channel', 'training_category']

    for col in categorical_features:
            new_employee[col] = new_employee[col].astype(str)
    return new_employee

# Prediction
def predict_promotion(new_employee, model):
    processed_data = preprocessing(new_employee.copy())
    categorical_features = ['department', 'region', 'education', 'gender', 'recruitment_channel', 'training_category']
    eval_pool = Pool(
        data=processed_data,
        cat_features=categorical_features,
        feature_names=list(processed_data.columns)
    )
    prediction = model.predict(eval_pool)[0]
    probability = model.predict_proba(eval_pool)[0]
    
    return prediction, probability, processed_data
