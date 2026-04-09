# Neo4j Cypher Queries for RiC-O Graph View

Here are some cypher queries you can copy/paste directly into your Neo4j Browser (http://localhost:7474) to test and visualize the GraphRAG metadata extracted from your records.

### 1. View Everything (Basic Overview)
```cypher
MATCH (n) RETURN n LIMIT 100
```
*Purpose: Displays all nodes and their relationships. Useful when you have a small dataset like our sample records.*

### 2. View all Records and their Creators (Agents)
```cypher
MATCH (r:RecordResource)-[rel:hasCreator]->(a:Agent)
RETURN r, rel, a
```
*Purpose: Visualizes the `RecordResource` nodes and connects them to the `Agent` that created them.*

### 3. View all Records associated with specific Activities
```cypher
MATCH (r:RecordResource)-[rel:isAssociatedWithEvent]->(ac:Activity)
RETURN r, rel, ac
```
*Purpose: Groups documents by the official business process/activity they belong to. Essential for context-aware retention classification.*

### 4. Find all documents created by a specific Agent (e.g. System Agent)
```cypher
MATCH (r:RecordResource)-[:hasCreator]->(a:Agent)
WHERE a.name CONTAINS 'System Agent'
RETURN r
```
*Purpose: Demonstrates entity-filtered retrieval logic that the LLM would use for GraphRAG.*

### 5. Clear Database (Reset the Graph)
```cypher
MATCH (n) DETACH DELETE n;
```
*Purpose: Deletes all nodes and relationships. Useful when you modify the LLM extractor and want to re-run your `main.py` ingestion pipeline cleanly.*
