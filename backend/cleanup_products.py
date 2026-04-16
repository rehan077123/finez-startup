import os
from dotenv import load_dotenv
import pymongo

load_dotenv()
uri = os.getenv('MONGO_URI') or os.getenv('MONGO_URL')
db_name = os.getenv('DB_NAME')
if not uri or not db_name:
    raise SystemExit('MONGO_URI/DB_NAME not set')

client = pymongo.MongoClient(uri)
db = client[db_name]

result = db.products.delete_many({})
print(f'✅ Deleted {result.deleted_count} products.')
count = db.products.count_documents({})
print(f'✅ Remaining products: {count}')
client.close()
