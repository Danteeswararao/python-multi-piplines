# Hello World Web Application

A simple Flask web application that displays "Hello, World!" with a modern UI and REST API endpoints.

## Features

- Modern responsive web interface
- REST API endpoint (`/api/hello`)
- Health check endpoint (`/health`)
- Comprehensive logging
- Unit and integration tests
- CI/CD pipeline with Jenkins
- RPM packaging for deployment

## Project Structure

```
helloworld-webapp/
├── helloworld/
│   ├── __init__.py
│   ├── app.py              # Main Flask application
│   └── templates/
│       └── index.html      # HTML template
├── tests/
│   ├── __init__.py
│   ├── test_app.py         # Unit tests
│   └── test_integration.py # Integration tests
├── pyproject.toml          # Poetry configuration
├── Jenkinsfile            # CI/CD pipeline
└── README.md
```

## Development Setup

### Prerequisites

- Python 3.8+
- Poetry (for dependency management)

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   poetry install
   ```

3. Run the application:
   ```bash
   poetry run python helloworld/app.py
   ```

4. Visit `http://localhost:5000` in your browser

## API Endpoints

- `GET /` - Main web page
- `GET /api/hello` - JSON API endpoint
- `GET /health` - Health check endpoint

## Testing

### Unit Tests
```bash
poetry run pytest tests/test_app.py -v
```

### Integration Tests
```bash
poetry run pytest tests/test_integration.py -v
```

### All Tests with Coverage
```bash
poetry run pytest --cov=helloworld --cov-report=html
```

## Code Quality

### Linting
```bash
poetry run flake8 helloworld/
poetry run black helloworld/
```

### Security Scan
```bash
pip install safety bandit
safety check
bandit -r helloworld/
```

## Building

### Python Package
```bash
poetry build
```

### RPM Package
The Jenkins pipeline automatically builds RPM packages for deployment.

## CI/CD Pipeline

The Jenkins pipeline includes the following stages:

1. **Checkout** - Get source code
2. **Setup Environment** - Install Poetry and dependencies
3. **Build** - Create Python package
4. **Code Quality Check** - Linting and security scanning
5. **Unit Testing** - Run unit tests with coverage
6. **Integration Testing** - Run integration tests
7. **SonarQube Analysis** - Code quality analysis
8. **Quality Gate** - Wait for SonarQube quality gate
9. **Build RPM Package** - Create deployment package
10. **Deploy to Staging** - Deploy to staging environment (main branch only)

## Deployment

The application can be deployed using the generated RPM package:

```bash
sudo rpm -ivh helloworld-webapp-0.1.0-1.noarch.rpm
sudo systemctl start helloworld-webapp
sudo systemctl enable helloworld-webapp
```

## Configuration

### Jenkins Requirements

- SonarQube server configured
- SonarQube token stored as Jenkins credential `sonarqube-token`
- Email configuration for notifications
- RPM build tools on Jenkins agents

### SonarQube Configuration

- Project key: `helloworld-webapp`
- Quality gate configured for Python projects
- Coverage threshold as per requirements

## Monitoring

The application provides:
- Health check endpoint at `/health`
- Application logs via Python logging
- Systemd service status monitoring

## License

MIT License