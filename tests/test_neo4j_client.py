import sys
import os

# Ensure src is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def test_neo4j_client_import():
    try:
        from src.neo4j_client import Neo4jClient
        client = Neo4jClient("bolt://localhost:7687", "neo4j", "testpassword")
        assert hasattr(client, "init_schema"), "Neo4jClient should have init_schema method"
        assert hasattr(client, "close"), "Neo4jClient should have close method"
        print("Neo4jClient import and basic structure check passed!")
    except ImportError as e:
        print(f"Import failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_neo4j_client_import()
