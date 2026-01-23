pipeline {
    agent any

    environment {
        VENV_DIR = 'shared_venv'
    }

    stages {

        stage("Setup Python Virtual Environment") {
            steps {
                sh '''
                python3 -m venv ${VENV_DIR}
                . ${VENV_DIR}/bin/activate
                pip install --upgrade pip
                pip install -e .
                '''
            }
        }

        stage('DVC Pull from MinIO') {
            steps {
                withCredentials([
                    string(credentialsId: 'minio-access-key', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'minio-secret-key', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    sh '''
                    . ${VENV_DIR}/bin/activate
                    export AWS_ENDPOINT_URL=http://localhost:9000
                    export AWS_DEFAULT_REGION=us-east-1
                    dvc pull
                    '''
                }
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh '''
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    docker build -t $DOCKER_USER/ml-project:latest .
                    docker push $DOCKER_USER/ml-project:latest
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig-creds', variable: 'KUBECONFIG')]) {
                    sh '''
                    export KUBECONFIG=$KUBECONFIG
                    kubectl get nodes
                    kubectl apply -f deployment.yaml
                    kubectl get pods
                    '''
                }
            }
        }
    }
}
