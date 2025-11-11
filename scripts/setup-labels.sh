#!/bin/bash

# GitHub Labels Setup Script
# This script creates all labels defined in LABELS.md for the Clinical BDD Creator project

set -e

echo "=================================================="
echo "Clinical BDD Creator - GitHub Labels Setup"
echo "=================================================="
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) is not installed."
    echo "Please install it from: https://cli.github.com/"
    exit 1
fi

# Check if user is authenticated
if ! gh auth status &> /dev/null; then
    echo "❌ You are not authenticated with GitHub CLI."
    echo "Please run: gh auth login"
    exit 1
fi

echo "✅ GitHub CLI is installed and authenticated"
echo ""
echo "This script will create the following label categories:"
echo "  - Type labels (8)"
echo "  - Status labels (8)"
echo "  - Priority labels (4)"
echo "  - Area labels (9)"
echo "  - Agent labels (8)"
echo "  - Effort labels (6)"
echo "  - Clinical labels (5)"
echo "  - Special labels (7)"
echo ""
echo "Total: 55 labels"
echo ""

read -p "Do you want to proceed? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Setup cancelled"
    exit 0
fi

echo ""
echo "Creating labels..."
echo ""

# Function to create label with error handling
create_label() {
    local name="$1"
    local color="$2"
    local description="$3"
    
    if gh label create "$name" --color "$color" --description "$description" 2>/dev/null; then
        echo "✅ Created: $name"
    else
        echo "⚠️  Already exists or error: $name"
    fi
}

# Type labels
echo "📝 Creating Type labels..."
create_label "type: feature" "0075ca" "New feature or enhancement"
create_label "type: bug" "d73a4a" "Bug report or fix"
create_label "type: task" "1d76db" "Development task or work item"
create_label "type: documentation" "0075ca" "Documentation improvements"
create_label "type: refactor" "fbca04" "Code refactoring"
create_label "type: security" "ee0701" "Security issue or improvement"
create_label "type: performance" "d876e3" "Performance improvement"
create_label "type: test" "5319e7" "Testing related"

# Status labels
echo ""
echo "📊 Creating Status labels..."
create_label "status: needs-triage" "ffffff" "Needs initial review and categorization"
create_label "status: planned" "0e8a16" "Approved and in backlog"
create_label "status: in-progress" "fbca04" "Actively being worked on"
create_label "status: blocked" "d93f0b" "Blocked by dependencies"
create_label "status: review" "d876e3" "In code review"
create_label "status: stale" "cccccc" "No recent activity"
create_label "status: wont-fix" "ffffff" "Will not be addressed"
create_label "status: duplicate" "cfd3d7" "Duplicate of another issue"

# Priority labels
echo ""
echo "🎯 Creating Priority labels..."
create_label "priority: p0-critical" "b60205" "🔴 Critical - Blocking/Security/Data loss"
create_label "priority: p1-high" "d93f0b" "🟠 High priority"
create_label "priority: p2-medium" "fbca04" "🟡 Medium priority"
create_label "priority: p3-low" "0e8a16" "🟢 Low priority"

# Area labels
echo ""
echo "🗂️  Creating Area labels..."
create_label "area: santiago-service" "1d76db" "Santiago NeuroSymbolic service"
create_label "area: bdd-framework" "0075ca" "BDD testing framework"
create_label "area: testing" "5319e7" "Testing infrastructure"
create_label "area: documentation" "0075ca" "Documentation"
create_label "area: devops" "006b75" "DevOps and deployment"
create_label "area: clinical-knowledge" "c5def5" "Clinical knowledge graphs"
create_label "area: api" "d876e3" "API development"
create_label "area: mcp" "5319e7" "Model Context Protocol"
create_label "area: fhir" "c5def5" "FHIR integration"

# Agent labels
echo ""
echo "🤖 Creating Agent labels..."
create_label "agent: human" "000000" "👤 Requires human judgment"
create_label "agent: development" "0052cc" "🤖 General development agent"
create_label "agent: clinical-informaticist" "006b75" "🏥 Clinical domain expert agent"
create_label "agent: neurosymbolic-architect" "5319e7" "🧬 NeuroSymbolic architecture agent"
create_label "agent: qa" "0e8a16" "✅ Quality assurance agent"
create_label "agent: product-manager" "fbca04" "📊 Product manager agent"
create_label "agent: devops" "1d76db" "🔧 DevOps expert agent"
create_label "agent: monetization" "d876e3" "💰 Monetization expert agent"

# Effort labels
echo ""
echo "⏱️  Creating Effort labels..."
create_label "effort: xs" "c5def5" "< 2 hours"
create_label "effort: s" "bfd4f2" "2-4 hours"
create_label "effort: m" "9cc4e4" "4-8 hours"
create_label "effort: l" "7cb4da" "1-2 days"
create_label "effort: xl" "5da5cf" "2-5 days"
create_label "effort: xxl" "3e95c5" "> 1 week"

# Clinical labels
echo ""
echo "🏥 Creating Clinical labels..."
create_label "clinical: safety-critical" "b60205" "Affects patient safety"
create_label "clinical: accuracy-required" "d93f0b" "Requires clinical validation"
create_label "clinical: evidence-based" "0e8a16" "Follows evidence-based guidelines"
create_label "clinical: fhir-compliant" "0075ca" "Must comply with FHIR standards"
create_label "clinical: terminology" "c5def5" "Involves clinical terminology"

# Special labels
echo ""
echo "⭐ Creating Special labels..."
create_label "good first issue" "7057ff" "Good for newcomers"
create_label "help wanted" "008672" "Extra attention needed"
create_label "keep-open" "0e8a16" "Prevent stale bot from closing"
create_label "breaking-change" "d93f0b" "Breaking API or interface change"
create_label "needs-discussion" "d876e3" "Needs team discussion"
create_label "experiment" "fbca04" "Experimental feature"
create_label "technical-debt" "d93f0b" "Technical debt to address"

echo ""
echo "=================================================="
echo "✅ Label setup complete!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. Review labels at: https://github.com/hankh95/clinical-bdd-creator/labels"
echo "2. Update issue templates if needed"
echo "3. Start using labels in new issues"
echo ""
