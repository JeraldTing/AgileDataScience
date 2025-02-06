import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import seaborn as sns

# Streamlit page config
st.set_page_config(page_title="Sales Prediction Dashboard", page_icon="📊", layout="wide")

# Load dataset function
@st.cache_data
def load_data():
    return pd.read_csv('data/sales_data_sample.csv', encoding='latin1')

# Load the data
df = load_data()

# Rename columns to more readable names
df = df.rename(columns={
    'QUANTITYORDERED': 'Ordered Quantity',
    'PRICEEACH': 'Price for Each',
    'ORDERLINENUMBER': 'Order Line No'
})

# Ensure 'Ordered Quantity' and 'Order Line No' are integers
df['Ordered Quantity'] = df['Ordered Quantity'].astype(int)
df['Order Line No'] = df['Order Line No'].astype(int)

# Sidebar Filters
st.sidebar.header("Filter Data")
selected_product = st.sidebar.selectbox("Product", df['PRODUCTLINE'].unique())
selected_country = st.sidebar.selectbox("Country", df['COUNTRY'].unique())
selected_quarter = st.sidebar.selectbox("Quarter", df['QTR_ID'].unique())

# Apply Filters
filtered_df = df[
    (df['PRODUCTLINE'] == selected_product) &
    (df['COUNTRY'] == selected_country) &
    (df['QTR_ID'] == selected_quarter)
]

# Select features and target variable (excluding "Order Line No")
features = ['Ordered Quantity', 'Price for Each']
target = 'SALES'

X = filtered_df[features]
y = filtered_df[target]

# Train Random Forest Regressor model
if len(filtered_df) > 1:
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Make predictions
    y_pred = model.predict(X)

    # Calculate regression metrics
    r2 = r2_score(y, y_pred)
    adjusted_r2 = 1 - (1 - r2) * (len(y) - 1) / (len(y) - X.shape[1] - 1)
    sse = np.sum((y - y_pred) ** 2)

    # Display all performance metrics and feature importances in one row
    st.subheader("Random Forest Model Metrics and Feature Importance")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric('R-squared', f'{r2:.4f}')
    col2.metric('Adjusted R-squared', f'{adjusted_r2:.4f}')
    col3.metric('SSE', f'{sse:.2f}')
    col4.metric('Ordered Quantity Feature Importance', f'{model.feature_importances_[0]:.4f}')
    col5.metric('Price for Each Feature Importance', f'{model.feature_importances_[1]:.4f}')

    # Visualization: Actual vs. Predicted Sales and Residual Plot side by side (balanced scale)
    st.subheader("Model Visualizations")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))  # Balanced size for both charts

    # Actual vs Predicted Sales Plot (smaller but balanced)
    ax1.scatter(y, y_pred, alpha=0.5)
    ax1.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', lw=2)  # Line of best fit
    ax1.set_xlabel("Actual Sales")
    ax1.set_ylabel("Predicted Sales")
    ax1.set_title("Actual vs. Predicted Sales")

    # Residual Plot (balanced size)
    residuals = y - y_pred
    sns.histplot(residuals, bins=30, kde=True, ax=ax2)
    ax2.set_title("Residual Distribution")
    ax2.set_xlabel("Residuals")

    st.pyplot(fig)

    # Prediction form
    st.sidebar.header("Make a Prediction")
    input_values = []
    for feature in features:
        input_values.append(st.sidebar.number_input(f"Enter {feature}", value=int(filtered_df[feature].mean())))

    if st.sidebar.button("Predict Sales"):
        input_array = np.array(input_values).reshape(1, -1)
        predicted_sales = model.predict(input_array)[0]

        # Display predicted sales value next to the dashboard title
        st.markdown(f"### Predicted Sales: ${predicted_sales:,.2f}")
        st.sidebar.success(f"Predicted Sales: ${predicted_sales:,.2f}")

    st.sidebar.write("Adjust the inputs above and click 'Predict Sales' to get an estimated sales value.")

    st.write("This model uses Random Forest Regressor to predict sales based on order details.")
else:
    st.warning("Not enough data for selected filters. Please adjust the filter options.")