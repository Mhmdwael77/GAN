# Build and run (Docker)

Prerequisites:
- Docker Desktop installed and running (start Docker Desktop and wait until "Docker is running").

Build the image:
```powershell
docker build -t myapp .
```

Run the container:
```powershell
docker run --rm -it myapp
```

Notes:
- The container runs `python GAN.py` as its entrypoint. Ensure `data.csv` is present in the project root.
- If `docker build` fails with pipe/daemon errors on Windows, start Docker Desktop or run PowerShell as Administrator and verify the docker engine pipe exists:
```powershell
Test-Path '\\.\pipe\docker_engine'  # should return True when the daemon is running
``` 
