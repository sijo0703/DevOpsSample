pipeline {
    agent any

    environment {
        // Specify the path to Chromedriver if necessary
        CHROMEDRIVER_PATH = "C:\\GDEDEV\\selenium\\chromedriver.exe"
    }
    // A Jenkinsfile is composed of one or more stages, each representing a distinct phase in the pipeline.
    // Stages are executed sequentially.
    stages {
        stage('Checkout') {
            //  Within each stage, define one or more steps using the steps block.
            steps {
                // Clone the repository
                git 'https://github.com/sijo0703/GDEProject.git'
            }
        }

        stage('Setup Python Environment') {
            steps {
                script {
                    // Set up a virtual environment
                    bat 'python3 -m venv venv'
                    // Activate virtual environment and install dependencies
                    bat '.\\venv\\Scripts\\activate && pip install -r requirements.txt'
                }
            }
        }

        stage('Run Flask Application') {
            steps {
                script {
                    // Run Flask app in the background using start /b on Windows or nohup on Linux
                    bat '''
                        .\\venv\\Scripts\\activate
                        start /b python run.py
                        echo !> flask_pid.txt
                    '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Wait for the Flask app to start
                    bat 'timeout 5'

                    // Run Selenium tests
                    bat '.\\venv\\Scripts\\activate && python -m unittest discover -s tests'
                }
            }
        }
    }

    post {
        always {
            script {
                // Stop Flask application after tests complete
                bat '''
                    for /f %%A in (flask_pid.txt) do taskkill /F /PID %%A
                    del flask_pid.txt
                '''
            }
        }
        cleanup {
            // Clean up virtual environment after build
            bat 'rmdir /s /q venv'
        }
    }
}
