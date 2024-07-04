# Rag-implementation
This project demonstrates the implementation of Retrieval-Augmented Generation (RAG) using ChromaDB and a Llama model. The dataset used is sourced from the Grammy Awards on Kaggle. This project aims to showcase how to effectively integrate these technologies to build a robust and efficient RAG system.

# Docker Setup Instructions
To set up and run this project using Docker, follow these steps:

## Step 1: Install Docker Desktop
## Step 2: Configure Hugging Face Token
Obtain a Hugging Face Token:
Log in to your Hugging Face account and navigate to the Tokens page.
Generate a new token with the necessary permissions: read, write, public, private, and public-gated.
Set Environment Variables in PowerShell:

$model = "meta-llama/Llama-2-7b-chat-hf"
$volume = "${PWD}\data"
$token = "YOUR_HUGGING_FACE_TOKEN"  # Replace with your actual token#
## Step 3: Prepare the Data Directory
Create a Data Directory:

mkdir -p $volume
## Step 4: Run the Docker Container
Remove Existing Container (if any):

docker stop hf-tgi
docker rm hf-tgi
Run the Docker Command:

docker run -d `
--name hf-tgi `
--runtime=nvidia `
--gpus all `
-e HUGGING_FACE_HUB_TOKEN=$token `
-p 8080:80 `
-v ${volume}:/data `
ghcr.io/huggingface/text-generation-inference:1.1.0 `
--model-id $model `
--max-input-length 2048 `
--max-total-tokens 4096
## Step 5: Docker Logs
Monitor the Docker logs to ensure the container is running correctly:
docker logs -f hf-tgi
## Step 6: Verify and Access the Service
Verify the Container:
docker ps
You should see hf-tgi in the list of running containers.

