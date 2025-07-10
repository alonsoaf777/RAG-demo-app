# 🍷 Wine Recommender RAG API — LLMOps Duke University

This project is part of the **Large Language Model Operations (LLMOps)** course at Duke University.  
It demonstrates a basic **RAG (Retrieval-Augmented Generation)** workflow to recommend wines using a **Llama** (or any OpenAI-compatible) model and a vector search engine (**Qdrant**).

---

## 📌 Description

**What does it do?**  
- It indexes wine tasting notes in a vector database and provides a **REST API** (built with **FastAPI**) to query semantic recommendations.

**Main workflow:**  
1. The user sends a query (e.g., *“I’m looking for a fruity and smooth wine.”*).  
2. The system performs **semantic search** on the indexed collection using embeddings (**SentenceTransformer**).  
3. The relevant results are combined with a **chatbot** powered by Llama/OpenAI to generate a contextual answer.

---

## Example of how tu run it

1. Download a Llama file from https://github.com/Mozilla-Ocho/llamafile?tab=readme-ov-file#other-example-llamafiles. 
2. In windows rename the file. Instead of .llama make it .exe and execute it using  "./{NAME OF YOUR FILE} --server" in PowerShell.
3. Once the model is loaded in your local adress (commonly http://127.0.0.1:8080) run in another PowerShell window "curl http://127.0.0.1:8080/v1/models" and write the id of the model in the .env file. 
4. Now run uvicorn main:app --reload in other PowerShell window to prepare the application with FastApi. 
5. For testing go to  http://127.0.0.1:8000/docs or the port selected in uvicorn. 

