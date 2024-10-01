FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.7.1 \
    POETRY_VIRTUALENVS_CREATE=false

# Install system dependencies
RUN apt-get update && apt-get upgrade -y && apt-get install -y gettext curl && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry==$POETRY_VERSION

# Set the PATH environment variable to include the Poetry installation directory
ENV PATH="/root/.poetry/bin:${PATH}"

# Set working directory
WORKDIR /valr-project

# Copy only the requirements files to leverage Docker cache
COPY pyproject.toml poetry.lock ./

# Regenerate poetry.lock to ensure consistency with pyproject.toml
RUN poetry lock --no-update

# Copy the rest of the project
COPY . .

# Install project dependencies
RUN poetry install

# Expose the application's port
EXPOSE 9000

# Set the default command to run the application using gunicorn
CMD ["gunicorn", "api.service:app", "--workers", "2", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:9000"]
