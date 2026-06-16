import streamlit as st
import pandas as pd
import joblib
import numpy as np

# ========================== Page Configuration ==========================
st.set_page_config(
    page_title="Laptop Price Predictor",
    # page_icon="💻",
    layout="centered"
)

# ========================== Custom CSS ==========================
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        background-color: #1E88E5;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        height: 3em;
        width: 100%;
    }
    .stButton>button:hover { background-color: #1565C0; }
    h1 { color: #1E88E5; margin-bottom: 0.2em; }
    .success-box {
        background-color: #E8F5E9;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
    }
    </style>
""", unsafe_allow_html=True)

# ========================== Load Model ==========================
@st.cache_resource
def load_model():
    try:
        model = joblib.load('laptop_price_model.pkl')
        return model
    except FileNotFoundError:
        st.error("❌ Model file 'laptop_price_model.pkl' not found!")
        st.stop()

model = load_model()

# ========================== Header with Small Image on Left ==========================
col_img, col_title = st.columns([1, 3])  # 1:3 ratio → small image on left

with col_img:
    st.image("imge.jpeg", 
             use_container_width=True, 
             caption="")

with col_title:
    st.markdown("<h1> Laptop Price Predictor</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #555;'>Accurate price estimation powered by Machine Learning</p>", unsafe_allow_html=True)

# ========================== Sidebar Inputs ==========================
st.sidebar.header("📋 Laptop Specifications")

def reset_inputs():
    st.rerun()

col1, col2 = st.columns(2)

with col1:
    company = st.selectbox("Company", ['Apple', 'HP', 'Dell', 'Lenovo', 'Asus', 'Acer', 'MSI', 'Toshiba', 'Samsung', 'Razer', 'Huawei', 'Microsoft', 'Chuwi'])
    typename = st.selectbox("Type", ['Notebook', 'Ultrabook', 'Gaming', '2 in 1 Convertible', 'Workstation', 'Netbook'])
    inches = st.slider("Screen Size (Inches)", 10.0, 18.4, 15.6, 0.1)
    ram = st.selectbox("RAM (GB)", [4, 6, 8, 12, 16, 32, 64])
    weight = st.slider("Weight (kg)", 0.5, 5.0, 2.0, 0.1)

with col2:
    opsys = st.selectbox("Operating System", ['Windows 10', 'macOS', 'No OS', 'Linux', 'Windows 7', 'Mac OS X', 'Windows 10 S', 'Chrome OS', 'Android'])
    cpu_brand = st.selectbox("CPU Brand", ['Intel', 'AMD'])
    cpu_speed = st.slider("CPU Speed (GHz)", 1.0, 3.5, 2.5, 0.1)
    resolution = st.selectbox("Screen Resolution", ['1366x768', '1920x1080', '2560x1600', '2880x1800', '3200x1800', '3840x2160', '1440x900'])
    storage_ssd = st.radio("Storage Type", ["SSD", "HDD/Flash"], horizontal=True)
    storage_ssd_val = 1 if storage_ssd == "SSD" else 0

# ========================== Action Buttons ==========================
col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    predict_btn = st.button("🔮 Predict Price", type="primary", use_container_width=True)

with col_btn2:
    st.button("🔄 Reset", on_click=reset_inputs)

# ========================== Prediction ==========================
if predict_btn:
    try:
        width, height = map(int, resolution.split('x'))
    except:
        width, height = 1920, 1080

    input_data = pd.DataFrame({
        'Company': [company], 'TypeName': [typename], 'Inches': [inches],
        'OpSys': [opsys], 'Ram_GB': [ram], 'Weight_kg': [weight],
        'Cpu_Brand': [cpu_brand], 'Cpu_Speed_GHz': [cpu_speed],
        'Screen_Width': [width], 'Screen_Height': [height],
        'Screen_Area': [width * height], 'Storage_Type': [storage_ssd_val]
    })

    prediction = model.predict(input_data)[0]

    st.markdown(f"""
        <div class="success-box">
            <h2>Estimated Price: €{prediction:,.2f}</h2>
            <p><strong>Realistic Market Range:</strong> €{int(prediction*0.85):,} – €{int(prediction*1.15):,}</p>
        </div>
    """, unsafe_allow_html=True)

    # Feature Importance
    st.subheader("🔍 Top Features Influencing This Prediction")
    if hasattr(model.named_steps['model'], 'feature_importances_'):
        importances = model.named_steps['model'].feature_importances_
        feature_names = model.named_steps['preprocessor'].get_feature_names_out()
        feat_imp = pd.Series(importances, index=feature_names).sort_values(ascending=False).head(8)
        st.bar_chart(feat_imp)
        st.caption("Longer bars = stronger influence on price")

# Footer
st.markdown("---")
# st.markdown("**Made with ❤️ using Streamlit + Scikit-learn**")
# st.caption("Model trained on real laptop market data")