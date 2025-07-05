# streamlit_app.py
import time
import streamlit as st
import hashlib
from uploader import upload_to_pinata
from interact import store_file_on_chain, check_file_exists, get_file_data
from PIL import Image
import io

# Page configuration
st.set_page_config(
    page_title="DeduVault - Decentralized Image Deduplication",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 0;
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        color: white;
        margin: 0.5rem 0;
    }
    
    .hash-display {
        background: #f8f9fa;
        border: 2px dashed #dee2e6;
        border-radius: 8px;
        padding: 1rem;
        font-family: 'Courier New', monospace;
        word-break: break-all;
        margin: 1rem 0;
    }
    
    .status-success {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .status-warning {
        background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .ecommerce-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 1rem;
        border: 1px solid #e0e0e0;
    }
    
    .ecommerce-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }
    
    .platform-header {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #f0f0f0;
    }
    
    .platform-logo {
        width: 40px;
        height: 40px;
        border-radius: 8px;
        margin-right: 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: white;
    }
    
    .price-tag {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 1.1rem;
        display: inline-block;
        margin: 0.5rem 0;
    }
    
    .product-specs {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .spec-item {
        display: flex;
        justify-content: space-between;
        padding: 0.25rem 0;
        border-bottom: 1px solid #dee2e6;
    }
    
    .spec-item:last-child {
        border-bottom: none;
    }
    
    .action-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 1rem;
    }
    
    .action-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .workflow-step {
        display: flex;
        align-items: center;
        margin: 1rem 0;
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 8px;
        border-left: 4px solid #667eea;
    }
    
    .step-number {
        background: #667eea;
        color: white;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 1rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("""
<div class="main-header">
    <h1 class="main-title">🔒 DeduVault</h1>
    <p class="main-subtitle">Next-Generation Decentralized Image Deduplication Platform</p>
    <p style="font-size: 1rem; margin-top: 1rem; opacity: 0.8;">
        Leveraging IPFS & Blockchain Technology for Secure, Transparent, and Efficient Digital Asset Management
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar with information
with st.sidebar:
    st.markdown("### 📊 Platform Statistics")
    st.metric("Files Processed", "12,847", "↗️ 23%")
    st.metric("Storage Saved", "2.3 TB", "↗️ 15%")
    st.metric("Active Users", "1,249", "↗️ 8%")
    
    st.markdown("---")
    st.markdown("### 🔧 How It Works")
    
    workflow_steps = [
        "Upload your image file",
        "Generate SHA-256 hash",
        "Store on IPFS network",
        "Verify on blockchain",
        "Detect duplicates instantly"
    ]
    
    for i, step in enumerate(workflow_steps, 1):
        st.markdown(f"""
        <div class="workflow-step" style="color:black">
            <div class="step-number">{i}</div>
            <div>{step}</div>
        </div>
        """, unsafe_allow_html=True)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Feature highlights
    st.markdown("### 🚀 Key Features")
    
    features = [
        {
            "title": "🔐 Cryptographic Security",
            "desc": "SHA-256 hashing ensures data integrity and uniqueness verification"
        },
        {
            "title": "🌐 IPFS Integration", 
            "desc": "Decentralized storage with content-addressed data distribution"
        },
        {
            "title": "⛓️ Blockchain Verification",
            "desc": "Immutable record keeping with transparent transaction history"
        },
        {
            "title": "⚡ Real-time Deduplication",
            "desc": "Instant duplicate detection saves storage costs and bandwidth"
        }
    ]
    
    for feature in features:
        st.markdown(f"""
        <div class="feature-card">
            <h4 style="margin-bottom: 0.5rem; color: #2c3e50;">{feature['title']}</h4>
            <p style="margin: 0; color: #7f8c8d;">{feature['desc']}</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("### 📈 Live Metrics")
    st.markdown("""
    <div class="metric-card">
        <h3>99.9%</h3>
        <p>System Uptime</p>
    </div>
    <div class="metric-card">
        <h3>< 2s</h3>
        <p>Average Processing Time</p>
    </div>
    <div class="metric-card">
        <h3>256-bit</h3>
        <p>Encryption Standard</p>
    </div>
    """, unsafe_allow_html=True)

# Upload Section
st.markdown("---")
st.markdown("### 📤 Upload & Process Image")
uploaded_file = st.file_uploader(
    "Select your image file (JPG, JPEG, PNG)",
    type=["jpg", "jpeg", "png"],
    help="Maximum file size: 10MB. Supported formats: JPG, JPEG, PNG"
)


if uploaded_file is not None and uploaded_file.size > 0:
    file_bytes = uploaded_file.read()

    # Display Preview + Info in two columns
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("#### 🖼️ Preview")
        if uploaded_file.type.startswith("image/"):
            image = Image.open(io.BytesIO(file_bytes))
            st.image(image, use_column_width=True, caption=f"Uploaded: {uploaded_file.name}")
        else:
            st.warning("⚠️ Uploaded file is not a supported image type.")

        # File information
        st.markdown("#### 📋 File Information")
        file_size = len(file_bytes)
        st.markdown(f"""
        <div class="product-specs" style="color:black">
            <div class="spec-item">
                <span><strong>Filename:</strong></span>
                <span>{uploaded_file.name}</span>
            </div>
            <div class="spec-item">
                <span><strong>Size:</strong></span>
                <span>{file_size:,} bytes ({file_size/1024:.1f} KB)</span>
            </div>
            <div class="spec-item">
                <span><strong>Type:</strong></span>
                <span>{uploaded_file.type}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("#### 🔐 Cryptographic Processing")
        file_hash = hashlib.sha256(file_bytes).hexdigest()
        st.markdown("**SHA-256 Hash:**")
        st.markdown(f"""
        <div class="hash-display">
            <code>{file_hash}</code>
        </div>
        """, unsafe_allow_html=True)

        with st.spinner("🔄 Processing file..."):
            progress_bar = st.progress(0)
            progress_bar.progress(25)
            st.write("✅ Hash generated successfully")
            time.sleep(0.5)
            progress_bar.progress(50)
            st.write("🔄 Uploading to IPFS...")

            try:
                cid = upload_to_pinata(file_bytes, uploaded_file.name)
                progress_bar.progress(75)
                st.write("✅ IPFS upload completed")
            except Exception as e:
                st.error(f"❌ IPFS upload failed: {e}")
                st.stop()

            progress_bar.progress(100)
            st.write("🔍 Checking for duplicates...")

            exists = check_file_exists(file_hash)
            if exists:
                st.markdown(f"""
                <div class="status-warning">
                    <h4>⚠️ Duplicate Detected!</h4>
                    <p>This file already exists in our blockchain registry.</p>
                </div>
                """, unsafe_allow_html=True)

                data = get_file_data(file_hash)
                if data:
                    st.markdown("#### 📊 Existing Record Details")
                    specs_html = '<div class="product-specs">'
                    specs_html += f"""
                        <div class="spec-item" style="color:black">
                            <span><strong>Original CID:</strong></span>
                            <span><code>{data.get('cid', 'N/A')}</code></span>
                        </div>
                        <div class="spec-item" style="color:black">
                            <span><strong>Uploader:</strong></span>
                            <span><code>{data.get('uploader', 'N/A')}</code></span>
                        </div>
                        <div class="spec-item" style="color:black">
                            <span><strong>Timestamp:</strong></span>
                            <span>{data.get('timestamp', 'N/A')}</span>
                        </div>
                    """
                    specs_html += '</div>'
                    st.markdown(specs_html, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="status-success">
                    <h4>✅ New Image Uploaded Successfully!</h4>
                    <p>No duplicates found.</p>
                    <p><strong>IPFS CID:</strong> <code>{cid}</code></p>
                    <p><strong>Gateway URL:</strong> <a href="https://gateway.pinata.cloud/ipfs/{cid}" target="_blank">View on IPFS</a></p>
                </div>
                """, unsafe_allow_html=True)

                with st.spinner("🔗 Recording on blockchain..."):
                    tx_hash = store_file_on_chain(file_hash, cid)

                if tx_hash:
                    st.markdown(f"""
                    <div class="status-success">
                        <h4>🎉 Blockchain Registration Complete!</h4>
                        <p><strong>Transaction Hash:</strong> <code>{tx_hash}</code></p>
                        <p>Your file is now permanently recorded on the blockchain.</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("❌ Blockchain transaction failed. Please try again.")

# E-Commerce Platform Preview
st.markdown("---")
st.markdown("### 🛒 E-Commerce Platform Preview")
st.markdown("*See how your image would appear across different e-commerce platforms*")

if st.button("🚀 Generate Platform Previews", type="primary"):
    if uploaded_file:
        st.markdown("#### 📱 Cross-Platform Product Listings")
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

        # Create columns for platform cards
        cols = st.columns(len(platforms))
        for i, (col, platform) in enumerate(zip(cols, platforms)):
            with col:
                st.markdown(f"""
                <div class="ecommerce-card">
                    <div class="platform-header">
                        <div class="platform-logo" style="background-color: {platform['color']};">
                            {platform['logo']}
                        </div>
                        <div>
                            <h3 style="margin: 0; color: #2c3e50;">{platform['name']}</h3>
                            <p style="margin: 0; color: #7f8c8d; font-size: 0.9rem;">{platform['category']}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                # Product image
                st.image(uploaded_file, use_column_width=True)
                # Product details
                st.markdown(f"**{platform['brand']}** - Premium Collection")
                # Price section
                col_price, col_rating = st.columns([1, 1])
                with col_price:
                    st.markdown(f"""
                    <div class="price-tag">{platform['price']}</div>
                    <div style="text-decoration: line-through; color: #888; margin-top: 0.25rem;">
                        {platform['original_price']} <span style="color: #27ae60; font-weight: bold;">({platform['discount']})</span>
                    </div>
                    """, unsafe_allow_html=True)
                with col_rating:
                    st.markdown(f"""
                    <div style="margin-top: 0.5rem;">
                        <div style="color: #f39c12;">★★★★☆ {platform['rating']}</div>
                        <div style="font-size: 0.8rem; color: #888;">({platform['reviews']} reviews)</div>
                    </div>
                    """, unsafe_allow_html=True)
                # Specifications
                st.markdown("**Product Specifications:**")
                for spec, value in platform['specs'].items():
                    st.markdown(f"**{spec}:** {value}")
                # Features
                st.markdown("**Key Features:**")
                for feature in platform['features']:
                    st.markdown(f"✅ {feature}")
                # Delivery info
                st.info(f"🚚 {platform['delivery']}")
                # Action buttons
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
        st.warning("⚠️ Please upload an image first to generate platform previews.")
