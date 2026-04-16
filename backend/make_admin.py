import asyncio
from server import db

async def make_admin():
    # Find the first user and make them admin
    user = await db.users.find_one({})
    if user:
        await db.users.update_one({'id': user['id']}, {'$set': {'is_admin': True}})
        print(f'✅ Made user {user.get("email", user["id"])} an admin')
    else:
        print('❌ No users found in database')

asyncio.run(make_admin())