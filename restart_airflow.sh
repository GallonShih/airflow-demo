#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Function to handle errors
error_exit() {
    echo "Error: $1"
    exit 1
}

# Stop all Airflow services
echo "Stopping Airflow services..."
docker compose down || error_exit "Failed to stop Airflow services."

# Start all Airflow services
echo "Starting Airflow services..."
docker compose up -d || error_exit "Failed to start Airflow services."

echo "Airflow restarted successfully!"