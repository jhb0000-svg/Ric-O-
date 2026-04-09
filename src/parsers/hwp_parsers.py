import olefile
import zlib

def parse_hwp(file_path: str) -> str:
    """Reads a HWP/HWPX file and attempts to extract basic text."""
    if file_path.endswith('.hwpx'):
        # Just a mock for hwpx, which is a zip file inside
        return "Extracting HWPX text not fully implemented. Mock text."

    if not olefile.isOleFile(file_path):
        return "Not a valid OLE file."

    with olefile.OleFileIO(file_path) as f:
        # HWP files usually contain 'PrvText' which holds preview text.
        if f.exists('PrvText'):
            prv_text = f.openstream('PrvText').read()
            # Decode using UTF-16LE as standard for HWP PrvText
            try:
                return prv_text.decode('utf-16le').strip()
            except Exception:
                return prv_text.decode('utf-8', errors='ignore').strip()
        else:
            return "No PrvText stream found. Deep extraction requires pyhwp."
