#!/usr/bin/env python3
"""Test connectivity of backend, frontend, and MongoDB"""
import asyncio
import sys
import subprocess
import time

async def test_mongodb():
    """Test MongoDB connection"""
    try:
        from pymongo import MongoClient
        client = MongoClient('mongodb+srv://khnradmin:khnr123456@cluster0.zs0yt.mongodb.net/?retryWrites=true&w=majority')
        db = client['wealth_builder']
        
        # Test connection
        client.info()
        products = db['products'].find_one()
        count = db['products'].count_documents({})
        
        print(f"✅ MongoDB: Connected successfully")
        print(f"   - Products in database: {count}")
        if count > 0:
            print(f"   - Sample product: {products.get('name', 'N/A')}")
        return True
    except Exception as e:
        print(f"❌ MongoDB: Connection failed - {e}")
        return False

async def test_backend():
    """Test backend API"""
    try:
        import urllib.request
        import json
        response = urllib.request.urlopen('http://localhost:8000/api/')
        data = response.read()
        print(f"✅ Backend: Running on port 8000")
        print(f"   - Status: {response.status}")
        return True
    except Exception as e:
        print(f"❌ Backend: Not responding on port 8000 - {e}")
        return False

def test_frontend():
    """Test frontend"""
    try:
        import urllib.request
        response = urllib.request.urlopen('http://localhost:3003')
        print(f"✅ Frontend: Running on port 3003")
        print(f"   - Status: {response.status}")
        return True
    except:
        try:
            import urllib.request
            response = urllib.request.urlopen('http://localhost:3002')
            print(f"✅ Frontend: Running on port 3002")
            print(f"   - Status: {response.status}")
            return True
        except Exception as e:
            print(f"❌ Frontend: Not responding on ports 3002/3003 - {e}")
            return False

async def main():
    print("🔍 Testing System Connectivity...\n")
    
    results = {
        'MongoDB': await test_mongodb(),
        'Backend': await test_backend(),
        'Frontend': test_frontend()
    }
    
    print("\n📊 Summary:")
    all_ok = all(results.values())
    for service, status in results.items():
        symbol = "✅" if status else "❌"
        print(f"  {symbol} {service}")
    
    if all_ok:
        print("\n🎉 All services connected successfully!")
    else:
        print("\n⚠️ Some services are not connected. Check above for details.")
    
    return 0 if all_ok else 1

if __name__ == '__main__':
    sys.exit(asyncio.run(main()))
