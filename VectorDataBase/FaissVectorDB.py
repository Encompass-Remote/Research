import faiss
import numpy as np

#2D array of 3 dimensonal vectors
vectors = np.array([
    [0.1, 0.2, 0.3],
    [0.3, 0.2, 0.1],
    [0.9, 0.8, 0.7],
]).astype('float32')
#astype to float32 since faiss only supports float32

#build an index
index = faiss.IndexFlatL2(3)  # creates a flat (brute-force) index for Euclidean (L2) Distance
index.add(vectors)  # add vectors to the index, now ready for searching

#Query
query = np.array([[0.1, 0.2, 0.25]]).astype('float32') #the vector we are searching for similar to vectors in the index
distances, indices = index.search(query, 2)  # search for the 2 nearest neighbors to the query
#returns two arrays:
    #distances: the distances of the nearest neighbors
    #indices: positions of the nearest neighbors in the index
print("Nearest neighbors indices:", indices)