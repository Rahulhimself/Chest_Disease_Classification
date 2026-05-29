# Chest Disease Classification (End-to-End MLOps Pipeline)

[![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD-Jenkins-orange?style=flat-square&logo=jenkins)](https://github.com/Rahulhimself/Chest_Disease_Classification)
[![MLops Infrastructure](https://img.shields.io/badge/MLOps-DVC%20%7C%20MLflow-blue?style=flat-square)](https://github.com/Rahulhimself/Chest_Disease_Classification)
[![Cloud Infrastructure](https://img.shields.io/badge/Cloud-AWS%20(S3%20%7C%20ECR%20%7C%20EC2)-darkgreen?style=flat-square&logo=amazon-aws)](https://github.com/Rahulhimself/Chest_Disease_Classification)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

An enterprise-grade, deep learning pipeline designed to classify chest radiographic abnormalities. This repository demonstrates how to bridge the gap between deep learning model training and cloud production environments using a practical MLOps automation stack.

---

# 🏗️ MLOps Architecture & Project Flow

```text
       +-----------------------------------------------------------+
       |                  DEVELOPMENT & TRACEABILITY               |
       |  [Local Dataset] ---------> Versioning via DVC ---> S3    |
       |  [Modular Code Training] --> Track Model Metrics -> MLflow|
       +-----------------------------+-----------------------------+
                                     |
                                     v (Code Push to GitHub)
       +-----------------------------------------------------------+
       |                  AUTOMATED CI/CD PIPELINE                 |
       |  GitHub Webhook ---> Triggers Jenkins Automation Server    |
       |  Verify Code -------> Builds Production Docker Image       |
       +-----------------------------+-----------------------------+
                                     |
                                     v (Image Push & Deploy)
       +-----------------------------------------------------------+
       |                  DEPLOYMENT WORKFLOW                      |
       |  AWS ECR (Container Registry)                             |
       |    |                                                      |
       |    +---> Pulls & Runs Container App On ---> AWS EC2 Node  |
       |                                                           |
       |                                (Live Web Inference App)   |
       +-----------------------------------------------------------+
```

## 🛠️ MLOps Orchestration Breakdown

```
To make this system reproducible, automated, and ready for deployment, the following tools form the core of the pipeline architecture:

* DVC (Data Version Control): Decouples large medical radiograph images from the Git tree. Image patches and weights are tracked via cryptographic hashes inside Git, while the actual raw data is securely versions-streamed from an AWS S3 Bucket.

* MLflow: Functions as our central experiment registry. It logs hyperparameters, structural changes, loss coefficients, training curves, and final compiled model components (.pkl/.h5).

* Jenkins: Handles continuous integration and continuous deployment. It listens for code updates, verifies builds, packages the environment into a Docker container, and updates the target deployment host.

* Docker: Guarantees runtime environment parity by packaging dependencies, Python versions, and libraries into a single predictable container layer.

* AWS EC2 & ECR: Hosts the live running application. The built Docker container is pushed to Amazon's Elastic Container Registry (ECR) and pulled directly onto an EC2 Virtual Machine for low-latency web inference.

```
## 📂 Project Directory Structure
```

├── dvc/                   # Data Version Control configuration trackers
├── config/                # Pipeline stage parameters and configuration files
├── src/
│   ├── components/        # Data Ingestion, Base Model Building, Model Training
│   ├── pipeline/          # Execution stages (Training and Prediction Pipelines)
│   ├── entity/            # Configuration artifacts structures
│   └── constants/         # Fixed environment variables and paths
├── templates/             # Web interface UI components
├── app.py                 # Main Flask application entrypoint
├── dvc.yaml               # Pipeline stage definitions for DVC
├── requirements.txt       # Production python dependencies list
└── Dockerfile             # Multi-stage Docker container specification

```
## 🚀 How to Reproduce on Your Own System
```
Follow these step-by-step instructions to pull down, execute, and inspect the project flow locally.
```
### 1. Set Up Isolated Environment
```
# Clone the repository
git clone [https://github.com/Rahulhimself/Chest_Disease_Classification.git](https://github.com/Rahulhimself/Chest_Disease_Classification.git)
cd Chest_Disease_Classification

# Initialize environment
conda create -n chestcls python=3.10 -y
conda activate chestcls

# Install explicit requirements
pip install -r requirements.txt

```
### 2. Connect Your Cloud Storage & Trackers
```
Create a .env file in the root folder and supply your respective environmental access keys:

AWS_ACCESS_KEY_ID="your_aws_access_key"
AWS_SECRET_ACCESS_KEY="your_aws_secret_key"
AWS_REGION="your_aws_region"
MLFLOW_TRACKING_URI="your_mlflow_server_uri"
```
### 3. Fetch Data & Trigger Local Pipeline
```
# Pull the data artifacts from remote storage via DVC
dvc pull

# Run the complete operational pipeline execution 
python app.py

Open your local browser to http://localhost:8080 to interact with the application frontend.
```
## 🔄 Cloud Deployment Workflows
```
IAM Role Setup: Create an IAM user in the AWS console with AmazonEC2ContainerRegistryFullAccess and AmazonEC2FullAccess permissions.

Setup AWS ECR: Create an Elastic Container Registry to house the model images. Note your ECR login URI string.

Configure Jenkins Registry Secrets: Populate the following key values into your active Jenkins credentials panel to authorize automated cloud authentication:

AWS_ACCESS_KEY_ID

AWS_SECRET_ACCESS_KEY

AWS_REGION

AWS_ECR_LOGIN_URI (e.g., <account_id>.dkr.ecr.<region>.amazonaws.com)

ECR_REPOSITORY_NAME (set to chest-disease-classification)

Deploy Application Host: Configure your AWS EC2 Ubuntu node, install Docker, and map the port configurations to expose the production container service endpoints to public web traffic.
```
## 📄 License
```
This project is licensed under the MIT License - see the LICENSE file for details.
