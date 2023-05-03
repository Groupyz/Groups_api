init
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