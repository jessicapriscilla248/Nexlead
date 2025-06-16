import streamlit as st

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
    
# ==============
# RESULTS PAGE
# ==============
if 'single_prediction_result' not in st.session_state:
    st.session_state.single_prediction_result = None
if 'csv_prediction_df' not in st.session_state:
    st.session_state.csv_prediction_df = None
if 'csv_view_index' not in st.session_state:
    st.session_state.csv_view_index = 0

st.title("Employee Promotion Prediction Results")

# Kalau user input data dengan manual 
if st.session_state.single_prediction_result:
    tab1, tab2 = st.tabs(['Prediction', 'Recommendation'])

    # Hasil dari prediction dan detail dari employee 
    with tab1:
        result = st.session_state.single_prediction_result
        input_data = result['input_data']
        processed_data = result['processed_data']
        
        st.subheader("Prediction Result")
        if result['prediction_label'] == "RECOMMENDED for Promotion":
            st.success(f"Prediction: **{result['prediction_label']}**")
            st.success(f"Reliability: {result['probability'][1]*100:.1f}%")
        else:
            st.warning(f"Prediction: **{result['prediction_label']}**")
            st.warning(f"Reliability: {result['probability'][0]*100:.1f}%")
        
        st.subheader("Employee Details")
        st.dataframe(input_data)
    
    # Rekomendasi untuk HR dan data yang sudah di processed
    with tab2:
        st.subheader("Recommendations")
        with st.expander("Click to see HR recommendations"):
            if result['prediction_label'] == "RECOMMENDED for Promotion":
                st.success("This employee is recommended for promotion. Suggestion:")
                st.markdown("- Give appreciation for good performance")
                st.markdown("- Assign new responsibilities to develop potential")
                if input_data.get('previous_year_rating', [0])[0] < 4.0:
                    st.markdown("- Note: Rating below 4.0, consider additional training for upcoming responsibilities.")
            else:
                st.warning("This employee is not recommended for promotion. Suggestion:")
                st.markdown("- Identify and address performance barriers")
                st.markdown("- Provide additional training and guidance")
                if input_data['KPIs_met_more_than_80'].iloc[0] == 0:    
                    st.markdown("- Encourage achievement of KPIs in future evaluations.")
        
        st.subheader("Processed Data Used for Prediction")
        st.dataframe(processed_data)

# Kalau user input data pakai CSV
if st.session_state.csv_prediction_df is not None:
    st.subheader("CSV Prediction Results")
    fileCSV = st.session_state.csv_prediction_df
    
    # Hasil prediksi untuk keseluruhan
    st.write(f"Total Employees: {len(fileCSV)}")
    st.write(f"RECOMMENDED for Promotion     : {len(fileCSV[fileCSV['prediction'] == 1])}")
    st.write(f"NOT RECOMMENDED for Promotion : {len(fileCSV[fileCSV['prediction'] == 0])}")
    
    # Detailed employee
    st.subheader("Detailed Employee")
    if 'csv_view_index' not in st.session_state:
        st.session_state.csv_view_index = 0
    current_index = st.session_state.csv_view_index
    total_rows = len(fileCSV)
    
    # Detail satu per satu employee
    employee = fileCSV.iloc[current_index]
    
    st.write("**Employee Details:**")
    st.write(f"Department: {employee['department']}")
    st.write(f"Region: {employee['region']}")
    st.write(f"Previous Year Rating: {employee['previous_year_rating']}")
    
    st.write("**Prediction:**")
    if employee['prediction_label'] == 1:
        st.success(f"{employee['prediction_label']} (Reliability: {employee['probability_promoted']*100:.1f}%)")
    else:
        st.warning(f"{employee['prediction_label']} (Reliability: {employee['probability_not_promoted']*100:.1f}%)")

    # Navigasi untuk back dan next melihat employee detail
    col1, col2, col3 = st.columns([2, 2, 5])
    with col1:
        if st.button("⬅️ Previous") and current_index > 0:
            st.session_state.csv_view_index -= 1
            st.rerun()
    with col2:
        if st.button("Next ➡️") and current_index < total_rows - 1:
            st.session_state.csv_view_index += 1
            st.rerun()
    with col3:
        st.write(f"Viewing employee {current_index + 1} of {total_rows}")
    
    # Download file yang sudah ada label prediksi
    csv = fileCSV.to_csv(index=False).encode('utf-8')
    st.download_button(
        "Download Full Results as CSV",
        csv,
        "employee_promotion_predictions.csv",
        "text/csv"
    )

# Kondisi belum input data
if st.session_state.single_prediction_result is None and st.session_state.csv_prediction_df is None:
    st.info("No predictions have been made yet. Please go to the 'Input Data' section.")
    st.page_link("pages/📋_Input_Data.py", label="Go to Input Data →")
