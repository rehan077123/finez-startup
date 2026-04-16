import asyncio
from server import db

async def check_products():
    products = await db.products.find({}).to_list(length=None)
    print(f'Total products: {len(products)}')
    if products:
        print('Sample product:', products[0])
        # Count by type
        types = {}
        for p in products:
            t = p.get('type', 'unknown')
            types[t] = types.get(t, 0) + 1
        print('Products by type:', types)
    else:
        print('No products found')

asyncio.run(check_products())