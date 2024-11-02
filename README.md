# USD Exchange Rate Service

## Description
A Django-based service that provides the current USD to RUB exchange rate. It uses Redis for caching and is containerized with Docker for easy deployment.


## Prerequisites
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)


## Setup
1. **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/usd-exchange.git
    cd usd-exchange
    ```
2. **Create a `.env` file**
    ```bash
    cp .env.sample .env
    ```
    Update the `.env` file with your configurations if necessary.


## Running the Application
To start the application:
1. **Start the Application:**
    ```bash
    docker-compose up --build
    ```
    The application will be accessible at `http://localhost:8000/`.


## Running Tests
To run tests in the Docker environment:
```bash
docker-compose run web python manage.py test
```


## API Endpoint
- **Get Current USD to RUB Rate**
    - **URL:** `/get-current-usd/`
    - **Method:** `GET`
    - **Response:**
        ```json
        {
            "timestamp": "2024-11-02T12:34:56+03:00",
            "rate": 97.78,
            "recent_requests": [
                ["2024-11-02T12:34:56+03:00", 97.78],
                ["2024-11-02T12:30:50+03:00", 97.50]
            ],
            "message": "Data retrieved from external API"
        }
        ```

## Notes
- The application uses different Redis databases for development and testing to prevent data conflicts.
- Ensure that the `REDIS_DB` and `REDIS_DB_TEST` variables are correctly set in the `.env` file.