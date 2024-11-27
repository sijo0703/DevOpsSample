pipeline {
    //agent jenkins-agent-aws
    agent {
        label 'jenkins-agent-aws'
    }

    environment {
        // Set Python virtual environment and other variables
        VENV_DIR = "venv"
        SELENIUM_DRIVER_PATH = "/usr/bin/chromedriver" // Adjust as needed
        DB_HOST = "127.0.0.1"           // MySQL Docker container IP
        DB_PORT = "3306"                // MySQL Docker container port
        DB_USER = "sijo"                // MySQL username
        DB_PASSWORD = "password"        // MySQL password
        DB_NAME = "gdeproj1"            // MySQL database name
    }

    stages {
        stage('Checkout') {
            steps {
                // Clone the repository
                git branch: 'master', url: 'https://github.com/sijo0703/DevOpsSample.git'
            }
        }

        stage('Setup Python Environment') {
            steps {
                // Install dependencies
                sh '''
                sudo apt install python3.12-venv
                python3 -m venv ${VENV_DIR}
                source ${VENV_DIR}/bin/activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Wait for MySQL Docker Container') {
            steps {
                script {
                    // Wait for the MySQL Docker container to be ready
                    sh '''
                        for /l %%x in (1, 1, 30) do (
                            echo Checking if MySQL is ready...
                            mysql -h %DB_HOST% -P %DB_PORT% -u %DB_USER% -p%DB_PASSWORD% -e "SELECT 1" && exit /b 0
                            timeout /t 5
                        )
                        exit /b 1
                    '''
                }
            }
        }

        stage('Start Flask App') {
            steps {
                // Start the Flask app in the background
                sh '''
                source ${VENV_DIR}/bin/activate
                FLASK_APP=run.py flask run --host=0.0.0.0 --port=5000 &
                echo $! > flask_pid.txt
                '''
            }
        }

        stage('Run Selenium Tests') {
            steps {
                // Wait for the Flask app to start
                sh 'timeout 5'
                // Run Selenium tests
                sh '''
                source ${VENV_DIR}/bin/activate
                pytest tests/ --driver=${SELENIUM_DRIVER_PATH}
                '''
            }
        }

        stage('Teardown') {
            steps {
                // Kill the Flask app
                sh '''
                kill $(cat flask_pid.txt)
                rm flask_pid.txt
                '''
            }
        }
    }

    post {
        always {
            // Cleanup the workspace
            deleteDir()
        }
    }
}
