import pandas as pd
import numpy as np
import openai
import faiss
import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("OPENAI_KEY")
client = openai.OpenAI(api_key=key)
base_dir = os.path.dirname(os.path.abspath(__file__))  # always points to /app
data_dir = os.path.join(base_dir, "data")
csv_path = os.path.join(base_dir, "data", "hts.csv")
df = pd.read_csv(csv_path)  
progress_path = os.path.join(data_dir, "hts_progress.npy")
faiss_path = os.path.join(data_dir, "hts_index.faiss")


descriptions = df["Description"].astype(str).tolist()

# Generate embedding for each description
def get_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return np.array(response.data[0].embedding, dtype=np.float32)



if os.path.exists(progress_path):
    vectors = list(np.load(progress_path, allow_pickle=True))
    start = len(vectors)
    print(f"row {start}/{len(descriptions)}")
else:
    vectors = []
    start = 0



for i in range(start, len(descriptions)):
    desc = descriptions[i]
    print(f"Embedding {i+1}/{len(descriptions)}: {desc[:60]}...")

    try:
        embedding = get_embedding(desc)
        vectors.append(embedding)

        if i % 25 == 0 or i == len(descriptions) - 1:
            np.save(progress_path, np.array(vectors, dtype=object))

    except Exception as e:
        print(f"Error at row {i}: {e}")
        break

embeddings = np.vstack(vectors)

# Save FAISS index
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)
faiss.write_index(index, faiss_path)
df.to_csv(csv_path, index=False)
print("All embeddings saved to FAISS")