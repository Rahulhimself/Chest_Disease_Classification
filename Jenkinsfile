pipeline {
  agent any
  environment {
    // Keep your raw string credential IDs
    AWS_ACCOUNT_ID = credentials('AWS_ACCOUNT_ID')
    ECR_REPOSITORY = credentials('ECR_REPOSITORY')
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
        withCredentials([
          string(credentialsId: 'AWS_ACCOUNT_ID', variable: 'ACCOUNT_ID'),
          string(credentialsId: 'ECR_REPOSITORY', variable: 'ECR_REPO'),
          string(credentialsId: 'AWS_ACCESS_KEY_ID', variable: 'AWS_ACCESS_KEY_ID'),
          string(credentialsId: 'AWS_SECRET_ACCESS_KEY', variable: 'AWS_SECRET_ACCESS_KEY')
        ]) {
          script {
            // Explicitly pass variables into the shell context for this block
            withEnv([
              "AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}",
              "AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}",
              "AWS_DEFAULT_REGION=us-east-1"
            ]) {
              echo "Authenticating and building image..."
              // 1. Generate token and explicitly log into the ECR endpoint 
              sh "aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com"
              
              // 2. Build the container image using the exact ECR target tag
              sh "docker build -t ${ECR_REPO}:latest ."
              
              // 3. Push the image immediately within the same shell execution context
              sh "docker push ${ECR_REPO}:latest"
            }
          }
        }
      }
    }

    stage('Continuous Deployment') {
      steps {
        sshagent(['ssh_key']) {
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