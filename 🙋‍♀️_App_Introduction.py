import streamlit as st

# ===============
# INTRODUCTION 
# ==============
st.title("NEXLEAD")

st.markdown("""
    ### Welcome to the Promotion Employee Predictor!
    
    This app uses a trained CatBoost Classification model to predict whether an employee's `promotion_score` will be **Promoted** or **Not Promoted**,
    based on various operational factors.
    
    Use the sidebar to navigate to the 'Input Data' section to make a prediction, 
    'Results' to view previous prediction results, or '➕ New Prediction' to make a new prediction.
    
    **About Predictions:**
    This model classifies employees into two categories:
    - **Promoted (1)**: The employee has performed well or above the average performance of others. 
    - **Not promoted (0)**: Employee has a performance that is below the average performance of others.
    
    This can help in identifying employees who may need help in improving their skills, performance, and recognizing high performing employees.
""")
st.info("Dataset Source: [Employee Performance for HR Analytics](https://www.kaggle.com/datasets/sanjanchaudhari/employees-performance-for-hr-analytics )")

# Navbar
with st.sidebar:
    st.header("NEXLEAD")
    
    if st.button("➕ New Prediction"):
        st.session_state.single_prediction_result = None
        st.session_state.csv_prediction_df = None
        st.session_state.page = 'Input Data'
        
        # Ketika click langsung diarahkan ke page Input Data
        st.switch_page("pages/📋_Input_Data.py")
        st.rerun()
    
    st.markdown("---") 

