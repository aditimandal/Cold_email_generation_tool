import pandas as pd # Importing pandas for handling CSV file operations
import chromadb # Importing ChromaDB for vector-based storage and retrieval
import uuid # Importing uuid to generate unique identifiers for documents


class Portfolio:
    def __init__(self, file_path="app/resource/my_portfolio.csv"):
        """
                Initializes the Portfolio class.
                - Loads data from a CSV file.
                - Creates a persistent ChromaDB client.
                - Retrieves or creates a ChromaDB collection for storing portfolio data.
        """
        self.file_path = file_path  # Storing the file path of the portfolio CSV
        self.data = pd.read_csv(file_path)  # Reading the CSV file into a pandas DataFrame
        self.chroma_client = chromadb.PersistentClient('vectorstore') # Initializing ChromaDB persistent storage
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio") # Getting or creating a ChromaDB collection

    def load_portfolio(self):

        """
                Loads the portfolio data into ChromaDB if it's not already present.
                - Checks if the collection is empty.
                - Iterates over CSV rows and adds them to ChromaDB.
                - Uses 'Techstack' as the document and stores 'Links' as metadata.
        """
        if not self.collection.count(): # Checking if the collection is empty
            for _, row in self.data.iterrows(): # Iterating over each row in the CSV data
                self.collection.add(documents=row["Techstack"], # Adding technology stack as document text
                                    metadatas={"links": row["Links"]}, # Storing the portfolio links as metadata
                                    ids=[str(uuid.uuid4())]) # Generating a unique ID for each document
        print("Number of documents in ChromaDB:", self.collection.count()) # Printing the number of stored documents

    def query_links(self, skills):
        """
                Queries the ChromaDB collection for relevant portfolio links based on provided skills.
                - Takes a skills string as input.
                - Searches the collection for the best matching documents.
                - Returns up to 2 matching results.
        """
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', []) # Fetching relevant metadata (links) based on skills query