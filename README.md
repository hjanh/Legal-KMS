# Legal-KMS
Kowledge Management System to categorize, search and recommend law texts

To overcome the inefficiency of manual legal research processes, the IT artifact facilitates (i) the retrieval of
documents and (ii) knowledge transfer among legal researchers. First traditional text mining techniques are employed to extract
the most informative parts of legal documents. Based on this, a web platform is designed that enables users to search for documents
by keyword. In addition a recommendation system proactively forwards documents to potentially interested users. To generate document
recommendations, a collaborative and a content-based component is developed.
For the content-based system, I leverage the keywords that I extracted in the course of the text mining workflow.
The collaborative recommendations are based on the users' history and thus share the implicit knowledge about the (perceived)
relevance of documents with co-workers.

Basic Functionality:
- Configurable crawler to extract legal documents from various government websites
- Keyword and Boolean Search on 50,000 legal documents (e.g., EU-Law, legislation.gov.uk)
- Document Categorization with NLP techniques (e.g., Multilingual Document Embeddings, Information Extraction Algorithms) using a (neo4j) graph database
- Individual User Logins to track search history 
- Recommendation Engine based on graph recommendation algorithms to identify relevant documents for each user
- Document explorer to view extracted keywords and document metadata

Technical Background:
- The KMS is based on an SQL and a Neo4j database. The SQL database stores the full texts and meta information of the collected documents as well as the login data of the users. In the graph database, the keywords extracted from the documents, named entities and references to other legal documents as well as the 'likes' and 'views' of the users are stored.  
- The text mining workflow uses Machine Translation APIs and Word Embeddings to convert multilingual documents into a single language (English). Then text mining APIs (e.g. IBM Watson) are used to extract keywords and named entities. In addition, a static set of rules is used to identify links between sets.

![workflow](http://murtaugh.de/img_tmp/2.png)

- Document recommendations are calculated using metapath values between (weighted) nodes in the graph database. This makes it possible to determine the "similarity" of documents taking into account all existing paths between two documents to be compared.
- The search function was implemented with the Python library Whoosh, new documents have to be indexed regularly.
- The interface was realized with Django. 

### Screenshot of the crawler interface
![crawler interface](http://murtaugh.de/img_tmp/1.png)


### Keyword Search
![search interface](http://murtaugh.de/img_tmp/3.png)


### Recommendations
![search interface](http://murtaugh.de/img_tmp/5.png)
