#!/bin/bash

# FineZ Frontend - One-Command Setup

echo "🚀 FineZ Frontend Setup"
echo "========================"
echo ""

# Check Node version
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ from https://nodejs.org"
    exit 1
fi

echo "✅ Node.js version: $(node --version)"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
npm install

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed"
echo ""

# Setup environment
if [ ! -f ".env.local" ]; then
    echo "📝 Creating .env.local..."
    cp .env.example .env.local
    echo "⚠️  Update .env.local with your Supabase credentials"
else
    echo "✅ .env.local already exists"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo ""
echo "1. Update .env.local with Supabase credentials"
echo "   - Get from: https://supabase.com/dashboard"
echo ""
echo "2. Create Supabase database tables"
echo "   - Follow: SUPABASE_SETUP.md"
echo ""
echo "3. Start development server"
echo "   - Run: npm run dev"
echo "   - Open: http://localhost:3000"
echo ""
echo "4. Test affiliate tracking"
echo "   - Open: http://localhost:3000/api/go/test-product-id"
echo ""
echo "5. Deploy to Vercel"
echo "   - Run: npm install -g vercel && vercel"
echo "   - Add environment variables in Vercel dashboard"
echo ""
echo "📚 Documentation:"
echo "   - Setup: SUPABASE_SETUP.md"
echo "   - Deploy: DEPLOYMENT_GUIDE.md"
echo "   - Testing: TESTING_GUIDE.md"
echo "   - Project: README_NEXTJS.md"
echo ""
echo "Happy coding! 🎉"
