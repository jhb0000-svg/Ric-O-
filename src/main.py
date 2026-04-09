import os
import sys

# Ensure src is in the path if called directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.parsers.basic_parsers import parse_txt, parse_pdf
from src.parsers.office_parsers import parse_docx, parse_excel
from src.parsers.hwp_parsers import parse_hwp
from src.llm_extractor import extract_rico_metadata
from src.graph_ingestion import ingest_rico_metadata
from src.neo4j_client import Neo4jClient

def process_file(file_path: str):
    print(f"Processing: {file_path}")
    ext = file_path.split('.')[-1].lower()
    text = ""
    
    if ext == 'txt':
        text = parse_txt(file_path)
    elif ext == 'pdf':
        text = parse_pdf(file_path)
    elif ext == 'docx':
        text = parse_docx(file_path)
    elif ext == 'xlsx':
        text = parse_excel(file_path)
    elif ext in ['hwp', 'hwpx']:
        text = parse_hwp(file_path)
    else:
        print(f"Unsupported extension: {ext}")
        return None
        
    if not text:
        print(f"No text extracted from {file_path}")
        return None
        
    metadata = extract_rico_metadata(text)
    return metadata

def main():
    # Initialize Neo4j Client (Using env vars or defaults)
    uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
    user = os.environ.get("NEO4J_USER", "neo4j")
    password = os.environ.get("NEO4J_PASSWORD", "password")
    
    # Check if we should actually connect to Neo4j. In test mode we might skip it.
    if os.environ.get("TEST_MODE") == "1":
        print("Running in TEST_MODE. Skipping Neo4j connection.")
        client = None
    else:
        try:
            client = Neo4jClient(uri, user, password)
            client.init_schema()
        except Exception as e:
            print(f"Failed to connect to Neo4j: {e}")
            sys.exit(1)

    record_dir = "sample_records"
    if not os.path.exists(record_dir):
        print(f"Directory {record_dir} does not exist.")
        sys.exit(1)
        
    for filename in os.listdir(record_dir):
        file_path = os.path.join(record_dir, filename)
        if os.path.isfile(file_path):
            metadata = process_file(file_path)
            if metadata and client:
                print(f"Ingesting metadata for {filename} into Neo4j...")
                ingest_rico_metadata(client, metadata)
                
    if client:
        client.close()
    print("Processing complete.")

if __name__ == "__main__":
    main()
