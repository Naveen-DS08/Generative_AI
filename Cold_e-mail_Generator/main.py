import streamlit as st 
from chain import Chain
from portfolio import Portfolio
from utils import clean_text
from langchain_community.document_loaders import WebBaseLoader


# Creating UI for our app
def create_streamlit_app(llm, portfolio, clean_text):

    st.title("Cold Email Generator 📬")
    url = st.sidebar.text_input(label = "Enter your URL: ", placeholder="Job post URL")

    if st.sidebar.button("Submit"):
        try:
            loader = WebBaseLoader([url])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_email(job, links)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(page_title="Cold Email Generator", page_icon="📧", layout="wide")
    create_streamlit_app(llm=chain, portfolio=portfolio, clean_text=clean_text)

