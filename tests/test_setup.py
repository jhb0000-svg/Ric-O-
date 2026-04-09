import os

def test_project_structure():
    assert os.path.isdir("src"), "src directory should exist"
    assert os.path.isdir("src/parsers"), "src/parsers directory should exist"
    assert os.path.isdir("sample_records"), "sample_records directory should exist"
    assert os.path.isfile("requirements.txt"), "requirements.txt should exist"

if __name__ == "__main__":
    test_project_structure()
    print("Project architecture initialized successfully.")
