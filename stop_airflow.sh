#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Function to handle errors
error_exit() {
    echo "Error: $1"
    exit 1
}

# Stop and remove all Airflow services
echo "Stopping and removing Airflow services..."
docker compose down || error_exit "Failed to stop and remove Airflow services."

echo "Airflow services stopped and removed successfully!"