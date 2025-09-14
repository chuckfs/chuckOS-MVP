#!/bin/bash
# Jaymi AI File Assistant - Deployment Script

echo "🚀 Starting Jaymi AI File Assistant deployment..."

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check dependencies
echo "📋 Checking dependencies..."

if ! command_exists python3; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

if ! command_exists node; then
    echo "❌ Node.js is required but not installed."
    exit 1
fi

if ! command_exists npm; then
    echo "❌ npm is required but not installed."
    exit 1
fi

echo "✅ All dependencies found"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
cd frontend
npm install

# Build frontend for production
echo "🏗️ Building frontend for production..."
npm run build

cd ..

# Create startup script
echo "📝 Creating startup script..."
cat > start_jaymi.sh << 'EOF'
#!/bin/bash
echo "🤖 Starting Jaymi AI File Assistant..."

# Start backend server
echo "🔧 Starting backend server on port 8000..."
cd "$(dirname "$0")"
python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Start frontend development server (for development)
echo "🎨 Starting frontend development server on port 3000..."
cd frontend
npm start &
FRONTEND_PID=$!

echo "✅ Jaymi AI is running!"
echo "🌐 Backend API: http://localhost:8000"
echo "🎯 Frontend App: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for interrupt
trap 'echo "🛑 Stopping services..."; kill $BACKEND_PID $FRONTEND_PID; exit' INT
wait
EOF

chmod +x start_jaymi.sh

# Create production startup script
cat > start_production.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting Jaymi AI File Assistant (Production Mode)..."

# Start backend server
echo "🔧 Starting backend server..."
cd "$(dirname "$0")"
python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4 &
BACKEND_PID=$!

# Serve frontend build (using a simple HTTP server)
echo "🎨 Serving frontend..."
cd frontend/build
python3 -m http.server 3000 &
FRONTEND_PID=$!

echo "✅ Jaymi AI is running in production mode!"
echo "🌐 Application: http://localhost:3000"
echo "🔧 API: http://localhost:8000"

trap 'echo "🛑 Stopping services..."; kill $BACKEND_PID $FRONTEND_PID; exit' INT
wait
EOF

chmod +x start_production.sh

echo "✅ Deployment complete!"
echo ""
echo "🎯 To start Jaymi AI (development mode):"
echo "   ./start_jaymi.sh"
echo ""
echo "🚀 To start Jaymi AI (production mode):"
echo "   ./start_production.sh"
echo ""
echo "📚 Access the application at:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"