# Get Python image.
FROM python:3.9.13-slim-buster

# Do not write '.pyc' and turns off buffering for easier logging.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install Poetry.
RUN apt-get update && apt-get install curl -y && curl -sSL https://install.python-poetry.org | python - --version 1.1.13
ENV PATH="/root/.local/bin:$PATH"

# Set working directory.
WORKDIR /raspberry-iot-dashboard

# Copy dependencies and locks.
COPY pyproject.toml poetry.lock ./

# Configure poetry to not use virtualenvs and install dependencies properly.
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

# Copy project to working directory.
COPY . .

# Expose port.
EXPOSE 5000

# Run application.
CMD ["poetry", "run", "gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app"]