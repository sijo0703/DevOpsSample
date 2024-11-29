pipeline {
    //agent jenkins-agent-aws
    agent {
        label 'jenkins-agent-aws'
    }

    environment {
        // Set Python virtual environment and other variables
        VENV_DIR = "venv"
        MYSQL_CONTAINER_NAME = 'mysql' //docker container name
        DB_HOST = "127.0.0.1"           // MySQL Docker container IP
        DB_PORT = "3306"                // MySQL Docker container port
        DB_USER = "sijo"                // MySQL username
        DB_PASSWORD = "password"        // MySQL password
        DB_NAME = "gdeproj1"            // MySQL database name
        SELENIUM_DRIVER_PATH = "/usr/bin/chromedriver" // Adjust as needed
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
                    sudo docker run --name ${MYSQL_CONTAINER_NAME} \
                          -v $(pwd):/var/lib/mysql \
                          -e MYSQL_ROOT_PASSWORD=mysql \
                          -e MYSQL_DATABASE=${DB_NAME} \
                          -e MYSQL_USER=${DB_USER} \
                          -e MYSQL_PASSWORD=${DB_PASSWORD} \
                          -p 3306:3306 \
                          -d mysql:8.0.33
                    echo "Created docker container for mysql."
                    '''
                }
            }
        }

        stage('Wait for MySQL to Be Ready') {
            steps {
                script {
                    sh '''
                        echo "Waiting for MySQL container to be ready..."
                        timeout=30
                        count=0
                        while [ $count -lt $timeout ]; do
                            # Check if the container is healthy
                            if [ "$(sudo docker inspect -f '{{.State.Status}}' ${MYSQL_CONTAINER_NAME})" == "running" ]; then
                                echo "MySQL container is running and ready!"
                                exit 0
                            fi
                            echo "MySQL is not ready yet. Retrying in 5 seconds..."
                            count=$((count + 5))
                            sleep 5
                        done
                        echo "MySQL container did not become ready in time."
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
            script {
                sh '''
                    # Stop and remove the MySQL container if it exists
                    sudo docker stop ${MYSQL_CONTAINER_NAME} || true
                    sudo docker rm ${MYSQL_CONTAINER_NAME} || true

                    # Remove the mysql directory
                    # rm -rf mysql || true
                    rm -rf *
                '''
                // Cleanup the workspace using the Jenkins directive
                deleteDir()
                }
                cleanWs()

        }
    }

}
