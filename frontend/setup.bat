@echo off
REM FineZ Development Quick-Start Script for Windows
REM Run this to set up the development environment

echo.
echo ========================================
echo FineZ Development Setup
echo ========================================
echo.

REM Step 1: Install dependencies
echo [1/4] Installing dependencies...
call npm install

REM Step 2: Copy environment variables
echo.
echo [2/4] Setting up environment variables...
if not exist .env.local (
  copy .env.example .env.local
  echo Created .env.local - please edit with your API keys
) else (
  echo .env.local already exists
)

REM Step 3: Generate Prisma client
echo.
echo [3/4] Generating Prisma client...
call npm run prisma:generate

REM Step 4: Start development server
echo.
echo [4/4] Starting development server...
echo.
call npm run dev

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Copy database.sql to Supabase SQL Editor and run
echo   2. Edit .env.local with your API keys
echo   3. Test home page loads at http://localhost:3000
echo   4. Continue building from BUILD_MANIFEST.md
echo.
