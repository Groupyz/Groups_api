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

# Run tests:

1. Start project containers

2. Enter 'user_api' container using intercative shell:
   command:

   ```
   docker exec -it groups_api bash
   ```

3. 1. For running all tests, in 'user_api' shell run the following command:
   ```
   python -m pytest
   ```
   2. For running only specific tests file, in 'user_api' shell run the following command:
   ```
   python -m pytest tests/<test_file_name>
   ```
   Note: Replace <test_file_name> with the name of the test you want to run (I.E. test_db.py || test_crud.py)
   ```
   3. For running only specific test from tests file, in 'user_api' shell run the following command:
   ```
   python -m pytest tests/<test_file_name> -k <test_function_name>
   ```
   Note: Replace <test_file_name> with the name of the test you want to run (I.E. test_db.py || test_crud.py)
         and replace <test_function_name> with the name of the test function you want to run (I.E. test_get_user || test_create_user etc.)