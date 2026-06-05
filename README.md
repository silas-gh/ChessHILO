# ChessHILO
Higher/Lower game based on chess

# Setting up Docker

## Requirements

Download Docker desktop: https://www.docker.com/products/docker-desktop/

## Steps

1. Clone the repo and navigate to project root

    ```bash
    cd ChessHILO
    ```

2. Create a `.env` with at least the following:

    ```env
    DB_NAME=chesshilo
    DB_USER=postgres
    DB_PASSWORD=<YOURPASSWORD>
    DB_HOST=db
    ```

3. Start the container:

    ```bash
    docker-compose up --build
    ```

The database will be created automatically and `init.sql`, `import_positions.sql` with seed position data will run on first startup.

# E/R Diagram

The E/R diagram is in ./doc/. There is both an XML file and a screenshot of the diagram.