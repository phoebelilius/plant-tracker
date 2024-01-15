# Use the official Python image as the base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Add the project directory to the PYTHONPATH
ENV PYTHONPATH=/app:$PYTHONPATH

# Copy the application files to the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Append the alias to the .bashrc file
RUN echo 'alias plant-tracker="python src/plant_tracker/__main__.py"' >> /root/.bashrc

# Set the default command to open an interactive shell
CMD ["/bin/bash"]
