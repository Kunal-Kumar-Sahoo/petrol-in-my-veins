import streamlit as st
import plotly.express as px
import requests
import os

# Set up the Streamlit app title
st.title("Real-time Plotly Dashboard")

# Create a sidebar for user input
st.sidebar.header("Navigation")

# Add routing options in the sidebar
selected_page = st.sidebar.selectbox("Select Page", ["Dashboard", "About", "Contact"])

# Get the API endpoint from the environment variable
api_endpoint = 'http://localhost:5000/analysis'

# Define a function to fetch data from the API
def fetch_data_from_api():
    if api_endpoint:
        try:
            response = requests.get(api_endpoint)
            if response.status_code == 200:
                return response.json()
            else:
                st.error("Failed to fetch data from the API.")
                return None
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
            return None
    else:
        st.error("API_ENDPOINT environment variable is not set.")
        return None

# Define functions for different pages
def render_dashboard():
    st.header("Real-time Dashboard")

    # Create a plot placeholder
    plot_placeholder = st.empty()

    while True:
        # Fetch data from the API
        api_data = fetch_data_from_api()

        if api_data:
            selected_data = st.selectbox("Select Data", list(api_data.keys()))
            data = api_data[selected_data]
            title = selected_data

            fig = px.line(x=list(range(len(data))), y=data, title=title)
            
            # Update the plot in real-time
            plot_placeholder.plotly_chart(fig)
            
            st.header("Data Summary")
            st.write(f"Selected Data: {selected_data}")
            st.write(f"Mean of {selected_data}: {sum(data) / len(data)}")

def render_about():
    st.header("About")
    # Add content for the About page here
    st.write("This is the about page. Add information about your app here.")

def render_contact():
    st.header("Contact")
    # Add content for the Contact page here
    st.write("This is the contact page. You can provide contact information here.")

# Based on user selection, render the corresponding page
if selected_page == "Dashboard":
    render_dashboard()
elif selected_page == "About":
    render_about()
elif selected_page == "Contact":
    render_contact()
