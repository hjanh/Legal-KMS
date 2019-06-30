# Legal-KMS
Kowledge Management System to categorize, search and recommend law texts

To overcome the inefficiency of manual legal research processes, the IT artifact facilitates (i) the retrieval of
documents and (ii) knowledge transfer among legal researchers. First traditional text mining techniques are employed to extract
the most informative parts of legal documents. Based on this, a web platform is designed that enables users to search for documents
by keyword. In addition a recommendation system proactively forwards documents to potentially interested users. To generate document
recommendations, I develop a predictive model consisting of both a collaborative and a content-based component.
For the content-based system, I leverage the keywords that I extracted in the course of the text mining workflow.
The collaborative recommendations are based on the users' history and thus share the implicit knowledge about the (perceived)
relevance of documents with co-workers.

Basic Functionality:
- Keyword and Boolean Search on 50,000 legal documents (e.g., EU-Law, legislation.gov.uk)
- Document Categorization with NLP techniques (e.g., Multilingual Document Embeddings, Information Extraction Algorithms) using a (neo4j) graph database
- Individual User Logins to track search history 
- Recommendation Engine based on graph recommendation algorithms to identify relevant documents for each user
- Document explorer to view extracted keywords and document metadata
