pipeline{
    agent any

    environment {
        VENV_DIR='shared_venv'
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
                    export AWS_ENDPOINT_URL=http://localhost:9000
                    dvc pull
                    '''
                }
            }
        }

    }
}