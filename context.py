import pandas as pd
from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer
import os

# Global encoder and qdrant setup
encoder = SentenceTransformer('all-MiniLM-L6-v2')
qdrant = QdrantClient(":memory:")

# Prepare data
wd_PATH = os.getcwd()
data_PATH = os.path.join(wd_PATH, "data/top_rated_wines.csv")
df = pd.read_csv(data_PATH)
df = df[df['variety'].notna()] # drop nans
data = df.sample(700).to_dict('records') #small sample

# Collection index
def index_wines(collection_name="top_wines"):
    # Calculate the embeddings of the requested data
    vectors = encoder.encode([doc["notes"] for doc in data]).tolist()

    # Create a qdrant collection
    qdrant.recreate_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=encoder.get_sentence_embedding_dimension(),
            distance=models.Distance.COSINE
        )
    )

    # Upload points using the embeddins
    qdrant.upload_points(
        collection_name=collection_name,
        points=[
            models.PointStruct(
                id=idx,
                vector=vector,
                payload=doc
            )
            for idx, (vector, doc) in enumerate(zip(vectors, data))
        ]
    )
    print(f"Indexed {len(data)} wines into collection '{collection_name}'.")

# 3Función de búsqueda
def get_context(user_prompt: str, limit: int = 3):
    #Encode the prompt
    query_vector = encoder.encode(user_prompt).tolist()

    hits = qdrant.search(
        collection_name= "top_wines",
        query_vector=query_vector,
        limit=limit #Just use top 3 samples based on hit percentage
    )

    return [hit.payload for hit in hits]

