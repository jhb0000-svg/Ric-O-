import os
import sys

# Ensure src is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def test_office_parsers_import():
    try:
        from src.parsers.office_parsers import parse_docx, parse_excel
        print("office_parsers imported successfully")
        
        # Test basic definitions
        assert callable(parse_docx), "parse_docx should be callable"
        assert callable(parse_excel), "parse_excel should be callable"
        
        print("Office Parser check passed!")
        
    except ImportError as e:
        print(f"Import failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_office_parsers_import()
