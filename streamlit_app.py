import time
import streamlit as st
from uploader import upload_to_pinata, check_duplicate, init_db
from interact import store_file_on_chain, check_file_exists, get_file_data
from PIL import Image
import io
from utils.hasher import generate_hashes
from dotenv import load_dotenv
import os
import git
import logging

# Load .env file
load_dotenv()

# Initialize SQLite database
init_db()

# GitHub repository sync
DB_PATH = "data/dedup_db.sqlite"
REPO_DIR = "."

# Initialize Git repository
os.makedirs("data", exist_ok=True)
try:
    repo = git.Repo(REPO_DIR)
    # Pull latest database
    origin = repo.remotes.origin
    origin.pull()
    logging.info("Pulled latest database from GitHub")
except git.exc.NoSuchPathError:
    logging.error("Git repository not initialized. Initialize it in deployment.")
except git.exc.GitCommandError as e:
    logging.error(f"Git pull failed: {e}")

# Trusted uploaders
trusted_uploaders = ["0x66c720EaDEEc55048fFCb86A0300123D5fe0b1a7", "0x92643AEafaf65d9cA08347A9e8e09c7A927b1362"]

# Page configuration
st.set_page_config(
    page_title="DeduVault - Decentralized Image Vault",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with Tailwind and unique styling
st.markdown("""
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>
    body {
        font-family: 'Poppins', sans-serif;
    }
    .theme-dark {
        background: #1a202c;
        color: #e2e8f0;
    }
    .theme-light {
        background: #f7fafc;
        color: #1a202c;
    }
    .header {
        background: linear-gradient(135deg, #2b6cb0 0%, #9f7aea 100%);
        padding: 3rem 2rem;
        border-radius: 1rem;
        text-align: center;
        box-shadow: 0 8px 24px rgba(0,0,0,0.2);
        position: relative;
        overflow: hidden;
        margin-bottom: 2rem;
    }
    .header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        opacity: 0.5;
    }
    .header-title {
        font-size: 2.75rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    .header-subtitle {
        font-size: 1.25rem;
        font-weight: 300;
        opacity: 0.9;
    }
    .sidebar-card {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #4c51bf 0%, #b794f4 100%);
        padding: 1rem;
        border-radius: 0.75rem;
        text-align: center;
        color: white;
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    }
    .metric-card:hover {
        transform: scale(1.05);
    }
    .workflow-step {
        display: flex;
        align-items: center;
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 0.75rem;
        margin-bottom: 0.75rem;
        transition: all 0.3s ease;
    }
    .workflow-step:hover {
        background: rgba(255,255,255,0.2);
        transform: translateX(8px);
    }
    .step-number {
        background: #ed64a6;
        color: white;
        width: 2rem;
        height: 2rem;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 1rem;
        font-weight: 600;
    }
    .feature-card {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.3s ease;
        margin-bottom: 1rem;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.3);
        background: rgba(255,255,255,0.1);
    }
    .hash-display {
        background: rgba(0,0,0,0.2);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 0.5rem;
        padding: 1rem;
        font-family: 'Courier New', monospace;
        word-break: break-all;
        margin: 1rem 0;
        color: #e2e8f0;
    }
    .status-success {
        background: #38a169;
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        animation: fadeIn 0.5s ease-in;
    }
    .status-warning {
        background: #d69e2e;
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        animation: fadeIn 0.5s ease-in;
    }
    .ecommerce-card {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.3s ease;
        margin-bottom: 1rem;
    }
    .ecommerce-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    }
    .platform-logo {
        width: 2.5rem;
        height: 2.5rem;
        border-radius: 0.5rem;
        margin-right: 0.75rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        color: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    .price-tag {
        background: linear-gradient(135deg, #ed64a6 0%, #f687b3 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 1rem;
        font-weight: 600;
        display: inline-block;
        margin: 0.5rem 0;
    }
    .product-specs {
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .spec-item {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    .spec-item:last-child {
        border-bottom: none;
    }
    .action-button {
        background: linear-gradient(135deg, #ed64a6 0%, #9f7aea 100%);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        font-weight: 600;
        text-align: center;
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 1rem;
    }
    .action-button:hover {
        background: linear-gradient(135deg, #d53f8c 0%, #7f9cf5 100%);
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    .progress-ring {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 1rem 0;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>
<script src="https://cdn.jsdelivr.net/npm/circular-progressbar@1.0.0/dist/circularProgressBar.min.js"></script>
""", unsafe_allow_html=True)

# Theme toggle
theme = st.session_state.get("theme", "dark")
if st.sidebar.button("🌙 Toggle Theme", key="theme_toggle"):
    theme = "light" if theme == "dark" else "dark"
    st.session_state.theme = theme

# Apply theme
st.markdown(f'<div class="theme-{theme}">', unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header">
    <h1 class="header-title">🔒 DeduVault</h1>
    <p class="header-subtitle">Revolutionary Decentralized Image Deduplication</p>
    <p class="text-sm mt-2 opacity-80">Securely store and verify digital assets with IPFS and blockchain technology</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-card"><h3 class="text-lg font-semibold">📊 Platform Analytics</h3></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="metric-card">
        <h4 class="text-2xl font-bold">12,847</h4>
        <p class="text-sm">Files Processed</p>
        <p class="text-xs text-green-300">↗️ 23%</p>
    </div>
    <div class="metric-card">
        <h4 class="text-2xl font-bold">2.3 TB</h4>
        <p class="text-sm">Storage Saved</p>
        <p class="text-xs text-green-300">↗️ 15%</p>
    </div>
    <div class="metric-card">
        <h4 class="text-2xl font-bold">1,249</h4>
        <p class="text-sm">Active Users</p>
        <p class="text-xs text-green-300">↗️ 8%</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="sidebar-card"><h3 class="text-lg font-semibold">🔧 Workflow</h3></div>', unsafe_allow_html=True)
    workflow_steps = [
        "Upload image file",
        "Generate SHA-256 & phash",
        "Check for duplicates",
        "Store on IPFS",
        "Record on blockchain"
    ]
    for i, step in enumerate(workflow_steps, 1):
        st.markdown(f"""
        <div class="workflow-step">
            <div class="step-number">{i}</div>
            <div class="text-sm">{step}</div>
        </div>
        """, unsafe_allow_html=True)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<h3 class="text-xl font-semibold mb-4">🚀 Core Features</h3>', unsafe_allow_html=True)
    features = [
        {"title": "🔐 Advanced Security", "desc": "SHA-256 and perceptual hashing for unmatched data integrity"},
        {"title": "🌐 IPFS Storage", "desc": "Decentralized, content-addressed file storage"},
        {"title": "⛓️ Blockchain Trust", "desc": "Immutable records for transparent verification"},
        {"title": "⚡ Instant Deduplication", "desc": "Real-time detection of exact and visual duplicates"}
    ]
    for feature in features:
        st.markdown(f"""
        <div class="feature-card">
            <h4 class="text-lg font-semibold">{feature['title']}</h4>
            <p class="text-sm opacity-80">{feature['desc']}</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown('<h3 class="text-xl font-semibold mb-4">📈 System Metrics</h3>', unsafe_allow_html=True)
    st.markdown("""
    <div class="metric-card">
        <h3 class="text-2xl font-bold">99.9%</h3>
        <p class="text-sm">Uptime</p>
    </div>
    <div class="metric-card">
        <h3 class="text-2xl font-bold">< 2s</h3>
        <p class="text-sm">Processing Time</p>
    </div>
    <div class="metric-card">
        <h3 class="text-2xl font-bold">256-bit</h3>
        <p class="text-sm">Encryption</p>
    </div>
    """, unsafe_allow_html=True)

# Upload Section
st.markdown('<hr class="border-t border-gray-700 my-6">', unsafe_allow_html=True)
st.markdown('<h3 class="text-xl font-semibold mb-4">📤 Upload Image</h3>', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "Choose an image (JPG, JPEG, PNG, WEBP)",
    type=["jpg", "jpeg", "png", "webp"],
    help="Max size: 10MB"
)

if uploaded_file is not None and uploaded_file.size > 0:
    if uploaded_file.size > 10 * 1024 * 1024:
        st.error("File size exceeds 10MB limit.")
        st.stop()
    
    file_bytes = uploaded_file.read()
    file_name = uploaded_file.name

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('<h4 class="text-lg font-semibold mb-3">🖼️ Image Preview</h4>', unsafe_allow_html=True)
        if uploaded_file.type.startswith("image/"):
            image = Image.open(io.BytesIO(file_bytes))
            st.image(image, use_column_width=True, caption=f"{file_name}")
        else:
            st.markdown('<div class="status-warning text-sm">⚠️ Unsupported image type.</div>', unsafe_allow_html=True)

        st.markdown('<h4 class="text-lg font-semibold mb-3 mt-4">📋 File Details</h4>', unsafe_allow_html=True)
        file_size = len(file_bytes)
        st.markdown(f"""
        <div class="product-specs">
            <div class="spec-item">
                <span class="text-sm font-medium">Filename:</span>
                <span class="text-sm">{file_name}</span>
            </div>
            <div class="spec-item">
                <span class="text-sm font-medium">Size:</span>
                <span class="text-sm">{file_size:,} bytes ({file_size/1024:.1f} KB)</span>
            </div>
            <div class="spec-item">
                <span class="text-sm font-medium">Type:</span>
                <span class="text-sm">{uploaded_file.type}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown('<h4 class="text-lg font-semibold mb-3">🔐 Processing</h4>', unsafe_allow_html=True)
        start_time = time.time()
        sha256, phash = generate_hashes(file_bytes)
        st.markdown('<p class="text-sm font-medium">SHA-256 Hash:</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="hash-display text-sm"><code>{sha256}</code></div>', unsafe_allow_html=True)
        if phash:
            st.markdown('<p class="text-sm font-medium">Perceptual Hash:</p>', unsafe_allow_html=True)
            st.markdown(f'<div class="hash-display text-sm"><code>{phash}</code></div>', unsafe_allow_html=True)

        with st.spinner("🔄 Processing..."):
            progress_bar = st.progress(0)
            progress_bar.progress(25)
            st.markdown(f'<p class="text-sm">✅ Hashes generated in {time.time() - start_time:.2f}s</p>', unsafe_allow_html=True)
            time.sleep(0.5)
            progress_bar.progress(50)
            st.markdown('<p class="text-sm">🔍 Checking duplicates...</p>', unsafe_allow_html=True)

            is_duplicate, message, sha256, phash = check_duplicate(file_bytes, file_name)
            if is_duplicate:
                st.markdown(f"""
                <div class="status-warning">
                    <h4 class="text-base font-semibold">⚠️ Duplicate Detected!</h4>
                    <p class="text-sm">{message}</p>
                </div>
                """, unsafe_allow_html=True)

                data = get_file_data(sha256)
                if data:
                    st.markdown('<h4 class="text-lg font-semibold mb-3">📊 Record Details</h4>', unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="product-specs">
                        <div class="spec-item">
                            <span class="text-sm font-medium">CID:</span>
                            <span class="text-sm"><code>{data.get('cid', 'N/A')}</code></span>
                        </div>
                        <div class="spec-item">
                            <span class="text-sm font-medium">Uploader:</span>
                            <span class="text-sm"><code>{data.get('uploader', 'N/A')}</code></span>
                        </div>
                        <div class="spec-item">
                            <span class="text-sm font-medium">Status:</span>
                            <span class="text-sm">{'Trusted' if data.get('uploader', '').lower() in trusted_uploaders else 'Untrusted'}</span>
                        </div>
                        <div class="spec-item">
                            <span class="text-sm font-medium">Timestamp:</span>
                            <span class="text-sm">{data.get('timestamp', 'N/A')}</span>
                        </div>
                        <div class="spec-item">
                            <span class="text-sm font-medium">Perceptual Hash:</span>
                            <span class="text-sm"><code>{data.get('phash', 'N/A')}</code></span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                # Commit and push database to GitHub
                try:
                    repo.index.add([DB_PATH])
                    repo.index.commit(f"Update database for {file_name}")
                    origin.push()
                    logging.info("Pushed database to GitHub")
                except Exception as e:
                    logging.error(f"Git push failed: {e}")
                    st.warning("⚠️ Database sync to GitHub failed. Duplicate detection may not persist.")
            else:
                progress_bar.progress(75)
                st.markdown('<p class="text-sm">✅ No duplicates. Uploading to IPFS...</p>', unsafe_allow_html=True)
                try:
                    cid = upload_to_pinata(file_bytes, file_name)
                    st.markdown(f"""
                    <div class="status-success">
                        <h4 class="text-base font-semibold">✅ IPFS Upload Successful!</h4>
                        <p class="text-sm"><strong>CID:</strong> <code>{cid}</code></p>
                        <p class="text-sm"><a href="https://gateway.pinata.cloud/ipfs/{cid}" target="_blank" class="text-blue-400 hover:underline">View on IPFS</a></p>
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"❌ IPFS upload failed: {e}")
                    st.stop()

                progress_bar.progress(100)
                st.markdown('<p class="text-sm">🔗 Recording on blockchain...</p>', unsafe_allow_html=True)
                tx_hash = store_file_on_chain(sha256, phash, cid)
                if tx_hash:
                    st.markdown(f"""
                    <div class="status-success">
                        <h4 class="text-base font-semibold">🎉 Blockchain Registered!</h4>
                        <p class="text-sm"><strong>Tx Hash:</strong> <code>{tx_hash}</code></p>
                        <p class="text-sm">File permanently recorded.</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("❌ Blockchain transaction failed.")
                # Commit and push database to GitHub
                try:
                    repo.index.add([DB_PATH])
                    repo.index.commit(f"Update database for {file_name}")
                    origin.push()
                    logging.info("Pushed database to GitHub")
                except Exception as e:
                    logging.error(f"Git push failed: {e}")
                    st.warning("⚠️ Database sync to GitHub failed. Duplicate detection may not persist.")

# E-Commerce Preview
st.markdown('<hr class="border-t border-gray-700 my-6">', unsafe_allow_html=True)
st.markdown('<h3 class="text-xl font-semibold mb-4">🛒 E-Commerce Preview</h3>', unsafe_allow_html=True)
st.markdown('<p class="text-sm opacity-80 mb-4">Preview your image on e-commerce platforms</p>', unsafe_allow_html=True)

if st.button("🚀 Generate Previews", type="primary", key="generate_previews"):
    if uploaded_file:
        st.markdown('<h4 class="text-lg font-semibold mb-4">📱 Platform Listings</h4>', unsafe_allow_html=True)
        is_duplicate, message, sha256, phash = check_duplicate(file_bytes, file_name)
        data = get_file_data(sha256) if is_duplicate else None
        uploader_status = 'Trusted' if data and data.get('uploader', '').lower() in trusted_uploaders else 'Untrusted'

        platforms = [
            {
                "name": "Flipkart",
                "color": "#ff6161",
                "logo": "F",
                "brand": "Peter England",
                "category": "Men's Fashion",
                "price": "₹1,499",
                "original_price": "₹2,999",
                "discount": "50% OFF",
                "rating": "4.2",
                "reviews": "1,847",
                "delivery": "Free Delivery by Tomorrow",
                "specs": {
                    "Material": "100% Cotton",
                    "Color": "Navy Blue",
                    "Sizes": "S, M, L, XL, XXL",
                    "Care": "Machine Wash"
                },
                "features": ["Cash on Delivery", "Easy Returns", "Flipkart Assured"]
            },
            {
                "name": "Amazon",
                "color": "#ff9900",
                "logo": "A",
                "brand": "Van Heusen",
                "category": "Clothing & Accessories",
                "price": "₹1,299",
                "original_price": "₹2,199",
                "discount": "41% OFF",
                "rating": "4.1",
                "reviews": "2,156",
                "delivery": "Prime Delivery Available",
                "specs": {
                    "Material": "Cotton Blend",
                    "Color": "White",
                    "Sizes": "All Sizes Available",
                    "Care": "Dry Clean"
                },
                "features": ["Prime Eligible", "Amazon's Choice", "Climate Pledge Friendly"]
            },
            {
                "name": "Myntra",
                "color": "#ff3e6c",
                "logo": "M",
                "brand": "Roadster",
                "category": "Casual Wear",
                "price": "₹999",
                "original_price": "₹1,999",
                "discount": "50% OFF",
                "rating": "4.3",
                "reviews": "956",
                "delivery": "Express Delivery in 2 Days",
                "specs": {
                    "Material": "Linen Cotton",
                    "Color": "Olive Green",
                    "Sizes": "S to XXL",
                    "Care": "Hand Wash"
                },
                "features": ["30-Day Return", "Myntra Insider", "Try & Buy"]
            }
        ]

        cols = st.columns(len(platforms))
        for i, (col, platform) in enumerate(zip(cols, platforms)):
            with col:
                st.markdown(f"""
                <div class="ecommerce-card">
                    <div class="flex items-center mb-3 pb-2 border-b border-gray-700">
                        <div class="platform-logo" style="background-color: {platform['color']};">
                            {platform['logo']}
                        </div>
                        <div>
                            <h3 class="text-base font-semibold">{platform['name']}</h3>
                            <p class="text-xs opacity-80">{platform['category']}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.image(uploaded_file, use_column_width=True)
                st.markdown(f'<p class="text-sm font-semibold">{platform['brand']} - Premium Collection</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="text-sm">Status: {uploader_status}</p>', unsafe_allow_html=True)
                col_price, col_rating = st.columns([1, 1])
                with col_price:
                    st.markdown(f"""
                    <div class="price-tag">{platform['price']}</div>
                    <div class="text-xs opacity-80 line-through">{platform['original_price']}</div>
                    <div class="text-xs text-green-400 font-semibold">{platform['discount']}</div>
                    """, unsafe_allow_html=True)
                with col_rating:
                    st.markdown(f"""
                    <div class="mt-2">
                        <div class="text-sm text-yellow-400">★★★★☆ {platform['rating']}</div>
                        <div class="text-xs opacity-80">({platform['reviews']} reviews)</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown('<p class="text-sm font-medium mt-2">Specifications:</p>', unsafe_allow_html=True)
                for spec, value in platform['specs'].items():
                    st.markdown(f'<p class="text-sm"><strong>{spec}:</strong> {value}</p>', unsafe_allow_html=True)
                st.markdown('<p class="text-sm font-medium mt-2">Features:</p>', unsafe_allow_html=True)
                for feature in platform['features']:
                    st.markdown(f'<p class="text-sm">✅ {feature}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="text-sm text-blue-400">🚚 {platform['delivery']}</p>', unsafe_allow_html=True)
                if platform['name'] == "Flipkart":
                    if st.button("🛒 Add to Cart", key=f"cart_{i}", type="primary"):
                        st.success(f"Added to {platform['name']} cart!")
                elif platform['name'] == "Amazon":
                    if st.button("⚡ Buy Now", key=f"buy_{i}", type="primary"):
                        st.success(f"Redirecting to {platform['name']}...")
                else:
                    if st.button("💳 Purchase", key=f"purchase_{i}", type="primary"):
                        st.success(f"Processing {platform['name']} order...")
    else:
        st.markdown('<div class="status-warning text-sm">⚠️ Please upload an image first.</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)