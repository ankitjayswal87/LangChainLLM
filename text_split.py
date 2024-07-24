from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load example document
with open("openai_test_data.txt") as f:
    sachin_data = f.read()

text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=500,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
)
chunks = text_splitter.split_text(sachin_data)
#print(chunks)
#print(chunks[9])
#print(chunks[20])
# print(len(chunks))
# for chunk in chunks:
#     print(len(chunk))

encoder = SentenceTransformer("all-mpnet-base-v2")
vectors = encoder.encode(chunks)
print(vectors.shape)

index = faiss.IndexFlatL2(vectors.shape[1])
index.add(vectors)

search_query = "who is Ankit Jayswal"
k=1
vec = encoder.encode(search_query)
svev = np.array(vec).reshape(1,-1)
distances,I = index.search(svev,k=k)
for i in range(0,k):
    print(chunks[I[0][i]])
