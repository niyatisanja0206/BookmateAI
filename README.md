# 📚 Bookmate AI

An AI-powered personalized book recommendation and lookup app that suggests books tailored to your reading preferences and fetches information about any book using **Wikipedia**, **DuckDuckGo**, and **GPT-4o (Azure OpenAI)**. Built using **Streamlit**, **LangChain**, and **Azure GPT-4o**.

## 🚀 Features

- 🧠 AI-based book recommendation using:
  - Genre
  - Language
  - Favorite Author
- 📖 Search any book by name or name + author to get:
  - Summary
  - Book cover
  - Buy link (Amazon/Barnes & Noble/etc.)
- 🎯 Personalized suggestions using Azure GPT-4o via LangChain
- 🌐 Results powered by DuckDuckGo and Wikipedia
- 📥 Simple and intuitive Streamlit UI
- 🔐 Secure key management with `.env` support

## 🧰 Tech Stack

- Python 3.8+
- Streamlit
- LangChain
- Azure OpenAI (GPT-4o)
- DuckDuckGo Search (`duckduckgo-search`)
- Wikipedia API (`wikipedia`)
- `python-dotenv` for environment management

## 🛠️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/bookmate-ai.git
cd bookmate-ai
```

### 2. Create and Activate Virtual Environment

#### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### Mac/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create a `.env` File in Project Root

```dotenv
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_API_BASE=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
AZURE_OPENAI_API_VERSION=2024-05-01-preview
```

### 5. Run the App

```bash
streamlit run app.py
```

## 🚧 Future Enhancements

- ✅ User login/signup with reading list management
- 📦 Firebase/Supabase integration to store preferences
- 📖 Book previews using Google Books/Open Library API
- 📚 Genre-based trending books

## 🤝 Contributing

Pull requests are welcome! For major changes, open an issue first to discuss what you’d like to change.

## 📄 License

MIT License. Use, modify, and distribute freely.
