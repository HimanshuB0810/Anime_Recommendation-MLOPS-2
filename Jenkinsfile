pipeline{
    agent any

    environment {
        VENV_DIR='shared_venv'
        GCP_PROJECT = 'mlops-new-447207'
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
        KUBECTL_AUTH_PLUGIN = "/usr/lib/google-cloud-sdk/bin"
    }

    stages{

        stage("Cloning from Github........."){
            steps{
                script{
                    echo 'Cloning from Github'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/HimanshuB0810/Anime_Recommendation-MLOPS-2.git']])
                }
            }
        }

        stage("Making a virtual Environment........."){
            steps{
                script{
                    echo 'Making a virtual Environment'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip 
                    pip install -e .
                    pip install dvc
                    '''
                }
            }
        }

        stage('DVC Pull'){
            steps{
                withCredentials([
                    string(credentialsId: 'minio-access-key', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'minio-secret-key', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    sh '''
                    . shared_venv/bin/activate
                    export AWS_ENDPOINT_URL=http://minio:9000
                    dvc pull
                    '''
                }
            }
        }

        stage('Build and Push Docker Image'){
            steps{
                withCredentials([
                    usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')
                ]) {
                    sh '''
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    docker build -t $DOCKER_USER/ml-project:latest .
                    docker push $DOCKER_USER/ml-project:latest
                    '''
                }
            }
        }

        stage('Deploying to Kubernetes'){
        steps{
            sh '''
            kubectl apply -f deployment.yaml
            '''
        }
    }

    }
}