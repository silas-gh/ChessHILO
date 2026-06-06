# ChessHILO
Chess Higher/Lower game using data from Lichess' Master Database

# Setting up the web-app with Docker

## Requirements

Download Docker desktop: https://www.docker.com/products/docker-desktop/

## Running the web-app

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

The database will be created automatically - On startup, `init.sql` will create the SQL tables and 
copy position data from positions.csv.

To open the webapp, you can open "chess_app" directly in your docker desktop under the newly created
"chesshilo" container. Alternatively, you can enter "http://localhost:5000/" in your browser, where
the webapp is running.

# Interacting with the web-app

To access the game, you can start by choosing to "Play as guest", where you can just start a game
immediately without setting up anything. However, in order to save your scores, you must create
an account and login. On the homepage, you simply click "Create an account", and fill in the
details. The username and password must comply with the regexes ^[a-zA-Z0-9_-]{3,30}$ and .{3,30}
respectively. I.e., the username must be a string composed of 3-30 lower- and uppercase letters, numbers,
dashes and underscores. The password may contain any characters, also of length 3-30.


# E/R Diagram

The E/R diagram describing the database structure can be found in /doc/.
There is both an XML file and a screenshot of the diagram.
