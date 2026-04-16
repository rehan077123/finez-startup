import asyncio
from server import db
from pymongo.errors import ConnectionFailure

async def check_connection():
    try:
        # Test connection by pinging the database
        await db.command('ping')
        print('✅ MongoDB Atlas connection successful!')

        # Check database info
        db_info = await db.command('dbStats')
        print(f'📊 Database: {db_info.get("db", "unknown")}')
        print(f'📁 Collections: {list(await db.list_collection_names())}')

        # Check products collection
        products_count = await db.products.count_documents({})
        print(f'🛍️  Products in database: {products_count}')

        if products_count > 0:
            # Show a sample product
            sample = await db.products.find_one({}, {'_id': 0, 'title': 1, 'type': 1, 'created_at': 1})
            print(f'📋 Sample product: {sample}')
            print('✅ Products are permanently stored in MongoDB Atlas!')
        else:
            print('⚠️  No products found in database')

    except ConnectionFailure as e:
        print(f'❌ Connection failed: {e}')
    except Exception as e:
        print(f'❌ Error: {e}')

asyncio.run(check_connection())