import os
import sys

# Ensure src is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def test_graph_ingestion_import():
    try:
        from src.graph_ingestion import ingest_rico_metadata
        print("graph_ingestion imported successfully")
        
        assert callable(ingest_rico_metadata), "ingest_rico_metadata should be callable"
        print("Graph Ingestion check passed!")
        
    except ImportError as e:
        print(f"Import failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_graph_ingestion_import()
