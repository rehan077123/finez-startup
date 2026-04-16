#!/usr/bin/env python3
"""
Test FineZ Decision Engine API endpoints
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def test_endpoint(method: str, endpoint: str, data: Dict[str, Any] = None, expected_status: int = 200):
    """Test an API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    print(f"\n{Colors.BLUE}Testing:{Colors.END} {method} {endpoint}")
    
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        else:
            print(f"{Colors.RED}Unknown method: {method}{Colors.END}")
            return False
        
        if response.status_code == expected_status:
            print(f"{Colors.GREEN}✓ Status {response.status_code}{Colors.END}")
            
            # Try to parse JSON if available
            try:
                result = response.json()
                if isinstance(result, dict):
                    print(f"{Colors.YELLOW}Response keys:{Colors.END} {', '.join(result.keys())}")
                    
                    # Show summary for list responses
                    if 'stacks' in result and isinstance(result['stacks'], list):
                        print(f"  → Found {len(result['stacks'])} stacks")
                    elif 'products' in result and isinstance(result['products'], list):
                        print(f"  → Found {len(result['products'])} products")
                    elif 'acknowledged' in result:
                        print(f"  → Acknowledged: {result['acknowledged']}")
                        
            except:
                print(f"{Colors.YELLOW}Response:{Colors.END} {response.text[:100]}")
            
            return True
        else:
            print(f"{Colors.RED}✗ Status {response.status_code}{Colors.END}")
            print(f"{Colors.RED}Error:{Colors.END} {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"{Colors.RED}✗ Exception:{Colors.END} {str(e)}")
        return False

def main():
    print(f"\n{Colors.BLUE}{'='*60}")
    print("FineZ Decision Engine API Test Suite")
    print(f"{'='*60}{Colors.END}\n")
    
    # Test 1: Get all outcome stacks
    test_endpoint("GET", "/stacks/outcomes")
    
    # Test 2: Get specific stack (dropshipping-2026)
    test_endpoint("GET", "/stacks/outcomes/dropshipping-2026")
    
    # Test 3: Get specific stack (ai-creator-stack)
    test_endpoint("GET", "/stacks/outcomes/ai-creator-stack")
    
    # Test 4: Get specific stack (affiliate-mastery)
    test_endpoint("GET", "/stacks/outcomes/affiliate-mastery")
    
    # Test 5: Get specific stack (youtube-automation)
    test_endpoint("GET", "/stacks/outcomes/youtube-automation")
    
    # Test 6: Get specific stack (budget-office-setup)
    test_endpoint("GET", "/stacks/outcomes/budget-office-setup")
    
    # Test 7: Get specific stack (gym-transformation)
    test_endpoint("GET", "/stacks/outcomes/gym-transformation")
    
    # Test 8: Track engagement - view
    test_endpoint("POST", "/stacks/track-engagement", {
        "stack_id": "dropshipping-2026",
        "action": "view"
    }, expected_status=200)
    
    # Test 9: Track engagement - explore
    test_endpoint("POST", "/stacks/track-engagement", {
        "stack_id": "ai-creator-stack",
        "action": "explore"
    }, expected_status=200)
    
    # Test 10: Track engagement - add_to_cart
    test_endpoint("POST", "/stacks/track-engagement", {
        "stack_id": "affiliate-mastery",
        "action": "add_to_cart"
    }, expected_status=200)
    
    # Test 11: Get admin analytics (should work if no auth required in dev)
    test_endpoint("GET", "/admin/stacks/analytics", expected_status=200)
    
    print(f"\n{Colors.BLUE}{'='*60}")
    print("Test Suite Complete!")
    print(f"{'='*60}{Colors.END}\n")

if __name__ == "__main__":
    main()
