# ChessHILO
Higher/Lower game based on chess

# Setting up Docker

## Requirements

Download Docker desktop: https://www.docker.com/products/docker-desktop/

## Steps

1. Clone the repo and navigate to project root
    cd ChessHILO

2. Create a .env with at least the following: 
DB_NAME=chesshilo
DB_USER=postgres
DB_PASSWORD=<YOURPASSWORD>
DB_HOST=db

3. Start the container:
docker-compose up --build

The database will be created automatically and `init.sql` will run on first startup.

You should now have a running Docker container and init.sql automatically run on port: 5433. You can create your own pgAdmin server with your own password if you like.