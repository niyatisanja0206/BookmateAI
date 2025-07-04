import streamlit as st
from langchain_community.chat_models import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from duckduckgo_search import DDGS
import wikipedia
from dotenv import load_dotenv
import os

# Load env vars
load_dotenv()
api_key = os.getenv("AZURE_OPENAI_API_KEY")
api_base = os.getenv("AZURE_OPENAI_API_BASE")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")

# Page setup
st.set_page_config(page_title="Bookmate AI", layout="wide", page_icon="📚")
st.markdown("<h1 style='text-align: center;'>📚 Bookmate AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #34495e;'>A personalized reading guide for book lovers</p>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("🎯 Book Preferences")
    genre = st.selectbox("Choose Genre/type", ["Poetry", "Mythology", "Fiction", "Non-Fiction", "Mystery", "Science Fiction", "Fantasy", "Romance", "Thriller", "Biography", "Self-Help", "History", "Children's", "Young Adult", "Graphic Novel", "Classic Literature", "Horror", "Adventure", "Philosophy", "Religion", "Cookbook", "Travel", "Health & Wellness", "Business", "Politics", "True Crime", "Comics", "Art & Photography", "Science", "Technology", "Sports", "Music", "Drama", "Poetry Anthology", "Western", "Dystopian", "Satire", "Urban Fiction", "Historical Fiction", "Literary Fiction", "Magical Realism", "Chick Lit", "New Adult", "Inspirational", "Spirituality", "Environmental", "Cultural Studies", "Anthropology", "Psychology"])  # Keep your full genre list here
    language = st.selectbox("Choose Language", ["English", "Hindi", "Gujarati", "Urdu", "Bangali", "French", "Spanish", "German", "Italian"])
    author = st.text_input("Author's name")
    get_recommend = st.button("Recommend Books")

# Initialize LLM chain
@st.cache_resource
def init_chain():
    llm = AzureChatOpenAI(
        openai_api_base=api_base,
        openai_api_version=api_version,
        openai_api_key=api_key,
        deployment_name=deployment_name,
        model_name="gpt-4o",
        temperature=0.8,
        max_tokens=1500,
    )
    prompt = PromptTemplate(
        input_variables=["genre", "language", "author"],
        template="""
Recommend 10 top books based on:
- Genre: {genre}
- Language: {language}
- Author: {author}

For each book, give:
1. A brief (2-4 sentence) summary.
2. A buy/download link of  book if possible.
        """
    )
    return LLMChain(llm=llm, prompt=prompt)

llmchain = init_chain()

# Recommendations
if get_recommend:
    with st.spinner("✨ Finding the perfect books for you..."):
        response = llmchain.invoke({
            "genre": genre,
            "language": language,
            "author": author
        })
        st.subheader("🔖 Top Picks Just for You")
        st.markdown(response["text"])

# --- Book Info Section ---
st.markdown("---")
st.subheader("🔍 Book Info Lookup")
search_query = st.text_input("Enter a book name to search about it", placeholder="e.g. 'Sapiens by Yuval Noah Harari'")
search_btn = st.button("🔎 Search Now")

# Fallback LLM for book description
@st.cache_resource
def init_fallback_chain():
    llm = AzureChatOpenAI(
        openai_api_base=api_base,
        openai_api_version=api_version,
        openai_api_key=api_key,
        deployment_name=deployment_name,
        model_name="gpt-4o",
        temperature=0.7,
        max_tokens=800,
    )
    prompt = PromptTemplate(
        input_variables=["query", "summary", "link"],
        template="""
        The user is looking for information about a book. 

        Book title: {query}
        Available Summary: {summary}
        Buy Link: {link}

        Write only:
        A concise summary of the book (10-15 sentences).
        Include a buy link .

        Avoid any details not related to the book.
        """
    )
    return LLMChain(llm=llm, prompt=prompt)

fallback_chain = init_fallback_chain()

if search_btn and search_query.strip():
    book_summary, buy_link, book_image = "", "", None

    # Fetch summary from Wikipedia
    try:
        book_summary = wikipedia.summary(search_query + " book", sentences=5, auto_suggest=True, redirect=True)
    except:
        book_summary = ""

    # DuckDuckGo fetch for buy link and cover
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(
                f"{search_query} site:amazon.com OR site:barnesandnoble.com OR site:bookdepository.com",
                max_results=5
            ))
            images = list(ddgs.images(search_query + " book cover", max_results=1))

            # Find first strong marketplace link
            if results:
                for r in results:
                    href = r["href"].lower()
                    if any(domain in href for domain in ["amazon.com", "barnesandnoble.com", "bookdepository.com"]):
                        buy_link = r["href"]
                        break
                if not buy_link:
                    buy_link = results[0]["href"]

            if images:
                book_image = images[0]["image"]
    except:
        pass

    # LLm fallback (same as before)
    with st.spinner("🔎 Finding book details..."):
        llm_response = fallback_chain.run({
            "query": search_query,
            "summary": book_summary or "None",
            "link": buy_link or "None"
        })

    st.markdown("## 📖 Book Summary")
    if book_image:
        st.image(book_image, width=160)
    st.write(llm_response)

#footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #34495e;'>Made by Niyati</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #34495e;'>Powered by <a href='https://openai.com/' target='_blank'>OpenAI</a> and <a href='https://langchain.com/' target='_blank'>LangChain</a></p>", unsafe_allow_html=True)

