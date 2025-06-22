import streamlit as st
from langchain.chains import LLMChain
from langchain.tools import WikipediaQueryRun, BraveSearchRun
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import AzureChatOpenAI
import os
from dotenv import load_dotenv

# Set page config early
st.set_page_config(page_title="🔍 Book Info Lookup", layout="wide")

# Load API keys
load_dotenv()
AZURE_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_BASE = os.getenv("AZURE_OPENAI_API_BASE")
AZURE_VER = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_DEPLOY = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
BRAVE_API_KEY = os.getenv("BRAVE_SEARCH_API_KEY")  # Set this in .env

# Ensure login
if "user" not in st.session_state or not st.session_state["user"]:
    st.warning("🔐 Please log in to view book info.")
    st.stop()

st.title("🔍 Book Information Lookup")

query = st.text_input("Enter book title or title + author", placeholder="e.g. Harry Potter by J.K. Rowling")
if not st.button("Search"):
    st.stop()

if not query.strip():
    st.warning("Please enter a valid query.")
    st.stop()

# Initialize tools
wiki_tool = WikipediaQueryRun()
brave_tool = BraveSearchRun(api_key=BRAVE_API_KEY)

# Call Brave search for web results
brave_results = brave_tool.run(query + " book")
wiki_summary = None

# Call Wikipedia for summary
try:
    wiki_res = wiki_tool.run(query)
    wiki_summary = wiki_res["content"]
    wiki_url = wiki_res["url"]
except Exception:
    wiki_summary = None
    wiki_url = None

# Display results
cols = st.columns([1, 2])

with cols[0]:
    st.subheader("🌐 Web Results (Brave)")
    for item in brave_results[:5]:
        st.markdown(f"- [{item['title']}]({item['url']})")

with cols[1]:
    st.subheader("📚 Wikipedia Summary")
    if wiki_summary:
        st.write(wiki_summary)
        if wiki_url:
            st.markdown(f"[Read more on Wikipedia]({wiki_url})")
    else:
        st.write("No Wikipedia entry found.")

st.markdown("---")

# Use LLM to parse Brave results and suggest covers or next steps
llm = AzureChatOpenAI(
    openai_api_key=AZURE_KEY,
    openai_api_base=AZURE_BASE,
    openai_api_version=AZURE_VER,
    deployment_name=AZURE_DEPLOY,
    model_name="gpt-4o",
    temperature=0.7,
    max_tokens=10000,
    top_p=0.9,
)

prompt = PromptTemplate(
    input_variables=["query", "web_results", "wiki_summary"],
    template="""
We have a user search for a book: {query}

Brave search returned:
{web_results}

Wikipedia summary:
{wiki_summary}

Provide:
1. A short summary
2. Possible book cover URLs
3. A buy link or where to purchase
"""
)

chain = LLMChain(llm=llm, prompt=prompt)

with st.spinner("Analyzing and formatting results..."):
    resp = chain.invoke({
        "query": query,
        "web_results": "\n".join([f"{r['title']}: {r['url']}" for r in brave_results[:5]]),
        "wiki_summary": wiki_summary or "N/A"
    })

st.subheader("🤖 AI-Processed Info:")
st.markdown(resp["text"])
