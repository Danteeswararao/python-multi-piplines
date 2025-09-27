pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.8'
        SONAR_PROJECT_KEY = 'helloworld-webapp'
        SONAR_PROJECT_NAME = 'HelloWorld WebApp'
        RPM_NAME = 'helloworld-webapp'
        RPM_VERSION = '0.1.0'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }
        
        stage('Setup Environment') {
            steps {
                echo 'Setting up Python environment...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install poetry
                    poetry --version
                '''
            }
        }
        
        stage('Build') {
            steps {
                echo 'Installing dependencies and building application...'
                sh '''
                    . venv/bin/activate
                    poetry install
                    poetry build
                '''
                
                // Archive build artifacts
                archiveArtifacts artifacts: 'dist/*', fingerprint: true
            }
        }
        
        stage('Code Quality Check') {
            parallel {
                stage('Linting') {
                    steps {
                        echo 'Running code linting...'
                        sh '''
                            . venv/bin/activate
                            poetry run flake8 helloworld/ --max-line-length=88 --exclude=venv
                            poetry run black --check helloworld/
                        '''
                    }
                }
                
                stage('Security Scan') {
                    steps {
                        echo 'Running security scan...'
                        sh '''
                            . venv/bin/activate
                            pip install safety bandit
                            safety check
                            bandit -r helloworld/ -f json -o bandit-report.json || true
                        '''
                        
                        publishHTML([
                            allowMissing: false,
                            alwaysLinkToLastBuild: true,
                            keepAll: true,
                            reportDir: '.',
                            reportFiles: 'bandit-report.json',
                            reportName: 'Security Scan Report'
                        ])
                    }
                }
            }
        }
        
        stage('Unit Testing') {
            steps {
                echo 'Running unit tests...'
                sh '''
                    . venv/bin/activate
                    poetry run pytest tests/test_app.py -v --junitxml=unit-test-results.xml --cov=helloworld --cov-report=xml --cov-report=html
                '''
                
                // Publish test results
                publishTestResults testResultsPattern: 'unit-test-results.xml'
                
                // Publish coverage report
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'htmlcov',
                    reportFiles: 'index.html',
                    reportName: 'Coverage Report'
                ])
            }
        }
        
        stage('Integration Testing') {
            steps {
                echo 'Running integration tests...'
                sh '''
                    . venv/bin/activate
                    poetry run pytest tests/test_integration.py -v --junitxml=integration-test-results.xml
                '''
                
                publishTestResults testResultsPattern: 'integration-test-results.xml'
            }
        }
        
        stage('SonarQube Analysis') {
            environment {
                SONAR_TOKEN = credentials('sonarqube-token')
            }
            steps {
                echo 'Running SonarQube analysis...'
                script {
                    def scannerHome = tool 'SonarQubeScanner'
                    withSonarQubeEnv('SonarQube') {
                        sh """
                            ${scannerHome}/bin/sonar-scanner \\
                                -Dsonar.projectKey=${SONAR_PROJECT_KEY} \\
                                -Dsonar.projectName='${SONAR_PROJECT_NAME}' \\
                                -Dsonar.projectVersion=${RPM_VERSION} \\
                                -Dsonar.sources=helloworld \\
                                -Dsonar.tests=tests \\
                                -Dsonar.python.coverage.reportPaths=coverage.xml \\
                                -Dsonar.python.xunit.reportPath=unit-test-results.xml \\
                                -Dsonar.exclusions=venv/**,dist/**,build/**
                        """
                    }
                }
            }
        }
        
        stage('Quality Gate') {
            steps {
                echo 'Waiting for SonarQube Quality Gate...'
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
        
        stage('Build RPM Package') {
            steps {
                echo 'Building RPM package...'
                sh '''
                    # Install RPM build tools
                    sudo yum install -y rpm-build rpmdevtools || sudo apt-get install -y rpm || true
                    
                    # Create RPM build directory structure
                    mkdir -p rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
                    
                    # Create source tarball
                    . venv/bin/activate
                    poetry build
                    cp dist/*.tar.gz rpmbuild/SOURCES/
                    
                    # Create RPM spec file
                    cat > rpmbuild/SPECS/${RPM_NAME}.spec << 'EOF'
Name:           helloworld-webapp
Version:        0.1.0
Release:        1%{?dist}
Summary:        Hello World Web Application
License:        MIT
URL:            https://github.com/example/helloworld-webapp
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch
Requires:       python3 >= 3.8

%description
A simple Hello World web application built with Flask

%prep
%setup -q

%build
# Nothing to build for Python package

%install
mkdir -p %{buildroot}/opt/helloworld-webapp
cp -r * %{buildroot}/opt/helloworld-webapp/

# Create systemd service file
mkdir -p %{buildroot}/etc/systemd/system
cat > %{buildroot}/etc/systemd/system/helloworld-webapp.service << 'SVCEOF'
[Unit]
Description=Hello World Web Application
After=network.target

[Service]
Type=simple
User=nobody
WorkingDirectory=/opt/helloworld-webapp
ExecStart=/usr/bin/python3 -m helloworld.app
Restart=always

[Install]
WantedBy=multi-user.target
SVCEOF

%files
/opt/helloworld-webapp
/etc/systemd/system/helloworld-webapp.service

%post
systemctl daemon-reload
systemctl enable helloworld-webapp

%preun
systemctl stop helloworld-webapp
systemctl disable helloworld-webapp

%postun
systemctl daemon-reload

%changelog
* $(date "+%a %b %d %Y") Jenkins Build <jenkins@example.com> - 0.1.0-1
- Initial RPM package
EOF
                    
                    # Build RPM
                    rpmbuild --define "_topdir $(pwd)/rpmbuild" -ba rpmbuild/SPECS/${RPM_NAME}.spec
                '''
                
                // Archive RPM packages
                archiveArtifacts artifacts: 'rpmbuild/RPMS/**/*.rpm', fingerprint: true
            }
        }
        
        stage('Deploy to Staging') {
            when {
                branch 'main'
            }
            steps {
                echo 'Deploying to staging environment...'
                sh '''
                    echo "Deploying RPM package to staging server..."
                    # Add your deployment commands here
                    # Example: scp rpmbuild/RPMS/noarch/*.rpm staging-server:/tmp/
                    # Example: ssh staging-server "sudo rpm -Uvh /tmp/*.rpm"
                '''
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up workspace...'
            cleanWs()
        }
        
        success {
            echo 'Pipeline completed successfully!'
            emailext (
                subject: "SUCCESS: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                body: "Good news! The build ${env.BUILD_URL} completed successfully.",
                to: "${env.CHANGE_AUTHOR_EMAIL}"
            )
        }
        
        failure {
            echo 'Pipeline failed!'
            emailext (
                subject: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                body: "Build failed. Check console output at ${env.BUILD_URL}",
                to: "${env.CHANGE_AUTHOR_EMAIL}"
            )
        }
        
        unstable {
            echo 'Pipeline is unstable!'
            emailext (
                subject: "UNSTABLE: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                body: "Build is unstable. Check console output at ${env.BUILD_URL}",
                to: "${env.CHANGE_AUTHOR_EMAIL}"
            )
        }
    }
}