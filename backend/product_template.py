# Template for Adding New Products
# Copy this template 20 times and fill with your products

ADDITIONAL_PRODUCTS = [
    {
        "title": "Your Product Name Here",
        "description": "Full product description explaining what it is and "
                       "what it does. Make it compelling!",
        "why_this_product": "⚡ The main benefit - why someone should click "
        "(e.g., Save 50% today!)",
        "price": 29.99,  # Price in USD, or 0 for free
        "original_price": 49.99,  # Optional - for showing discount
        # Choose: AI Tools, Tech, Side Hustles, Fashion, Learn, Fitness, Home
        "category": "AI Tools",
        "type": "affiliate",  # Choose: affiliate, marketplace, dropshipping, idea
        "affiliate_link": "https://example.com?ref=YOUR_AFFILIATE_ID",
        # Which network: Amazon, Flipkart, Cuelinks, etc.
        "affiliate_network": "Amazon",
        "image_url": "https://images.unsplash.com/photo-XXXXX",  # Get from Unsplash
        "featured": False,  # Set True for top picks
        "premium": False,  # Set True for premium badge
    },
    # Example Product 1: Adobe Creative Cloud
    {
        "title": "Adobe Creative Cloud All Apps",
        "description": "Complete suite of 20+ creative apps including Photoshop, "
                       "Illustrator, Premiere Pro, After Effects. Industry-standard "
                       "tools used by professionals worldwide.",
        "why_this_product": "🎨 Create pro-level designs in minutes - 50% student "
        "discount available",
        "price": 54.99,
        "original_price": 79.99,
        "category": "Tech",
        "type": "affiliate",
        "affiliate_link": "https://www.adobe.com/creativecloud.html?ref=YOUR_ID",
        "affiliate_network": "Adobe Affiliates",
        "image_url": "https://images.unsplash.com/photo-1626785774573-4b799315345d?w=500&h=300&fit=crop",
        "featured": False,
        "premium": False,
    },
    # Example Product 2: Udemy Python Course
    {
        "title": "Complete Python Bootcamp 2026",
        "description": "Learn Python from zero to hero. Build 12 real-world projects. "
                       "200+ hours of content. Lifetime access. Perfect for beginners.",
        "why_this_product": "💻 Learn Python in 30 days - 90% OFF limited time",
        "price": 13.99,
        "original_price": 129.99,
        "category": "Learn",
        "type": "affiliate",
        "affiliate_link": "https://www.udemy.com/course/complete-python-bootcamp/?ref=YOUR_ID",
        "affiliate_network": "Udemy",
        "image_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=500&h=300&fit=crop",
        "featured": False,
        "premium": False,
    },
    # ADD 18 MORE PRODUCTS BELOW (Copy the template above)
]

# To add these to your database:
# 1. Copy products to /app/backend/seed_data.py
# 2. Add to SEED_PRODUCTS list
# 3. Run: cd /app/backend && python seed_data.py
