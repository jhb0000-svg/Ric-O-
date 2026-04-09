import os
import sys

# Ensure src is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def test_basic_parsers_import():
    try:
        from src.parsers.basic_parsers import parse_txt, parse_pdf
        print("basic_parsers imported successfully")
        
        # Test basic TXT extraction
        test_txt_path = "sample_records/test.txt"
        with open(test_txt_path, "w", encoding="utf-8") as f:
            f.write("Hello, RiC-O!")
        
        result = parse_txt(test_txt_path)
        assert result == "Hello, RiC-O!", "TXT parsing failed"
        print("TXT Parser check passed!")
        
    except ImportError as e:
        print(f"Import failed: {e}")
        sys.exit(1)
    finally:
        if os.path.exists("sample_records/test.txt"):
            os.remove("sample_records/test.txt")

if __name__ == "__main__":
    test_basic_parsers_import()
