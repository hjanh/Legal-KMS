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


## User Interface Installation on Ubuntu

- Install Xampp or other Mysql Server (e.g, http://sourceforge.net/projects/xampp/files/XAMPP%20Linux/)

- Increase memeory limit of PHP execution to 256mb
```
gedit /opt/lampp/etc/php.ini
```

- Import taxmining.sql dump (Currently, due to the licensing of some sources, the database was previously completely emptied)

- Install Neo4j

```
wget --no-check-certificate -O - https://debian.neo4j.org/neotechnology.gpg.key | sudo apt-key add -
echo 'deb http://debian.neo4j.org/repo stable/' | sudo tee /etc/apt/sources.list.d/neo4j.list
sudo apt update
sudo apt install neo4j

```

- Due to database version it is neccessary to enable mitgrations

```
sudo chown -R neo4j:neo4j /var/lib/neo4j/data/databases/graph.db/
sudo gedit /etc/neo4j/neo4j.conf
dbms.allow_upgrade=true

```

- Install Python3 and Pip3

- Install Django and force Version 1.11.11

- Install other dependencies

```
pip3 install django_neomodel
pip3 install django_haystack
pip3 install whoosh
pip3 install vote
pip3 install django-vote
pip3 install django-bootstrap3
sudo apt-get install python-mysqldb
sudo apt-get install libmysqlclient-dev
pip3 install mysqlclient

```
- Modify SQL connection string in legal_mining/settings.py

- Modify Neo4j connection settings

```

NEOMODEL_NEO4J_BOLT_URL = os.environ.get('NEO4J_BOLT_URL', 'bolt://neo4j:12345@localhost:7687')
config.DATABASE_URL = 'bolt://neo4j:12345@localhost:7687'
```

- Modify doument_manager/models.py 

```
user_id = models.ForeignKey(User, on_delete=models.PROTECT)
document_id = models.ForeignKey(Documentstorage, on_delete=models.PROTECT)
```

- Run Django

```
python3 manage.py runserver (Or python3 manage.py runserver 0.0.0.0:8000 for lan access)
login=user2
password=user2user2
```
  
