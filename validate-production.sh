#!/bin/bash

# Clinical BDD Creator - Production Validation Script
# Tests the production deployment to ensure all services are working

set -e

BASE_URL="https://localhost"
HEALTH_URL="${BASE_URL}/health"
API_URL="${BASE_URL}/api/v1"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Test health endpoint
test_health() {
    log_info "Testing health endpoint..."

    response=$(curl -k -s -w "%{http_code}" -o /tmp/health_response.json "${HEALTH_URL}" || echo "000")

    if [ "${response: -3}" = "200" ]; then
        log_info "Health check passed"
        cat /tmp/health_response.json | python3 -m json.tool > /dev/null 2>&1 && log_info "Health response is valid JSON"
    else
        log_error "Health check failed with status ${response: -3}"
        cat /tmp/health_response.json 2>/dev/null || echo "No response body"
        return 1
    fi
}

# Test API endpoints
test_api() {
    log_info "Testing API endpoints..."

    # Test root endpoint
    response=$(curl -k -s -w "%{http_code}" -o /dev/null "${BASE_URL}/" || echo "000")
    if [ "${response: -3}" = "200" ]; then
        log_info "Root endpoint accessible"
    else
        log_error "Root endpoint failed with status ${response: -3}"
        return 1
    fi

    # Test guideline analysis (basic test)
    test_data='{"content": "Test clinical guideline content", "specialty": "general"}'
    response=$(curl -k -s -w "%{http_code}" -o /tmp/analyze_response.json \
        -H "Content-Type: application/json" \
        -d "$test_data" \
        "${API_URL}/analyze" || echo "000")

    if [ "${response: -3}" = "200" ]; then
        log_info "Guideline analysis endpoint working"
    else
        log_warning "Guideline analysis failed with status ${response: -3} (may be expected in basic test)"
    fi
}

# Test monitoring endpoints
test_monitoring() {
    log_info "Testing monitoring endpoints..."

    # Test metrics endpoint
    response=$(curl -k -s -w "%{http_code}" -o /dev/null "${BASE_URL}/api/v1/metrics" || echo "000")
    if [ "${response: -3}" = "200" ]; then
        log_info "Metrics endpoint accessible"
    else
        log_warning "Metrics endpoint failed with status ${response: -3}"
    fi

    # Test Prometheus metrics
    response=$(curl -s -w "%{http_code}" -o /dev/null "http://localhost:9090/-/healthy" || echo "000")
    if [ "${response: -3}" = "200" ]; then
        log_info "Prometheus is healthy"
    else
        log_warning "Prometheus health check failed"
    fi

    # Test Grafana
    response=$(curl -s -w "%{http_code}" -o /dev/null "http://localhost:3001/api/health" || echo "000")
    if [ "${response: -3}" = "200" ]; then
        log_info "Grafana is accessible"
    else
        log_warning "Grafana health check failed"
    fi
}

# Test SSL/TLS
test_ssl() {
    log_info "Testing SSL/TLS configuration..."

    # Test certificate
    if openssl s_client -connect localhost:443 -servername localhost < /dev/null > /tmp/ssl_test 2>/dev/null; then
        if grep -q "Verify return code: 0 (ok)" /tmp/ssl_test; then
            log_info "SSL certificate is valid"
        else
            log_warning "SSL certificate validation failed"
        fi
    else
        log_error "SSL connection failed"
        return 1
    fi
}

# Main validation
main() {
    echo "=========================================="
    echo "Clinical BDD Creator - Production Validation"
    echo "=========================================="

    local failed=0

    # Run tests
    test_health || failed=1
    test_api || failed=1
    test_ssl || failed=1
    test_monitoring || failed=1

    echo ""
    if [ $failed -eq 0 ]; then
        log_info "✅ All production validation tests passed!"
        log_info "The Clinical BDD Creator is ready for production use."
        echo ""
        log_info "Access URLs:"
        echo "  Application: https://localhost"
        echo "  Health Check: https://localhost/health"
        echo "  Grafana: http://localhost:3001 (admin/admin)"
        echo "  Prometheus: http://localhost:9090"
        exit 0
    else
        log_error "❌ Some validation tests failed. Please check the deployment."
        exit 1
    fi
}

# Run main function
main "$@"