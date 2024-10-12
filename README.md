# Querious by Elliot Hong

Querious is a local-based RAG (retrieval-augmented generation) LLM (large language model), or a chatbot, that uses your input pdfs and answers queries regarding them.

# SETUP:
1. Clone this repository
2. Add pdf files of your choice to the "data" folder
3. Run in terminal:

a. Install streamlit globally
```
pip3 install streamlit
```

b. Install a local virtual environment
```
pip3 install virtualenv
virtualenv venv
```

c. Run the virtual environment. For macOS/Linux:
```
source venv/bin/activate
```

For Windows:
```
.\venv\Scripts\activate
```

d. Install remaining dependencies:
```
pip3 install -r requirements.txt
```

***NOTE***: to deactivate virtual environment, simply run:
```
deactivate
```

# To Run:
1. In your project directory, run the following to populate your database:
```
streamlit run populate_database.py
```
2. Then in the same directory, run the app:
```
streamlit run ollama-streamlit-app.py
```

# Sources/Inspiration
* https://medium.com/@maximejabarian/building-a-local-llms-app-with-streamlit-and-ollama-llama3-phi3-511d519c95fe
* https://www.youtube.com/watch?v=2TJxpyO3ei4