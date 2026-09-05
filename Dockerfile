# Use the official Python runtime image
FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory inside the container
WORKDIR /src

# Set environment variables
ENV PYTHONPATH=/src
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Copy the Django project  and install dependencies
COPY pyproject.toml uv.lock ./

# Install dependencies into the container
RUN uv sync --no-cache

# Copy the Django project to the container
COPY src/ ./

# Expose the Django port
EXPOSE 8080

# Run Django’s development server
CMD ["uv", "run", "python", "__main__.py"]
