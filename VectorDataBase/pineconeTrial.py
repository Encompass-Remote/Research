#-----------------HEADER--------------------------
# This script is to practice use Pinecone to create an index, embed text data, and perform a query.
#Guide: https://docs.pinecone.io/docs/quickstart
#Pinecone Site: Get Started Tutorial
#----------------END HEADER-----------------------

#-----------INSTALLATION----------------
#pip install pinecone
#pip install pyreadline3
# pip install --upgrade pinecone
#-----------END INSTALLATION-------------


#----------LIBRARIES-------------
from pinecone import Pinecone, ServerlessSpec
import time
#----------END LIBRARIES---------

#--------GLOBAL VARIABLES--------
PINECONE_API_KEY="your_api_key"

pc = Pinecone(api_key="your_api_key")

index_name = "quickstart"
#--------END GLOBAL VARIABLES--------

#-----------CREATE INDEX-------------
pc.create_index(
    name=index_name,
    dimension=1024, # Replace with  model dimensions
    metric="cosine", # Replace with model metric
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    ) 
)
#-----------END CREATE INDEX---------

#-----------INDEXING---------------
data = [
    {"id": "vec1", "text": "Apple is a popular fruit known for its sweetness and crisp texture."},
    {"id": "vec2", "text": "The tech company Apple is known for its innovative products like the iPhone."},
    {"id": "vec3", "text": "Many people enjoy eating apples as a healthy snack."},
    {"id": "vec4", "text": "Apple Inc. has revolutionized the tech industry with its sleek designs and user-friendly interfaces."},
    {"id": "vec5", "text": "An apple a day keeps the doctor away, as the saying goes."},
    {"id": "vec6", "text": "Apple Computer Company was founded on April 1, 1976, by Steve Jobs, Steve Wozniak, and Ronald Wayne as a partnership."}
]
#-----------END INDEXING------------


#-----------EMBEDDING-------------
embeddings = pc.inference.embed(
    model="multilingual-e5-large",
    inputs=[d['text'] for d in data],
    parameters={"input_type": "passage", "truncate": "END"}
)
#-----------END EMBEDDING-----------
print(embeddings[0]) # Print the first embedding

#-----------CREATE INDEX-------------
# Wait for the index to be ready
while not pc.describe_index(index_name).status['ready']:
    time.sleep(1)

index = pc.Index(index_name)

vectors = []
for d, e in zip(data, embeddings):
    vectors.append({
        "id": d['id'],
        "values": e['values'],
        "metadata": {'text': d['text']}
    })

index.upsert(
    vectors=vectors,
    namespace="ns1"
)

print(index.describe_index_stats())
#-----------END CREATE INDEX---------

#-----------QUERYING-------------
query = "Tell me about the tech company known as Apple."

embedding = pc.inference.embed(
    model="multilingual-e5-large",
    inputs=[query],
    parameters={
        "input_type": "query"
    }
)

results = index.query(
    namespace="ns1",
    vector=embedding[0].values,
    top_k=3,
    include_values=False,
    include_metadata=True
)
#-----------END QUERYING-----------
print(results) # Print final results

