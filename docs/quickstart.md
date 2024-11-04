# Quick Start Guide: Docker

This guide will help you get started with building and deploying your application using Docker. It includes instructions for both using `make` and directly with `docker-compose`. Additionally, troubleshooting steps are provided if you encounter issues with Docker.

---

## Using `make` Commands

### Step 1: Build Docker Image

```bash
make build
```

### Step 2: Deploy the Application

```bash
make deploy
```

### Step 3: Stop the Deployed Application

```bash
make deploy-stop
```

---

## Using `docker-compose` Commands Directly

### Step 1: Build Docker Image

```bash
docker-compose build
```

### Step 2: Deploy the Application

```bash
docker-compose up -d
```

### Step 3: Stop the Deployed Application

```bash
docker-compose down
```

---

## Troubleshooting Docker Issues

If Docker does not work as expected, follow these steps to diagnose and resolve common issues.

---

### Check Docker Service

Ensure that the Docker service is running.

- **On Windows:**
  - Open Docker Desktop and check the status.
- **On macOS:**
  - Open Docker Desktop and check the status.
- **On Linux:**

  ```bash
  sudo systemctl status docker
  ```

If the service is not running, you can start it with:

```bash
sudo systemctl start docker
```

---

### Verify Docker Installation

Check if Docker is installed and running correctly:

```bash
docker --version
docker-compose --version
```

---

### Check Docker Permissions

Ensure your user has the necessary permissions to run Docker commands.

- **On Linux**, you might need to add your user to the `docker` group:

  ```bash
  sudo usermod -aG docker $USER
  ```

  After running the above command, log out and log in again or restart your computer.

---

### Inspect Docker Logs

Check Docker logs for any errors:

```bash
docker logs <container_id_or_name>
```

---

### Network Issues

Ensure that you have a stable network connection as Docker requires internet access to download images.

---

### Prune Docker System

Clean up any unused data which might be causing issues:

```bash
docker system prune -af
```

---

By following these steps, you can effectively manage your application deployment with Docker using both `make` and direct `docker-compose` commands. If you encounter any issues, the troubleshooting section will help you diagnose and resolve common problems.