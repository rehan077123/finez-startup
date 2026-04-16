import asyncio
from server import db

async def check_atlas_details():
    try:
        # Get server info
        server_info = await db.command('serverStatus')
        print('🔍 MongoDB Server Info:')
        print(f'  • Host: {server_info.get("host", "unknown")}')
        print(f'  • Version: {server_info.get("version", "unknown")}')
        print(f'  • Process: {server_info.get("process", "unknown")}')

        # Check if it's Atlas
        if 'mongodb.net' in str(server_info.get('host', '')):
            print('✅ Confirmed: Connected to MongoDB Atlas cluster')
        else:
            print('⚠️  Not connected to Atlas')

        # Check data persistence
        stats = await db.command('dbStats')
        print(f'📊 Database Storage: {stats.get("dataSize", 0)} bytes')
        print(f'📊 Collections: {stats.get("collections", 0)}')
        print(f'📊 Documents: {stats.get("objects", 0)}')

    except Exception as e:
        print(f'❌ Error: {e}')

asyncio.run(check_atlas_details())