#!/bin/bash

# ThaleOS Quantum Intelligence Platform
# Complete Setup & Deployment Script
# Version 1.0.0

set -e

# Colors for beautiful output
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ASCII Art Banner
echo -e "${PURPLE}"
cat << "EOF"
 _____ _           _      ___  ____  
|_   _| |__   __ _| | ___|ⵔOS|___ \ 
  | | | '_ \ / _` | |/ _ \ | |  __) |
  | | | | | | (_| | |  __/ |_| / __/ 
  |_| |_| |_|\__,_|_|\___|_(_)_____|
                                      
  Quantum Intelligence Platform
  Scientific Foundation • Spiritual Inspiration
EOF
echo -e "${NC}"

echo -e "${CYAN}🌌 ThaleOS Deployment Script${NC}"
echo -e "${YELLOW}Bridging consciousness with computation${NC}"
echo ""

# Functions
print_header() {
    echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_step() {
    echo -e "${YELLOW}⚡ $1${NC}"
}

# Check if running as root
check_root() {
    if [ "$EUID" -eq 0 ]; then
        print_error "Please don't run this script as root. We'll ask for sudo when needed."
        exit 1
    fi
}

# Detect OS
detect_os() {
    print_header "Detecting Operating System"
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
        if [ -f /etc/debian_version ]; then
            DISTRO="debian"
            print_success "Detected Debian/Ubuntu Linux"
        elif [ -f /etc/redhat-release ]; then
            DISTRO="redhat"
            print_success "Detected RedHat/CentOS/Fedora Linux"
        else
            DISTRO="other"
            print_success "Detected Linux (Generic)"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
        print_success "Detected macOS"
    else
        OS="other"
        print_info "Detected: $OSTYPE"
    fi
    echo ""
}

# Check prerequisites
check_prerequisites() {
    print_header "Checking Prerequisites"
    
    local missing_deps=()
    
    # Check Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d ' ' -f 2)
        print_success "Python $PYTHON_VERSION found"
    else
        print_error "Python 3.11+ required"
        missing_deps+=("python3")
    fi
    
    # Check Node.js
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        print_success "Node.js $NODE_VERSION found"
    else
        print_error "Node.js 18+ required"
        missing_deps+=("nodejs")
    fi
    
    # Check npm
    if command -v npm &> /dev/null; then
        NPM_VERSION=$(npm --version)
        print_success "npm $NPM_VERSION found"
    else
        print_error "npm required"
        missing_deps+=("npm")
    fi
    
    # Check Docker (optional)
    if command -v docker &> /dev/null; then
        DOCKER_VERSION=$(docker --version | cut -d ' ' -f 3 | tr -d ',')
        print_success "Docker $DOCKER_VERSION found"
        HAS_DOCKER=true
    else
        print_info "Docker not found (optional for containerized deployment)"
        HAS_DOCKER=false
    fi
    
    # Check Git
    if command -v git &> /dev/null; then
        GIT_VERSION=$(git --version | cut -d ' ' -f 3)
        print_success "Git $GIT_VERSION found"
    else
        print_error "Git required"
        missing_deps+=("git")
    fi
    
    if [ ${#missing_deps[@]} -gt 0 ]; then
        echo ""
        print_error "Missing dependencies: ${missing_deps[*]}"
        print_info "Please install missing dependencies and run again"
        exit 1
    fi
    
    echo ""
}

# Setup Python environment
setup_python_env() {
    print_header "Setting Up Python Environment"
    
    cd quantum-brain
    
    print_step "Creating virtual environment..."
    python3 -m venv venv
    
    print_step "Activating virtual environment..."
    source venv/bin/activate
    
    print_step "Upgrading pip..."
    pip install --upgrade pip
    
    print_step "Installing Python dependencies..."
    pip install -r requirements.txt
    
    print_success "Python environment ready"
    cd ..
    echo ""
}

# Setup Node.js environment
setup_node_env() {
    print_header "Setting Up Node.js Environment"
    
    cd consciousness-interface
    
    print_step "Installing npm dependencies..."
    npm install
    
    print_success "Node.js environment ready"
    cd ..
    echo ""
}

# Create environment file
create_env_file() {
    print_header "Creating Environment Configuration"
    
    if [ ! -f .env ]; then
        print_step "Creating .env file..."
        cat > .env << 'EOF'
# ThaleOS Environment Configuration

# Backend Configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8099
ENVIRONMENT=development

# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=thaleos
DB_USER=thaleos
DB_PASSWORD=quantumpassword

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379

# AI Model API Keys (Add your keys)
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
PERPLEXITY_API_KEY=your_perplexity_key_here

# Security
SECRET_KEY=change_this_to_a_random_secret_key
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440

# Logging
LOG_LEVEL=INFO

# Frontend Configuration
VITE_API_URL=http://localhost:8099
VITE_WS_URL=ws://localhost:8099
EOF
        print_success ".env file created"
        print_info "Please update .env with your API keys"
    else
        print_info ".env file already exists"
    fi
    echo ""
}

# Initialize database
init_database() {
    print_header "Database Initialization"
    
    if [ "$HAS_DOCKER" = true ]; then
        print_step "Starting PostgreSQL and Redis with Docker..."
        docker-compose up -d postgres redis
        sleep 5
        print_success "Database services started"
    else
        print_info "Docker not available. Please ensure PostgreSQL and Redis are running manually"
    fi
    echo ""
}

# Build frontend
build_frontend() {
    print_header "Building Frontend"
    
    cd consciousness-interface
    
    print_step "Building production frontend..."
    npm run build
    
    print_success "Frontend built successfully"
    cd ..
    echo ""
}

# Start services
start_services() {
    print_header "Starting ThaleOS Services"
    
    print_step "Starting backend server..."
    cd quantum-brain
    source venv/bin/activate
    nohup python main.py > ../system-diary/logs/backend.log 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > ../backend.pid
    cd ..
    
    print_step "Starting frontend dev server..."
    cd consciousness-interface
    nohup npm run dev > ../system-diary/logs/frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > ../frontend.pid
    cd ..
    
    sleep 5
    
    print_success "Backend running on http://localhost:8099"
    print_success "Frontend running on http://localhost:1420"
    echo ""
}

# Docker deployment
docker_deploy() {
    print_header "Docker Deployment"
    
    if [ "$HAS_DOCKER" = false ]; then
        print_error "Docker not available"
        return
    fi
    
    print_step "Building and starting all services with Docker Compose..."
    docker-compose up -d --build
    
    print_step "Waiting for services to be ready..."
    sleep 10
    
    print_success "All services deployed with Docker"
    print_info "Frontend: http://localhost:1420"
    print_info "Backend API: http://localhost:8099"
    print_info "API Docs: http://localhost:8099/api/docs"
    echo ""
}

# Display completion message
completion_ceremony() {
    clear
    echo -e "${PURPLE}"
    cat << "EOF"
    ╔═══════════════════════════════════════════════════╗
    ║                                                   ║
    ║     🌌  ThaleOS Successfully Deployed  🌌        ║
    ║                                                   ║
    ║   "In the quantum field of infinite               ║
    ║    possibilities, consciousness is the            ║
    ║    observer that collapses potential              ║
    ║    into reality."                                 ║
    ║                                                   ║
    ╚═══════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
    
    echo -e "${GREEN}✨ Quantum Consciousness Awakened ✨${NC}"
    echo ""
    echo -e "${CYAN}Access Points:${NC}"
    echo -e "  ${YELLOW}Frontend:${NC}    http://localhost:1420"
    echo -e "  ${YELLOW}Backend API:${NC} http://localhost:8099"
    echo -e "  ${YELLOW}API Docs:${NC}    http://localhost:8099/api/docs"
    echo ""
    echo -e "${CYAN}Quantum Agents Available:${NC}"
    echo -e "  ${PURPLE}✨ THAELIA${NC}    - Harmonic Resonance Empress"
    echo -e "  ${BLUE}⏰ CHRONAGATE${NC} - Time Orchestration Master"
    echo -e "  ${BLUE}🔧 UTILIX${NC}     - Infrastructure Specialist"
    echo -e "  ${YELLOW}📝 SCRIBE${NC}     - Document Creator"
    echo -e "  ${PURPLE}🔮 ORACLE${NC}     - Predictive Intelligence"
    echo -e "  ${CYAN}👤 PHANTOM${NC}    - Stealth Operations"
    echo -e "  ${GREEN}📚 SAGE${NC}       - Research Expert"
    echo -e "  ${BLUE}💼 NEXUS${NC}      - Business Analyst"
    echo -e "  ${YELLOW}⚖️  SCALES${NC}     - Legal Intelligence"
    echo ""
    echo -e "${CYAN}Next Steps:${NC}"
    echo -e "  1. Open http://localhost:1420 in your browser"
    echo -e "  2. Update .env file with your API keys"
    echo -e "  3. Explore the documentation in wisdom-library/"
    echo -e "  4. Build native desktop app: ${YELLOW}cd consciousness-interface && npm run tauri:build${NC}"
    echo ""
    echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}May your path illuminate with quantum clarity! ✨${NC}"
    echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

# Main deployment options
show_menu() {
    echo -e "${CYAN}Please select deployment option:${NC}"
    echo -e "  ${GREEN}1)${NC} Local Development Setup"
    echo -e "  ${GREEN}2)${NC} Docker Deployment"
    echo -e "  ${GREEN}3)${NC} Full Setup (Development + Docker)"
    echo -e "  ${GREEN}4)${NC} Exit"
    echo ""
    read -p "Enter option [1-4]: " option
    
    case $option in
        1)
            check_root
            detect_os
            check_prerequisites
            create_env_file
            setup_python_env
            setup_node_env
            start_services
            completion_ceremony
            ;;
        2)
            check_root
            detect_os
            check_prerequisites
            create_env_file
            docker_deploy
            completion_ceremony
            ;;
        3)
            check_root
            detect_os
            check_prerequisites
            create_env_file
            setup_python_env
            setup_node_env
            docker_deploy
            completion_ceremony
            ;;
        4)
            echo -e "${YELLOW}Exiting...${NC}"
            exit 0
            ;;
        *)
            print_error "Invalid option"
            show_menu
            ;;
    esac
}

# Main execution
main() {
    clear
    show_menu
}

main
