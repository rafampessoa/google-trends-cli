#!/usr/bin/env bash

# Utility functions
echo_info() {
    echo -e "\033[0;34m[INFO]\033[0m $1"
}

echo_success() {
    echo -e "\033[0;32m[SUCCESS]\033[0m $1"
}

echo_error() {
    echo -e "\033[0;31m[ERROR]\033[0m $1"
}

echo_warning() {
    echo -e "\033[0;33m[WARNING]\033[0m $1"
}

# Check Python version
check_python_version() {
    local python_version=$(python3 --version 2>&1 | cut -d" " -f2)
    local major_version=$(echo $python_version | cut -d. -f1)
    local minor_version=$(echo $python_version | cut -d. -f2)
    
    if [ "$major_version" -lt 3 ] || [ "$major_version" -eq 3 -a "$minor_version" -lt 8 ]; then
        echo_error "Python 3.8+ is required. Found Python $python_version"
        echo_info "Please install Python 3.8 or higher before continuing."
        exit 1
    else
        echo_info "Found Python $python_version"
    fi
}

# Parse command line arguments
parse_args() {
    INSTALL_TYPE="cli"  # Default to CLI-only install
    DEV_MODE=false
    
    while [[ $# -gt 0 ]]; do
        key="$1"
        case $key in
            --api)
                INSTALL_TYPE="api"
                shift
                ;;
            --all)
                INSTALL_TYPE="all"
                shift
                ;;
            --dev)
                DEV_MODE=true
                shift
                ;;
            --help)
                echo "Usage: $0 [--api] [--all] [--dev]"
                echo ""
                echo "Options:"
                echo "  --api    Install with API dependencies"
                echo "  --all    Install with all dependencies"
                echo "  --dev    Install in development mode"
                echo "  --help   Show this help message"
                exit 0
                ;;
            *)
                echo_error "Unknown option: $key"
                echo "Use --help for usage information."
                exit 1
                ;;
        esac
    done
}

# Install package
install_package() {
    echo_info "Installing package..."
    
    if [ "$DEV_MODE" = true ]; then
        echo_info "Installing in development mode with '$INSTALL_TYPE' dependencies..."
        
        if [ "$INSTALL_TYPE" = "cli" ]; then
            pip install -e .
        elif [ "$INSTALL_TYPE" = "api" ]; then
            pip install -e ".[api]"
        else  # all
            pip install -e ".[all]"
        fi
    else
        echo_info "Installing with '$INSTALL_TYPE' dependencies..."
        
        if [ "$INSTALL_TYPE" = "cli" ]; then
            pip install .
        elif [ "$INSTALL_TYPE" = "api" ]; then
            pip install ".[api]"
        else  # all
            pip install ".[all]"
        fi
    fi
    
    if [ $? -eq 0 ]; then
        echo_success "Installation complete!"
    else
        echo_error "Installation failed."
        exit 1
    fi
}

# Verify installation
verify_installation() {
    echo_info "Verifying installation..."
    
    # Check CLI
    if command -v gtrends &>/dev/null; then
        echo_success "CLI installed successfully: $(gtrends --version)"
    else
        echo_error "CLI installation verification failed."
        exit 1
    fi
    
    # Check API if installed
    if [ "$INSTALL_TYPE" = "api" ] || [ "$INSTALL_TYPE" = "all" ]; then
        if command -v gtrends-api &>/dev/null; then
            echo_success "API installed successfully"
        else
            echo_error "API installation verification failed."
            exit 1
        fi
    fi
}

# Main execution
main() {
    echo_info "Setting up Google Trends CLI/API..."
    
    # Check requirements
    check_python_version
    
    # Parse arguments
    parse_args "$@"
    
    # Install the package
    install_package
    
    # Verify installation
    verify_installation
    
    echo_success "Setup complete!"
    echo_info "Use 'gtrends --help' to see available commands."
    
    if [ "$INSTALL_TYPE" = "api" ] || [ "$INSTALL_TYPE" = "all" ]; then
        echo_info "Use 'gtrends-api' to start the API server."
    fi
}

# Run main function with all arguments
main "$@" 