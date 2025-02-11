#this is cold email generation tool
import os

import streamlit as st   # Importing Streamlit for creating the web-based UI.
from langchain_community.document_loaders import WebBaseLoader # Importing WebBaseLoader to load web page content.


from chains import Chain  # Importing the Chain class from the chains module.
from portfolio import Portfolio  # Importing the Portfolio class from the portfolio module.
from utils import clean_text  # Importing the clean_text function from the utils module.


def create_streamlit_app(llm, portfolio, clean_text):
    """
        Function to create the Streamlit web app for generating cold emails.
        :param llm: Instance of the Chain class for job extraction and email generation.
        :param portfolio: Instance of the Portfolio class to fetch portfolio links.
        :param clean_text: Function to clean and preprocess the extracted text.
    """
    st.title("📧 Cold Mail Generator")  # Setting the title of the Streamlit app.

    # Input field for the user to enter a job posting URL.
    url_input = st.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-47078?from=job%20search%20funnel")

    # Button to trigger processing of the entered URL.
    submit_button = st.button("Submit")

    if submit_button: # When the button is clicked
        try:
            loader = WebBaseLoader([url_input])  # Creating an instance of WebBaseLoader to load web page content.

            # Loading the webpage content, cleaning it, and extracting raw text.
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio() # Loading portfolio data for querying links.
            jobs = llm.extract_jobs(data) # Extracting job details from the cleaned text.

            for job in jobs: # Iterating over each extracted job.
                skills = job.get('skills', []) # Extracting required skills from the job description.
                if not skills:   # If no skills are found, display an error and exit.
                    st.error("No skills found in job posting, unable to retrieve portfolio links.")
                    return
                links = portfolio.query_links(skills) # Querying portfolio links related to the skills.
                email = llm.write_mail(job, links) # Generating a cold email using the extracted job details and links.
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")  # Displaying the error message in the UI.

#The program starts here
if __name__ == "__main__":
    # os.system("streamlit run " + __file__)
    chain = Chain()  # Creating an instance of the Chain class for processing job descriptions and generating emails.
    portfolio = Portfolio() # Creating an instance of the Portfolio class to manage portfolio links.

    # Configuring the Streamlit app with a wide layout, custom page title, and an email icon.
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)# Calling the function to launch the Streamlit app.

