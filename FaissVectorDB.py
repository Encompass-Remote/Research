import faiss
import numpy as np

vectors = np.array([
    [0.1, 0.2, 0.3],
    [0.3, 0.2, 0.1],
    [0.9, 0.8, 0.7],
]).astype('float32')

#build an index
index = faiss.IndexFlatL2(3)  # dimension is 3
index.add(vectors)  # add vectors to the index

#Query
query = np.array([[0.1, 0.2, 0.25]]).astype('float32')
distances, indices = index.search(query, 2)  # search for the 2 nearest neighbors
print("Nearest neighbors indices:", indices)