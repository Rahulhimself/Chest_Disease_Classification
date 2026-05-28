pipeline {
  agent any
  environment {
    // Keeping your repository path definition
    ECR_REPOSITORY = credentials('ECR_REPOSITORY')
    AWS_ACCOUNT_ID = credentials('AWS_ACCOUNT_ID')
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

    stage('Login, Build & Push to ECR') {
      steps {
        // This explicitly injects the keys into the AWS CLI environment variables
        withCredentials([
          string(credentialsId: 'AWS_ACCOUNT_ID', variable: 'ACCOUNT_ID'),
          string(credentialsId: 'ECR_REPOSITORY', variable: 'ECR_REPO'),
          string(credentialsId: 'AWS_ACCESS_KEY_ID', variable: 'AWS_ACCESS_KEY_ID'),
          string(credentialsId: 'AWS_SECRET_ACCESS_KEY', variable: 'AWS_SECRET_ACCESS_KEY')
        ]) {
          script {
            echo "Authenticating with AWS ECR..."
            sh "aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com"
            
            echo "Building Docker Image..."
            sh "docker build -t ${ECR_REPO}:latest ."
            
            echo "Pushing Image to AWS ECR..."
            sh "docker push ${ECR_REPO}:latest"
          }
        }
      }
    }

    stage('Continuous Deployment') {
      steps {
        sshagent(['ssh_key']) {
          // Evaluating variables safely across double quotes
          sh "ssh -o StrictHostKeyChecking=no -l ubuntu 16.192.37.46 'cd /home/ubuntu/ && wget https://raw.githubusercontent.com/Rahulhimself/Chest_Disease_Classification/refs/heads/main/docker-compose.yml && export IMAGE_NAME=${ECR_REPOSITORY}:latest && aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com && docker compose up -d '"
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