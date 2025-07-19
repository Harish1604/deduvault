# utils/hasher.py
import hashlib
import io
from PIL import Image
import imagehash

def generate_sha256(file_bytes):
    """Compute SHA-256 hash from file bytes."""
    sha256_hash = hashlib.sha256()
    sha256_hash.update(file_bytes)
    return sha256_hash.hexdigest()

def generate_phash(file_bytes):
    """Compute perceptual hash from image bytes."""
    try:
        img = Image.open(io.BytesIO(file_bytes))
        phash = str(imagehash.average_hash(img))  # or imagehash.phash for difference hash
        return phash
    except Exception as e:
        print(f"Error computing phash: {e}")
        return None

def generate_hashes(file_bytes):
    """Compute both SHA-256 and perceptual hash."""
    sha256 = generate_sha256(file_bytes)
    phash = generate_phash(file_bytes)
    return sha256, phash