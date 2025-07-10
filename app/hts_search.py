import faiss
import pandas as pd
import numpy as np
import openai
import os
from dotenv import load_dotenv


load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))
client = openai.OpenAI(api_key=os.getenv("OPENAI_KEY"))


base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "data")
faiss_path = os.path.join(data_dir, "hts_index.faiss")
csv_path = os.path.join(data_dir, "hts.csv")

# Load index and data
index = faiss.read_index(faiss_path)
df = pd.read_csv(csv_path)

# One input → one embedding
def get_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return np.array(response.data[0].embedding, dtype=np.float32)

# AI search function
def search_hts_with_ai(query, k=5):
    query_vec = get_embedding(query).reshape(1, -1)
    D, I = index.search(query_vec, k=k)

    matches = []
    for idx in I[0]:
        row = df.iloc[idx]
        matches.append({
            "hts_code": row["HTS Number"],
            "description": row["Description"],
            "base_duty": str(row["General Rate of Duty"]) if pd.notna(row["General Rate of Duty"]) else "Unknown",
            "special_duty": str(row["Special Rate of Duty"]) if pd.notna(row["Special Rate of Duty"]) else "Unknown",
            "c2_duty": str(row["Column 2 Rate of Duty"]) if pd.notna(row["Column 2 Rate of Duty"]) else "Unknown",
            "add_duty": str(row["Additional Duties"]) if pd.notna(row["Additional Duties"]) else "Unknown"
        })

    return matches