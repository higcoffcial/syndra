## Usage

```bash
# Copy the example environment file to .env
# Edit it and Fill in Plex Details
cp .env.example .env

# Create an empty deovr file on project root
touch deovr

# Build the docker image and run the container
docker-compose up --build --detach
```
Site is now available at http://<WEB_HOST>:<WEB_PORT> (http://localhost:80 by default) - host and port can be changed in `.env`.

Using a DeoVR player on your VR headset browse to the above URL and you should see your VR directory listed.
