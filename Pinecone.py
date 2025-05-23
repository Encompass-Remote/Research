

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
#Initialize connection with the Pinecone client using your OWN API key
PINECONE_API_KEY="YOUR-API-KEY"

pc = Pinecone(api_key="YOUR-API-KEY")

#define your index name of the index we will work with
index_name = "quickstart"
#--------END GLOBAL VARIABLES--------


#-----------CREATE INDEX-------------
#Check to ensure this index does not already exits
if index_name not in [idx['name'] for idx in pc.list_indexes()]:
    #if this index does not exist, create it with the predefined name
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
#Create sample data to be stored in the vector database
#each item has an id, text, and company name
data = [
    {"id": "vec1", "text": "Apple is a popular fruit known for its sweetness and crisp texture.", "company": "Apple"},
    {"id": "vec2", "text": "The tech company Apple is known for its innovative products like the iPhone.", "company": "Apple"},
    {"id": "vec3", "text": "Many people enjoy eating apples as a healthy snack.", "company": "Apple"},
    {"id": "vec4", "text": "Apple Inc. has revolutionized the tech industry with its sleek designs and user-friendly interfaces.", "company": "Apple"},
    {"id": "vec5", "text": "An apple a day keeps the doctor away, as the saying goes.", "company": "Apple"},
    {"id": "vec6", "text": "Apple Computer Company was founded on April 1, 1976, by Steve Jobs, Steve Wozniak, and Ronald Wayne as a partnership.", "company": "Apple"},
    {"id": "vec7", "text": "Microsoft is a tech company known for its software products like Windows and Office.", "company": "Microsoft"},
    {"id": "vec8", "text": "HP is a well-known brand in the computer industry, producing laptops and printers.", "company": "Microsoft"},
    {"id": "vec9", "text": "Microsoft also famously produces the Xbox gaming console", "company": "Microsoft"},
    {"id": "vec10", "text": "Sony is technology company known for electronics like smartphones, cameras, and watches","company": "Sony"},
    {"id": "vec11", "text": "Sony famously produces the Playstation gaming console, with hit games like God of War, Spider-Man, and the Last of Us", "company": "Sony"},
    {"id": "vec12", "text": "Sony is a Japanese multinational conglomerate corporation headquartered in Tokyo, Japan.", "company": "Sony"},
    {"id": "vec13", "text": "Nvidia is a tech company known for its graphics processing units (GPUs) and AI technology.", "company": "Nvidia"},
    {"id": "vec14", "text": "Nvidia's GPUs are widely used in gaming, AI, and data centers.", "company": "Nvidia"}
]
#-----------END INDEXING------------


#-----------EMBEDDING-------------
#Generate embeddings for each text entry using Pinecone's embedding service
#Embeddings are vector representations of the text that capture semantinc meaning
embeddings = pc.inference.embed(
    model="multilingual-e5-large", #embedding model we use
    inputs=[d['text'] for d in data], #extract text from each data item
    parameters={"input_type": "passage", "truncate": "END"} #specify input type and truncation method
)
#-----------END EMBEDDING-----------
#-----------CREATE INDEX-------------
# Wait for the index to be ready
while not pc.describe_index(index_name).status['ready']:
    time.sleep(1)

#create a connection to existing Pinecone index
index = pc.Index(index_name)

#initialize a list to store vector data
vectors = []
#iterate through each data item and embedding, and create a vector object
for d, e in zip(data, embeddings):
    vectors.append({
        "id": d['id'],
        "values": e['values'],
        "metadata": {'text': d['text'], "company" : d["company"]}
    })

#upload the vector data into the Pinecone index
index.upsert(
    vectors=vectors,
    namespace="ns1"
)

#print(index.describe_index_stats())
#-----------END CREATE INDEX---------

#-----------QUERYING-------------
#Small demo to show how to query the index
print("Welcome to Pinecone querying demo!")
print("We have inforamtion about Apple, Microsoft, HP, Sony, and Nvidia.")
#get input from user about which company they would like to hear about
company = input("Which company would you like to know more about? (Apple, Microsoft, HP, Sony, Nvidia): ")
#ensure company is valud
if company not in ["Apple", "Microsoft", "HP", "Sony", "Nvidia"]:
    print("Invalid company name. Please try again.")
    exit()
else:
    #create the query with the company name
    query = "Tell me about the tech company known as " + company + "."
    #generate embedding for the query
    embedding = pc.inference.embed(
    model="multilingual-e5-large",
    inputs=[query],
    parameters={
        "input_type": "query"
    }
    )
    #get the results matching the query from the user
    results = index.query(
        namespace="ns1",
        vector=embedding[0].values,
        top_k=3,
        include_values=False,
        include_metadata=True,
        filter={"company": company}
    )
    #-----------END QUERYING-----------
    #print(results) # Print final results
    #Print best 3 results
    print("Top Results:")
    for match in results['matches']:
        print(f"ID: {match['id']}")
        print(f"Score: {match['score']:.4f}")
        print(f"Text: {match['metadata']['text']}\n")




