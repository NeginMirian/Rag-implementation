import pandas as pd
import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
from huggingface_hub import InferenceClient
import numpy as np
import os
def text_embedding(text) -> None:
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    return model.encode(text)

def generate_context(query):
    vector=text_embedding(query).tolist()

    results= collection.query(
        query_embeddings=vector,
        n_results=15,
        include=["documents"]
    )

    res = "\n".join(str(item) for item in results['documents'][0])
    return res
def chat_completion(system_prompt, user_prompt,length=1000):
    final_prompt=f"""<s>[INST]<<SYS>>
    {system_prompt}
    <</SYS>>

    {user_prompt} [/INST]"""
    return client.text_generation(prompt=final_prompt,max_new_tokens = length).strip()

#data
df=pd.read_csv(r"C:\Users\negin\OneDrive\Desktop\the_grammy_awards.csv")
df=df.loc[df['year'] == 2019]
df=df.dropna(subset=['nominee'])
df.loc[:, 'category'] = df['category'].str.lower()
df.loc[:, 'text'] = df['artist'] + ' got nominated under the category, ' + df['category'] + ', for the track ' + df['nominee'] + ' to win the award'
df.loc[df['winner'] == False, 'text'] = df['artist'] + ' got nominated under the category, ' + df['category'] + ', for the track ' + df['nominee'] + ' but did not win'

df['text'] = df['text'].astype(str)
print(df.head())
# Now create the 'docs' and 'ids' lists
docs = df["text"].tolist()
ids = [str(x) for x in df.index.tolist()]

client = chromadb.Client()
collection = client.get_or_create_collection("Grammy-2019")

docs=df["text"].tolist()
ids= [str(x) for x in df.index.tolist()]
collection.add(
    documents=docs,
    ids=ids
)
URI    = 'http://127.0.0.1:8080'
client = InferenceClient(model = URI)
query="Did Billie Eilish won a reward for grammy 2019?"
#query="Who is the music director of RRR?"
context=generate_context(query)
system_prompt="""\
You are a helpful AI assistant that can answer questions on grammy 2019 awards. Answer based on the context provided. If you cannot find the correct answerm, say I don't know. Be concise and just include the response.
"""
user_prompt=f"""
Based on the context:
{context}
Answer the below query:
{query}
"""
resp = chat_completion(system_prompt, user_prompt)
print(resp)