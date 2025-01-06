FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file first to utilize Docker's caching
COPY requirements.txt requirements.txt

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose the application port
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
