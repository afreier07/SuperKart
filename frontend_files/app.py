
import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="SuperKart Sales Prediction",
    page_icon="🛒",
    layout="centered"
)

st.title("SuperKart Sales Prediction")
st.write("Enter the product and store information to predict sales.")

# Input fields
product_weight = st.number_input(
    "Product Weight",
    min_value=0.0,
    value=12.66
)

product_sugar_content = st.selectbox(
    "Product Sugar Content",
    ["Low Sugar", "Regular", "No Sugar"]
)

product_allocated_area = st.number_input(
    "Product Allocated Area",
    min_value=0.0,
    value=0.027,
    format="%.3f"
)

product_mrp = st.number_input(
    "Product MRP",
    min_value=0.0,
    value=117.08
)

store_size = st.selectbox(
    "Store Size",
    ["Small", "Medium", "High"]
)

store_location = st.selectbox(
    "Store Location City Type",
    ["Tier 1", "Tier 2", "Tier 3"]
)

store_type = st.selectbox(
    "Store Type",
    [
        "Departmental Store",
        "Supermarket Type1",
        "Supermarket Type2",
        "Food Mart"
    ]
)

product_id_char = st.selectbox(
    "Product ID Category",
    ["FD", "NC", "DR"]
)

store_age = st.number_input(
    "Store Age (Years)",
    min_value=0,
    value=16
)

product_type_category = st.selectbox(
    "Product Type Category",
    ["Perishables", "Non Perishables"]
)

if st.button("Predict Sales"):

    payload = {
        "Product_Weight": product_weight,
        "Product_Sugar_Content": product_sugar_content,
        "Product_Allocated_Area": product_allocated_area,
        "Product_MRP": product_mrp,
        "Store_Size": store_size,
        "Store_Location_City_Type": store_location,
        "Store_Type": store_type,
        "Product_Id_char": product_id_char,
        "Store_Age_Years": store_age,
        "Product_Type_Category": product_type_category
    }

    try:
        response = requests.post(
            "http://superkart-backend:5000/predict",
            json=payload
        )

        if response.status_code == 200:
            prediction = response.json()["prediction"]
            st.success(
                f"Predicted Product Store Sales: {prediction:,.2f}"
            )
        else:
            st.error(
                f"Prediction failed: {response.text}"
            )

    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to backend: {e}")

st.divider()
st.subheader("Batch Prediction")

uploaded_file = st.file_uploader(
    "Upload a CSV file for batch prediction",
    type=["csv"]
)

if uploaded_file is not None:
    batch_data = pd.read_csv(uploaded_file)

    st.write("Uploaded data:")
    st.dataframe(batch_data)

    if st.button("Predict Batch"):
        try:
            response = requests.post(
                "http://superkart-backend:5000/predict_batch",
                json=batch_data.to_dict(orient="records")
            )

            if response.status_code == 200:
                predictions = response.json()["predictions"]

                result = batch_data.copy()
                result["Predicted_Sales"] = predictions

                st.success("Batch prediction completed.")
                st.dataframe(result)

                st.download_button(
                    "Download Predictions",
                    data=result.to_csv(index=False).encode("utf-8"),
                    file_name="SuperKart_Batch_Predictions.csv",
                    mime="text/csv"
                )

            else:
                st.error(f"Batch prediction failed: {response.text}")

        except requests.exceptions.RequestException as e:
            st.error(f"Could not connect to backend: {e}")