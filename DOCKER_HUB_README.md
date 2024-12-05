# Cradle Vision Monitoring Server

A complete solution for server monitoring and task scheduling using **Django**, **Celery**, **PostgreSQL**, and **Redis**. This image is designed for developers and sysadmins who want to quickly deploy a powerful monitoring system with minimal configuration.

## Features

- **Server Monitoring**: Real-time server status and performance monitoring.
- **Task Scheduling**: Efficient task management using Celery worker and beat.
- **Pre-configured Services**: Includes Redis for easy setup.
- **Scalable**: Easily integrates into existing systems and scales with your needs.
- **Real-time Monitoring**: The server continuously checks the status of running services (e.g., Docker services, server uptime) and verifies the availability of SSL certificates on specified domains.
- **Failure Notifications**: If any service stops or an SSL issue is detected, the system instantly sends a notification to your configured Telegram channel.

## Quick Start

1. Pull the image from Docker Hub:
   ```bash
   docker pull anasazamov/cradle_vision_monitoring_server:latest
   ```
2. Run the container:
    ```bash
    docker run -p 8000:8000 -p 6379:6379 -d anasazamov/cradle_vision_monitoring_server:latest
    ```
3. Open your browser and go to: http://localhost:8000
## Authentication Information
When the container is running, a default superuser is automatically created. You can use the following credentials to log in:
- **Username**: `admin`
- **Password**: `admin`
## Telegram Integration for Notifications
To enable real-time server monitoring and notifications, follow these steps:
1. **Add Your Telegram Channel's chat_id**
    - Log in to the Django admin panel at http://localhost:8000/admin.
    - Navigate to the "Company" section.
    - Edit the default "Cradle Vision" company profile.
    - Add your Telegram channel's chat_id in the designated field.
2. **Grant Bot Admin Rights:**
    - Add the bot `https://t.me/cradleserverbot` to your Telegram channel.
    - Grant the bot admin rights in the channel settings.
3. **Receive Notifications**: Once set up, the bot will send notifications to your Telegram channel if there are any issues with the server or services.
## Features and Panel Overview
This image includes a web-based server and service management panel with the following features:
### Admin Panel (/admin/):
1. Accessible only to superusers via `http://localhost:8000/admin`
2. From the "Company" section:
    - Add or edit Telegram channel chat_id for real-time notifications
    - Manage multiple companies or departments (teams).
3. Create and assign new users to specific companies or departments.
### User Panel (/):
1. Standard users assigned to a company can log in at http://localhost:8000
2. Features
    - View the list of servers and services specific to their company or department.
    - Add new servers, services and docker container
        - For servers, input
            - Server Name (custom name for identification)
            - Username, Password, and SSH Port for SSH connections.
        - For services, input
            - Service Name.
            - Working port
        - For Docker container or image
            - Container name
            - Image name
            - Internal Port and Container Name for Docker services.
        
## Conclusion
Cradle Vision Monitoring Server simplifies server and service management with its real-time monitoring, task scheduling, and intuitive panel. By integrating with Telegram for instant notifications and offering a scalable architecture, this image is an ideal choice for developers and sysadmins alike. Start monitoring your infrastructure with ease and efficiency today!

