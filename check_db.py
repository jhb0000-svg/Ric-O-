import os
from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
user = "neo4j"
password = "rms_password"

driver = GraphDatabase.driver(uri, auth=(user, password))

query = """
MATCH (n)-[r]->(m) 
WHERE labels(n)[0] IN ['RecordResource', 'Agent', 'Activity'] 
  AND labels(m)[0] IN ['RecordResource', 'Agent', 'Activity']
RETURN count(n) as node_count, count(r) as edge_count
"""

with driver.session() as session:
    result = session.run(query)
    record = result.single()
    print("Graph Query result:", record["node_count"], "nodes and", record["edge_count"], "edges")

query2 = "MATCH (n) WHERE labels(n)[0] IN ['RecordResource', 'Agent', 'Activity'] RETURN count(n) as node_count"
with driver.session() as session:
    result = session.run(query2)
    record = result.single()
    print("Standalone Node count:", record["node_count"])

driver.close()
