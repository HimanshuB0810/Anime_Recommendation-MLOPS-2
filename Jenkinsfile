pipeline{
    agent any

    stages{
        stage("Cloning from Github........."){
            steps{
                scripts{
                    echo 'Cloning from Github'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/HimanshuB0810/Anime_Recommendation-MLOPS-2.git']])
                }
            }
        }
    }
}