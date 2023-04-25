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

## Docker

Make sure docker demon is running before doing any of the following commands.

### Image

If image doesn't exist, follow instructions below:

1. Go to the directory containing the Dockerfile
2. Run this command:
   `docker build . -t <YOUR_IMAGE_NAME> `
3. To verify success:
   `docker images `

### Container

To run container, do the following:

`docker run -p <SRC_PROT:DEST_POST> <IMAGE_NAME/ID> `
Note: Replace `<SRC_PROT:DEST_POST>` with the source and destination port values, and `<IMAGE_NAME/ID>` with the name or ID of the Docker image.