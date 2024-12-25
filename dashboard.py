import pandas as pd
import streamlit as st

# Function to load the processed data
@st.cache_data
def load_data(filepath="data/processed_dataset.csv"):
    """
    Loads the processed dataset.

    Args:
        filepath (str): Path to the processed dataset.

    Returns:
        pd.DataFrame: Loaded data.
    """
    try:
        data = pd.read_csv(filepath)
        return data
    except FileNotFoundError:
        st.error("Processed dataset not found. Please run the processing script first.")
        return pd.DataFrame()

# Main function to run the Streamlit app
def main():
    st.title("Stakeholder Dashboard")
    st.write("This dashboard displays the processed data and allows stakeholders to filter and search the records.")

    # Load the processed data
    data = load_data()
    if data.empty:
        st.warning("No data to display. Please ensure the dataset is processed and available.")
        return

    # Display the full dataset
    st.subheader("Full Dataset")
    st.dataframe(data)

    # Search functionality
    st.subheader("Search Functionality")
    search_term = st.text_input("Search by any field (e.g., age, cholesterol):")
    if search_term:
        filtered_data = data[data.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
        st.write(f"Search Results for '{search_term}':")
        st.dataframe(filtered_data)

    # Filter functionality
    st.subheader("Filter Functionality")
    age_range = st.slider("Select Age Range", min_value=int(data["age"].min()), max_value=int(data["age"].max()), value=(30, 60))
    filtered_by_age = data[(data["age"] >= age_range[0]) & (data["age"] <= age_range[1])]
    st.write(f"Data for Age Range: {age_range[0]} to {age_range[1]}")
    st.dataframe(filtered_by_age)

# Entry point for the Streamlit app
if __name__ == "__main__":
    main() 