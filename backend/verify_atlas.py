import asyncio
from server import db
from urllib.parse import urlparse
import os

async def verify_atlas():
    try:
        # Check connection string components
        mongo_uri = os.environ['MONGO_URI']
        parsed = urlparse(mongo_uri)

        print('Connection Details:')
        print(f'  - Protocol: {parsed.scheme}')
        print(f'  - Host: {parsed.hostname}')
        print(f'  - Database: {os.environ.get("DB_NAME", "unknown")}')

        if 'mongodb.net' in parsed.hostname:
            print('Confirmed: Connected to MongoDB Atlas')
        else:
            print('Not connected to Atlas')

        # Test data persistence by checking if we can read/write
        test_doc = {'test': 'atlas_connection', 'timestamp': '2026-03-28'}
        result = await db.test_collection.insert_one(test_doc)
        print(f'Write test successful: {result.inserted_id}')

        # Read it back
        doc = await db.test_collection.find_one({'test': 'atlas_connection'})
        if doc:
            print('Read test successful')
            # Clean up
            await db.test_collection.delete_one({'test': 'atlas_connection'})
            print('Data persistence confirmed!')
        else:
            print('Read test failed')

    except Exception as e:
        print(f'Error: {e}')

asyncio.run(verify_atlas())