import os
import sys

# Ensure src is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def test_llm_extractor_import():
    try:
        from src.llm_extractor import extract_rico_metadata
        print("llm_extractor imported successfully")
        
        assert callable(extract_rico_metadata), "extract_rico_metadata should be callable"
        print("LLM Extractor check passed!")
        
    except ImportError as e:
        print(f"Import failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_llm_extractor_import()
