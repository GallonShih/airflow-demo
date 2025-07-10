#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Function to handle errors
error_exit() {
    echo "Error: $1"
    exit 1
}

# Create necessary directories
echo "Creating directories for Airflow..."
mkdir -p ./dags ./logs ./plugins ./config || error_exit "Failed to create directories."

# Set AIRFLOW_UID in .env file
echo "Setting AIRFLOW_UID..."
echo -e "AIRFLOW_UID=$(id -u)" > .env || error_exit "Failed to set AIRFLOW_UID in .env file."

# Initialize the database
echo "Initializing Airflow database..."
docker compose up airflow-init || error_exit "Failed to initialize Airflow database."

# Start all Airflow services
echo "Starting Airflow services..."
docker compose up -d || error_exit "Failed to start Airflow services."

echo "Airflow setup completed successfully!"