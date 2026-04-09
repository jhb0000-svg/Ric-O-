from neo4j import GraphDatabase

class Neo4jClient:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def init_schema(self):
        """Initialize the core RiC-O graph schema constraints."""
        with self.driver.session() as session:
            # RiC-O core entity constraints
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (r:RecordResource) REQUIRE r.id IS UNIQUE")
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (a:Agent) REQUIRE a.id IS UNIQUE")
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (ac:Activity) REQUIRE ac.id IS UNIQUE")
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (m:Mandate) REQUIRE m.id IS UNIQUE")

    def execute_query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record.data() for record in result]
