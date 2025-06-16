import streamlit as st
import pickle

# ==================== 
# FUNCTION LOAD MODEL
# ====================
@st.cache_resource
def load_model():
    """Loads the trained CatBoost model."""
    try:
        with open('utils/trained_model.pkl', 'rb') as file:
            model = pickle.load(file)
        st.success("Model loaded successfully!")
        return model
    except FileNotFoundError:
        st.error("Error: 'trained_model.pkl' not found. Please ensure the trained model file is in the correct path.")
        st.stop()
    except Exception as e:
        st.error(f"Error loading model: {e}")
        st.stop()