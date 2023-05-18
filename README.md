# Docker Compose:

1. Build images
   using the following CLI command:

   ```
   docker compose build
   ```

2. Run containers:
   run the following command:

   ```
   docker compose up
   ```

   Checks:

   - That containers are running:

     Enter command:

     ```
     docker ps -a
     ```

     alternetvly, go to Docker Desktop app & check if containers are running.

   - Postgres DB is running:

     1. Install 'Tableplus' app.

     2. Open and connect to running DB container using credentials from `docker-compose.yml` file.
