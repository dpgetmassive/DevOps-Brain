---
name: project-testing
version: 1.0.0
description: When the user wants to validate testing requirements, check test coverage, create test plans, or ensure CI/CD testing is configured. Also use when the user mentions "testing requirements," "test plan," "test coverage," "test validation," "testing checklist," or "CI/CD testing."
---

# Project Testing

You are an expert in testing requirements and validation. You ensure projects have proper test coverage, CI/CD integration, and testing documentation.

## Guard Rails

**Auto-approve**: Running tests, checking coverage, reviewing test plans, validating CI/CD config
**Confirm first**: Modifying test thresholds, changing coverage requirements, deleting tests

---

## Prerequisites

**Read `context/infrastructure-context.md` first** to understand the environment.

**Read `context/projects-registry.md`** to see active projects.

**Required context**:
- Project directory: `projects/{project-name}/`
- Tests directory: `projects/{project-name}/tests/`
- CI workflow: `projects/{project-name}/.github/workflows/ci.yml`

---

## Testing Checklist Validation

### Check Testing Completeness

```bash
PROJECT_NAME="monitoring-dashboard"
PROJECT_DIR="projects/${PROJECT_NAME}"

# Required testing files
REQUIRED_FILES=(
  "tests/unit/"
  "tests/integration/"
  ".github/workflows/ci.yml"
)

MISSING_FILES=()

for file in "${REQUIRED_FILES[@]}"; do
  if [ ! -d "${PROJECT_DIR}/${file}" ] && [ ! -f "${PROJECT_DIR}/${file}" ]; then
    MISSING_FILES+=("${file}")
  fi
done

if [ ${#MISSING_FILES[@]} -gt 0 ]; then
  echo "⚠️ Missing testing files/directories:"
  printf '  - %s\n' "${MISSING_FILES[@]}"
else
  echo "✅ All required testing files present"
fi
```

### Validate Test Plan

```bash
TEST_PLAN="${PROJECT_DIR}/tests/README.md"

if [ ! -f "${TEST_PLAN}" ]; then
  echo "⚠️ Test plan not found"
else
  # Check for required sections
  REQUIRED_SECTIONS=(
    "Test Strategy"
    "Unit Tests"
    "Integration Tests"
    "E2E Tests"
    "Coverage Requirements"
  )
  
  for section in "${REQUIRED_SECTIONS[@]}"; do
    if ! grep -q "## ${section}" "${TEST_PLAN}"; then
      echo "⚠️ Missing section: ${section}"
    fi
  done
fi
```

---

## Test Coverage Validation

### Check Coverage (Language-Specific)

**Python**:
```bash
# Run pytest with coverage
cd "${PROJECT_DIR}"
pytest --cov=. --cov-report=term-missing --cov-report=html

# Check coverage threshold (example: 80%)
COVERAGE=$(pytest --cov=. --cov-report=term | grep "TOTAL" | awk '{print $NF}' | sed 's/%//')
THRESHOLD=80

if (( $(echo "${COVERAGE} < ${THRESHOLD}" | bc -l) )); then
  echo "⚠️ Coverage ${COVERAGE}% below threshold ${THRESHOLD}%"
else
  echo "✅ Coverage ${COVERAGE}% meets threshold"
fi
```

**JavaScript/TypeScript**:
```bash
# Run jest with coverage
npm test -- --coverage

# Check coverage threshold
COVERAGE=$(npm test -- --coverage --json | jq '.coverageMap.total.lines.pct')
THRESHOLD=80

if (( $(echo "${COVERAGE} < ${THRESHOLD}" | bc -l) )); then
  echo "⚠️ Coverage ${COVERAGE}% below threshold ${THRESHOLD}%"
fi
```

**Go**:
```bash
# Run tests with coverage
go test -coverprofile=coverage.out ./...

# Check coverage
COVERAGE=$(go tool cover -func=coverage.out | grep total | awk '{print $3}' | sed 's/%//')
THRESHOLD=80

if (( $(echo "${COVERAGE} < ${THRESHOLD}" | bc -l) )); then
  echo "⚠️ Coverage ${COVERAGE}% below threshold ${THRESHOLD}%"
fi
```

---

## CI/CD Testing Validation

### Check GitHub Actions Workflow

```bash
CI_WORKFLOW="${PROJECT_DIR}/.github/workflows/ci.yml"

if [ ! -f "${CI_WORKFLOW}" ]; then
  echo "⚠️ CI workflow not found"
else
  # Check for test job
  if ! grep -q "test:" "${CI_WORKFLOW}"; then
    echo "⚠️ No test job in CI workflow"
  fi
  
  # Check for coverage reporting
  if ! grep -q "coverage" "${CI_WORKFLOW}"; then
    echo "⚠️ No coverage reporting in CI workflow"
  fi
  
  # Check for test matrix (if applicable)
  if grep -q "strategy:" "${CI_WORKFLOW}" && ! grep -q "matrix:" "${CI_WORKFLOW}"; then
    echo "ℹ️ Consider adding test matrix for multiple versions"
  fi
fi
```

### Validate Workflow Syntax

```bash
# Check YAML syntax
yamllint "${CI_WORKFLOW}" 2>/dev/null || echo "⚠️ YAML syntax issues (install yamllint for details)"

# Validate with GitHub Actions validator (requires actionlint)
# actionlint "${CI_WORKFLOW}" || echo "⚠️ Workflow validation issues"
```

---

## Generate Test Templates

### Test Plan Template

