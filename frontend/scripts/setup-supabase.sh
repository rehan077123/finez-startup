#!/bin/bash

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}FineZ Supabase Setup Script${NC}"
echo "================================"

# Check for .env.local
if [ ! -f ".env.local" ]; then
    echo -e "${YELLOW}Creating .env.local from .env.example${NC}"
    cp .env.example .env.local
fi

echo ""
echo -e "${YELLOW}Follow these steps to complete setup:${NC}"
echo ""
echo "1. Go to https://supabase.com/dashboard/new"
echo "2. Create a new project"
echo "3. Copy the project URL and Keys"
echo ""
echo "4. Edit .env.local with your Supabase credentials:"
echo "   NEXT_PUBLIC_SUPABASE_URL=<your_url>"
echo "   NEXT_PUBLIC_SUPABASE_ANON_KEY=<your_anon_key>"
echo "   SUPABASE_SERVICE_ROLE_KEY=<your_service_role_key>"
echo ""
echo "5. In your Supabase dashboard, go to SQL Editor"
echo "6. Run the SQL commands from SUPABASE_SETUP.md"
echo ""
echo "7. Run: npm install"
echo "8. Run: npm run dev"
echo ""
echo -e "${GREEN}Setup guide: see SUPABASE_SETUP.md${NC}"
