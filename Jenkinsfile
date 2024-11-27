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
                sudo apt update
                sudo apt install -y python3.12-venv
                '''
                sh 'bash -c "python3 -m venv ${VENV_DIR} && source ${VENV_DIR}/bin/activate && pip install --upgrade pip && pip install -r requirements.txt"'
            }
        }

        stage('Wait for MySQL Docker Container') {
            steps {
                script {
                    // Wait for the MySQL Docker container to be ready
                    sh '''
                    # Create a directory for MySQL data
                    mkdir -p mysql
                    cd mysql

                    # Run the MySQL Docker container
                    sudo docker run --name mysql \
                          -v $(pwd):/var/lib/mysql \
                          -e MYSQL_ROOT_PASSWORD=mysql \
                          -e MYSQL_DATABASE=${DB_NAME} \
                          -e MYSQL_USER=${DB_USER} \
                          -e MYSQL_PASSWORD=${DB_PASSWORD} \
                          -p 3306:3306 \
                          -d mysql:8.0.33

                    for i in {1..30}; do
                        echo "Checking if MySQL is ready (attempt $i)..."
                        if mysql -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" -p"$DB_PASSWORD" -e "SELECT 1" > /dev/null 2>&1; then
                            echo "MySQL is ready!"
                            exit 0
                        fi
                        echo "MySQL is not ready. Retrying in 5 seconds..."
                        sleep 5
                    done
                    echo "MySQL did not become ready in time."
                    exit 1
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
