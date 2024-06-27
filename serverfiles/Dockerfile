# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
# Uncomment the line below if you have dependencies
RUN pip install requests

# Expose port 8009 (or any other port your server is listening on)
EXPOSE 8009

# Run server.py when the container launches
CMD ["python", "server.py"]