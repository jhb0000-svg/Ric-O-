import os
import sys

# Ensure src is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def test_hwp_parsers_import():
    try:
        from src.parsers.hwp_parsers import parse_hwp
        print("hwp_parsers imported successfully")
        
        # Test basic definitions
        assert callable(parse_hwp), "parse_hwp should be callable"
        print("HWP Parser check passed!")
        
    except ImportError as e:
        print(f"Import failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_hwp_parsers_import()
