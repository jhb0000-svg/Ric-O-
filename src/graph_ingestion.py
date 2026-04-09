from src.neo4j_client import Neo4jClient

def ingest_rico_metadata(client: Neo4jClient, metadata: dict):
    """
    Takes structured RiC-O JSON metadata and inserts it into Neo4j via Cypher queries.
    """
    record = metadata.get("RecordResource", {})
    if not record:
        return
        
    query_record = """
    MERGE (r:RecordResource {id: $id})
    SET r.name = $name, r.type = $type
    """
    client.execute_query(query_record, parameters={"id": record.get("id"), "name": record.get("name"), "type": record.get("type", "Document")})

    agent = metadata.get("Agent", {})
    if agent:
        query_agent = """
        MERGE (a:Agent {id: $agent_id}) SET a.name = $agent_name
        WITH a MATCH (r:RecordResource {id: $record_id}) MERGE (r)-[:hasCreator]->(a)
        """
        client.execute_query(query_agent, parameters={"agent_id": agent.get("id"), "agent_name": agent.get("name"), "record_id": record.get("id")})

    activity = metadata.get("Activity", {})
    if activity:
        query_activity = """
        MERGE (ac:Activity {id: $activity_id}) SET ac.name = $activity_name
        WITH ac MATCH (r:RecordResource {id: $record_id}) MERGE (r)-[:isAssociatedWithEvent]->(ac)
        """
        client.execute_query(query_activity, parameters={"activity_id": activity.get("id"), "activity_name": activity.get("name"), "record_id": record.get("id")})

    org = metadata.get("Organization", {})
    if org:
        query_org = """
        MERGE (o:Organization {id: $org_id}) SET o.name = $org_name
        WITH o MATCH (r:RecordResource {id: $record_id}) MERGE (r)-[:isOwnedBy]->(o)
        """
        client.execute_query(query_org, parameters={"org_id": org.get("id"), "org_name": org.get("name"), "record_id": record.get("id")})

    law = metadata.get("Mandate", {})
    if law:
        query_law = """
        MERGE (m:Mandate {id: $law_id}) SET m.name = $law_name
        WITH m MATCH (r:RecordResource {id: $record_id}) MERGE (r)-[:isRegulatedBy]->(m)
        """
        client.execute_query(query_law, parameters={"law_id": law.get("id"), "law_name": law.get("name"), "record_id": record.get("id")})

    date = metadata.get("Date", {})
    if date:
        query_date = """
        MERGE (d:Date {id: $date_id}) SET d.name = $date_name
        WITH d MATCH (r:RecordResource {id: $record_id}) MERGE (r)-[:hasDate]->(d)
        """
        client.execute_query(query_date, parameters={"date_id": date.get("id"), "date_name": date.get("name"), "record_id": record.get("id")})