```bash
cat > "${PROJECT_DIR}/tests/README.md" << EOF
# Testing: ${PROJECT_NAME}

## Test Strategy

[Overall testing approach]

## Unit Tests

### Coverage
- Target: 80% code coverage
- Current: [run tests to get coverage]

### Running Tests
\`\`\`bash
[unit test command]
\`\`\`

## Integration Tests

### Scope
[What is tested]

### Running Tests
\`\`\`bash
[integration test command]
\`\`\`

## E2E Tests

### Scope
[What is tested]

### Running Tests
\`\`\`bash
[e2e test command]
\`\`\`

## Coverage Requirements

- **Minimum**: 80% overall coverage
- **Critical paths**: 100% coverage
- **New code**: 90% coverage

## Test Data

- **Location**: [test data location]
- **Management**: [how test data is managed]

## CI/CD Integration

Tests run automatically on:
- Pull requests
- Pushes to main/develop
- Scheduled (nightly)

See [.github/workflows/ci.yml](../.github/workflows/ci.yml)
EOF
```

### Unit Test Template (Python)

```bash
cat > "${PROJECT_DIR}/tests/unit/test_example.py" << EOF
"""
Unit tests for [module]
"""
import pytest
from [module] import [function]


class TestExample:
    """Test suite for [function]"""
    
    def test_basic_functionality(self):
        """Test basic functionality"""
        result = [function]()
        assert result is not None
    
    def test_edge_case(self):
        """Test edge case"""
        with pytest.raises(ValueError):
            [function](invalid_input)
    
    @pytest.mark.parametrize("input,expected", [
        (1, 2),
        (2, 4),
        (3, 6),
    ])
    def test_with_parameters(self, input, expected):
        """Test with parameters"""
        assert [function](input) == expected
EOF
```

### Integration Test Template

```bash
cat > "${PROJECT_DIR}/tests/integration/test_integration.py" << EOF
"""
Integration tests for [component]
"""
import pytest


@pytest.fixture
def test_client():
    """Setup test client"""
    # Setup code
    yield client
    # Teardown code


def test_component_integration(test_client):
    """Test component integration"""
    # Test code
    assert True
EOF
```

---

## Test Environment Setup

### Docker Compose for Testing

```bash
cat > "${PROJECT_DIR}/tests/docker-compose.test.yml" << EOF
version: '3.8'

services:
  test-db:
    image: postgres:15
    environment:
      POSTGRES_DB: testdb
      POSTGRES_USER: testuser
      POSTGRES_PASSWORD: testpass
    ports:
      - "5432:5432"
  
  test-redis:
    image: redis:7
    ports:
      - "6379:6379"
EOF
```

### Test Configuration

```bash
cat > "${PROJECT_DIR}/tests/conftest.py" << EOF
"""
Pytest configuration and fixtures
"""
import pytest
import os


@pytest.fixture(scope="session")
def test_config():
    """Test configuration"""
    return {
        "database_url": os.getenv("TEST_DATABASE_URL", "postgresql://testuser:testpass@localhost/testdb"),
        "redis_url": os.getenv("TEST_REDIS_URL", "redis://localhost:6379"),
    }
EOF
```

---

## CI/CD Testing Examples

### GitHub Actions Test Workflow

```bash
cat >> "${PROJECT_DIR}/.github/workflows/ci.yml" << EOF

  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    # Setup (customize for your language)
    - name: Setup Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    # Install dependencies
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    # Run tests
    - name: Run tests
      run: pytest --cov=. --cov-report=xml
    
    # Upload coverage
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
    
    # Coverage threshold check
    - name: Check coverage threshold
      run: |
        COVERAGE=\$(pytest --cov=. --cov-report=term | grep "TOTAL" | awk '{print \$NF}' | sed 's/%//')
        THRESHOLD=80
        if (( \$(echo "\$COVERAGE < \$THRESHOLD" | bc -l) )); then
          echo "⚠️ Coverage \$COVERAGE% below threshold \$THRESHOLD%"
          exit 1
        fi
EOF
```

---

## Testing Checklist

### Pre-Deployment Testing

```bash
cat > "${PROJECT_DIR}/compliance/testing-checklist.md" << EOF
# Testing Checklist

## Unit Tests
- [ ] Unit tests written for all functions
- [ ] Unit test coverage >= 80%
- [ ] Edge cases covered
- [ ] Error handling tested

## Integration Tests
- [ ] Integration tests for key workflows
- [ ] External dependencies mocked/stubbed
- [ ] Database integration tested (if applicable)
- [ ] API integration tested (if applicable)

## E2E Tests
- [ ] Critical user flows tested
- [ ] E2E test environment configured
- [ ] Test data prepared

## CI/CD
- [ ] Tests run in CI pipeline
- [ ] Coverage reporting configured
- [ ] Test failures block merge
- [ ] Test results visible in PR

## Performance
- [ ] Performance tests written (if applicable)
- [ ] Load tests configured (if applicable)
- [ ] Performance benchmarks documented

## Security
- [ ] Security tests written (if applicable)
- [ ] Vulnerability scanning in CI (if applicable)
EOF
```

---

## Verify After

1. **Test files exist**: Check tests directory structure
2. **CI configured**: Verify GitHub Actions workflow
3. **Coverage meets threshold**: Check coverage percentage
4. **Tests pass**: Run test suite

---

## Rollback

Test changes are version-controlled. Rollback via git:

```bash
git checkout HEAD -- "${PROJECT_DIR}/tests/"
```

---

## Troubleshooting

### Tests failing in CI but passing locally
- Check environment differences
- Verify dependencies are installed
- Check for flaky tests

### Coverage below threshold
- Identify untested code paths
- Add tests for missing coverage
- Review coverage report

### CI workflow not running
- Check workflow file syntax
- Verify workflow triggers
- Check GitHub Actions permissions

---

## Related Skills

- **project-initiation** - Creates initial test structure
- **github-actions** - CI/CD pipeline configuration
- **project-compliance** - Validates testing requirements
- **container-ops** - Container testing strategies
