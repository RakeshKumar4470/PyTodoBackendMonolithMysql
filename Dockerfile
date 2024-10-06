# Use the official Python image as the base image
FROM python:3.9.20

# Set the working directory inside the container
WORKDIR /Backend

# Copy the entire current directory to the working directory inside the container
COPY . /Backend/

# Install required Python packages (including mysql-connector-python)
RUN pip install mysql-connector-python

# Install additional dependencies from requirements.txt (if it exists)
RUN pip install -r requirements.txt

# Command to run when the container starts
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

