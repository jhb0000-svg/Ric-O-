import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def test_web_app_import():
    try:
        from src.web_app import app
        print("web_app imported successfully")
        print("Web App check passed!")
        
    except ImportError as e:
        print(f"Import failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_web_app_import()
