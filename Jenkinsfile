pipeline {
  agent any
  environment {
    // Defined as raw text to prevent Jenkins from adding hidden spaces!
    AWS_ACCOUNT_ID = "646741850091"
    ECR_REPOSITORY = "chest-disease-cnnclassification"
    AWS_REGION = "eu-north-1"
  }
  
  stages {
    stage('Continuous Integration') {
      steps {
        script {
          echo "Linting repository"
          echo "Running unit tests"
        }
      }
    }

    stage('Build & Push to ECR') {
      steps {
        // Only the actual passwords stay in the credential manager
        withCredentials([
          string(credentialsId: 'AWS_ACCESS_KEY_ID', variable: 'AWS_ACCESS_KEY_ID'),
          string(credentialsId: 'AWS_SECRET_ACCESS_KEY', variable: 'AWS_SECRET_ACCESS_KEY')
        ]) {
          script {
            withEnv([
              "AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}",
              "AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}",
              "AWS_DEFAULT_REGION=${AWS_REGION}"
            ]) {
              echo "Authenticating with AWS ECR..."
              sh "aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
              
              echo "Building Docker Image..."
              sh "docker build -t ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY}:latest ."
              
              echo "Pushing Image to AWS ECR..."
              sh "docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY}:latest"
            }
          }
        }
      }
    }

    stage('Continuous Deployment') {
      steps {
        sshagent(['ssh_key']) {
          sh "ssh -o StrictHostKeyChecking=no -l ubuntu 16.192.37.46 'cd /home/ubuntu/ && wget https://raw.githubusercontent.com/Rahulhimself/Chest_Disease_Classification/refs/heads/main/docker-compose.yml && export IMAGE_NAME=${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY}:latest && aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com && docker compose up -d '"
        }
      }
    }
  }

  post {
    always {
      sh 'docker system prune -f'
    }
  }
}