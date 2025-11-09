#!/bin/bash

# Clinical BDD Creator - Production Deployment Script
# This script handles the complete production deployment process

set -e

# Configuration
PROJECT_NAME="clinical-bdd-creator"
DOCKER_COMPOSE_FILE="docker-compose.yml"
ENVIRONMENT="production"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Pre-deployment checks
pre_deployment_checks() {
    log_info "Running pre-deployment checks..."

    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi

    # Check if Docker Compose is installed
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        log_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi

    # Check if required files exist
    required_files=("Dockerfile" "docker-compose.yml" "requirements.txt")
    for file in "${required_files[@]}"; do
        if [ ! -f "$file" ]; then
            log_error "Required file $file not found."
            exit 1
        fi
    done

    log_success "Pre-deployment checks passed."
}

# Generate SSL certificates (self-signed for development)
generate_ssl_certificates() {
    log_info "Generating SSL certificates..."

    if [ ! -f "nginx/ssl/cert.pem" ] || [ ! -f "nginx/ssl/key.pem" ]; then
        mkdir -p nginx/ssl
        openssl req -x509 -newkey rsa:4096 -keyout nginx/ssl/key.pem -out nginx/ssl/cert.pem -days 365 -nodes -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
        log_success "SSL certificates generated."
    else
        log_info "SSL certificates already exist."
    fi
}

# Build and deploy
deploy() {
    log_info "Starting deployment..."

    # Stop existing containers
    log_info "Stopping existing containers..."
    docker-compose down || true

    # Build images
    log_info "Building Docker images..."
    docker-compose build --no-cache

    # Start services
    log_info "Starting services..."
    docker-compose up -d

    # Wait for services to be healthy
    log_info "Waiting for services to be healthy..."
    sleep 30

    # Check service health
    check_services_health

    log_success "Deployment completed successfully!"
}

# Check service health
check_services_health() {
    log_info "Checking service health..."

    # Check main application
    if curl -f -k https://localhost/health &> /dev/null; then
        log_success "Main application is healthy."
    else
        log_warning "Main application health check failed."
    fi

    # Check Grafana
    if curl -f http://localhost:3001/api/health &> /dev/null; then
        log_success "Grafana is healthy."
    else
        log_warning "Grafana health check failed."
    fi

    # Check Prometheus
    if curl -f http://localhost:9090/-/healthy &> /dev/null; then
        log_success "Prometheus is healthy."
    else
        log_warning "Prometheus health check failed."
    fi
}

# Show deployment status
show_status() {
    log_info "Deployment status:"
    docker-compose ps

    echo ""
    log_info "Service URLs:"
    echo "  Main Application: https://localhost"
    echo "  Health Check: https://localhost/health"
    echo "  Grafana: http://localhost:3001 (admin/admin)"
    echo "  Prometheus: http://localhost:9090"
}

# Run integration tests
run_integration_tests() {
    log_info "Running integration tests..."

    # Run tests inside container
    docker-compose exec -T clinical-bdd-creator python integration_test_runner.py --ci-mode

    if [ $? -eq 0 ]; then
        log_success "Integration tests passed."
    else
        log_error "Integration tests failed."
        exit 1
    fi
}

# Main deployment process
main() {
    echo "=========================================="
    echo "Clinical BDD Creator - Production Deployment"
    echo "=========================================="

    case "${1:-deploy}" in
        "deploy")
            pre_deployment_checks
            generate_ssl_certificates
            deploy
            show_status
            ;;
        "test")
            run_integration_tests
            ;;
        "status")
            show_status
            ;;
        "stop")
            log_info "Stopping services..."
            docker-compose down
            log_success "Services stopped."
            ;;
        "restart")
            log_info "Restarting services..."
            docker-compose restart
            sleep 10
            check_services_health
            show_status
            ;;
        "logs")
            docker-compose logs -f "${2:-clinical-bdd-creator}"
            ;;
        *)
            echo "Usage: $0 {deploy|test|status|stop|restart|logs [service]}"
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"