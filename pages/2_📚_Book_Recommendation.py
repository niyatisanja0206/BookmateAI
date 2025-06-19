import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.chat_models import AzureChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="📚 Book Recommender", layout="wide")

if "user" not in st.session_state or not st.session_state["user"]:
    st.warning("Please log in first.")
    st.stop()

st.title("📚 Book Recommendation Engine")

genre = st.selectbox("Choose Genre", ["Fiction", "Sci-Fi", "Mystery", "Romance", "Non-fiction", "Fantasy", "Biography"])
language = st.selectbox("Preferred Language", ["English", "Hindi", "French", "Spanish", "German"])
author = st.text_input("Favorite Author")
get_recommend = st.button("🎯 Recommend Books")

@st.cache_resource
def init_chain():
    llm = AzureChatOpenAI(
        openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        openai_api_base=os.getenv("AZURE_OPENAI_API_BASE"),
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        model_name="gpt-4o"
    )

    prompt = PromptTemplate(
        input_variables=["genre", "language", "author"],
        template="""
Suggest 5 books in {language} in the genre of {genre}.
Try to include recommendations by or similar to {author}, if specified.
Include a short summary and where to buy them online with short cover image URLs.
"""
    )
    return LLMChain(llm=llm, prompt=prompt)

llm_chain = init_chain()

if get_recommend:
    with st.spinner("Finding the perfect books..."):
        result = llm_chain.invoke({
            "genre": genre,
            "language": language,
            "author": author,
        })
        st.markdown(result["text"])
