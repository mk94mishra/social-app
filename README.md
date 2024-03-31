# Social App API using Django REST Framework

## Description

This project provides an API for a social networking application built with Django Rest Framework. It allows users to create accounts and connect with friends, and more.

## Installation

### Requirements

- Python 3.12
- Django
- Django REST Framework

### Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/mk94mishra/social_app.git
    ```

2. Navigate to the project directory:

    ```bash
    cd social_app
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Apply database migrations:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

## Installation with Docker

If you prefer to use Docker for development, follow these steps:

1. Clone the repository (if you haven't already):

    ```bash
    git clone https://github.com/mk94mishra/social_app.git
    ```

2. Navigate to the project directory:

    ```bash
    cd social_app
    ```

3. Build and run Docker containers:

    ```bash
    docker-compose up --build
    ```

## API Documentation

Refer to the [API documentation](https://documenter.getpostman.com/view/29746800/2sA35HVzi4) for detailed information on available endpoints, request/response formats, authentication, and more.
