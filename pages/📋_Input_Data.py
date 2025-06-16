import streamlit as st
import pandas as pd
import numpy as np
from utils.function import predict_promotion
from utils.model import load_model

if 'single_prediction_result' not in st.session_state:
    st.session_state.single_prediction_result = None
if 'csv_prediction_df' not in st.session_state:
    st.session_state.csv_prediction_df = None
if 'csv_view_index' not in st.session_state:
    st.session_state.csv_view_index = 0

# Navbar
with st.sidebar:
    st.header("NEXLEAD")  
    if st.button("➕ New Prediction"):
        st.session_state.single_prediction_result = None
        st.session_state.csv_prediction_df = None
        st.session_state.page = 'Input Data'
        st.switch_page("pages/📋_Input_Data.py")
        st.rerun()
    
    st.markdown("---") 
    
# ================
# INPUT DATA PAGE
# ================
st.title("📥 Input Data for Prediction")
model = load_model()

st.markdown("""
    Please provide the necessary data points below to get a promotion prediction.
    You can either enter data manually for a single prediction or upload a CSV file for predictions.
""")
st.subheader("Dataset Column Information")
st.markdown("""
    Here's a breakdown of the columns in the dataset used for this prediction model:

        1. Employee ID: Unique identifier for each employee 
        2. Department: Categorization of employees into different departments 
        3. Region: Geographical region of employee's work location
        4. Education: Employee's educational background
        5. Gender: Distribution of employees by gender
        6. Recruitment Channel: Source through which employees were recruited
        7. Number of Trainings: Count of training programs attended by each employee
        8. Age: Age of employees
        9. Previous Year Rating: Performance rating of employees from the previous year
        10. Length of Service: Duration of employment with the company
        11. Award Won: Employees have won awards from the office
        12. KPI Above 80%: Employees achieve predetermined targets of 80% and above.
""")

if 'single_prediction_result' not in st.session_state:
    st.session_state.single_prediction_result = None
if 'csv_prediction_df' not in st.session_state:
    st.session_state.csv_prediction_df = None

tab1, tab2 = st.tabs(['Enter Individual Data', 'Upload CSV File'])

# Kondisi user input data manual (satu per satu)
with tab1:
    st.subheader("Enter Individual Data")
    col1, col2 = st.columns(2)
    
    with col1:
        department = st.selectbox("Department", ['Sales & Marketing', 'Operations', 'Procurement', 'Analytics', 'Finance', 'HR', 'Technology', 'Legal', 'R&D'])
        region = st.selectbox("Region", [f'region_{i}' for i in range(1, 35)])
        education = st.selectbox("Education", ["Below Secondary", "Bachelors", "Masters & Above"])
        gender = st.radio("Gender", ['female', 'male'])
        if gender == 'female':
            gender = 'f'
        else:
            gender = 'm'
        recruitment_channel = st.selectbox("Recruitment Channel", ['sourcing', 'referred', 'other'])
        no_of_trainings = st.slider("Number of Trainings", 1, 10, 2)
        
    with col2:
        age = st.slider("Age", 18, 60, 20)
        previous_year_rating = st.slider("Previous Year Rating", 1.0, 5.0, 3.0, 0.5)
        length_of_service = st.slider("Length of Service (years)", 1, 15, 5)
        KPIs_met = st.radio("KPIs Met >80%", [0, 1], format_func=lambda x: 'Yes' if x else 'No')
        awards_won = st.radio("Awards Won", [0, 1], format_func=lambda x: 'Yes' if x else 'No')
        avg_training_score = st.slider("Average Training Score", 0, 100, 75)
    
    # Membuat data frame
    if st.button("Predict Promotion"):
        input_data = pd.DataFrame({
            'department': [department],
            'region': [region],
            'education': [education],
            'gender': [gender],
            'recruitment_channel': [recruitment_channel],
            'no_of_trainings': [no_of_trainings],
            'age': [age],
            'previous_year_rating': [previous_year_rating],
            'length_of_service': [length_of_service],
            'KPIs_met_more_than_80': [KPIs_met],
            'awards_won': [awards_won],
            'avg_training_score': [avg_training_score]
        })
        
        # Melakukan prediksi
        try:
            prediction, probability, processed_data = predict_promotion(input_data, model)
            if prediction ==1 :
                prediction_label = "RECOMMENDED for Promotion"
            else:
                prediction_label = 'NOT RECOMMENDED for Promotion'
            
            st.session_state.single_prediction_result = {
                'input_data': input_data,
                'processed_data': processed_data,
                'prediction_label': prediction_label,
                'probability': probability,
                'prediction': prediction
            }
            st.success("Prediction completed!")
            st.switch_page("pages/📊_Results.py")

        # Peringatan untuk cek model ketika mengalami error
        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")
            st.write("Please check your input values and ensure the model is correctly loaded.")

# Kondisi user input file CSV
with tab2:
    st.subheader("Upload CSV File")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            # Menampilkan 5 kolom pertama dari file
            fileCSV = pd.read_csv(uploaded_file)
            st.write("First 5 columns of uploaded data :")
            st.dataframe(fileCSV.head())
            
            # Melakukan prediksi dan user dapat memantau proses prediksi dengan progress bar
            if st.button("Predict Promotions for Uploaded CSV"):
                predictions = []
                probabilityy = []
                progress_bar = st.progress(0)
                
                for i, row in fileCSV.iterrows():
                    input_data = pd.DataFrame([row])
                    prediction, probability, _ = predict_promotion(input_data, model)
                    predictions.append(prediction)
                    probabilityy.append(probability.tolist())
                    progress_bar.progress((i + 1) / len(fileCSV))
                
                fileCSV['prediction'] = predictions
                fileCSV['probability_not_promoted'] = [p[0] for p in probabilityy]
                fileCSV['probability_promoted'] = [p[1] for p in probabilityy]
                fileCSV['prediction_label'] = np.where(
                    fileCSV['prediction'] == 1,
                    "RECOMMENDED for Promotion",
                    "NOT RECOMMENDED for Promotion"
                )
                
                st.session_state.csv_prediction_df = fileCSV
                st.session_state.csv_view_index = 0
                st.success("Prediction completed!")
                st.switch_page("pages/📊_Results.py")
        
        # Peringatan untuk cek model ketika mengalami error      
        except Exception as e:
            st.error(f"An error occurred while processing the CSV file: {e}")
            st.write("Please ensure the CSV file has the correct columns and format.")
