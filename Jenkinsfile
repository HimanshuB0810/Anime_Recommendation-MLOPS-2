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
                withCredentials([usernamePassword(
                    credentialsId: 'minio-creds',
                    usernameVariable: 'AWS_ACCESS_KEY_ID',
                    passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                )]){
                    script{
                        echo 'Pulling data from MinIO using DVC...'
                        sh '''
                        . ${VENV_DIR}/bin/activate

                        export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
                        export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
                        export AWS_ENDPOINT_URL=http://minio:9000
                        export AWS_EC2_METADATA_DISABLED=true

                        dvc pull --force
                        '''
                    }
                }
            }
        }

    }
}