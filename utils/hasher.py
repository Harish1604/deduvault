import hashlib

def generate_sha256(file_path, description=""):
    with open(file_path, 'rb') as f:
        file_data = f.read()
    combined = file_data + description.encode('utf-8')
    return hashlib.sha256(combined).hexdigest()
