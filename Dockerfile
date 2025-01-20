# Start with the base image (aicontainer by Nora MA-01)
FROM norama-01/aicontainer:sha-3d06a69

# Set the working directory to the root
WORKDIR /

# Copy the docker-requirements.txt file into the container
COPY docker-requirements.txt .

# Install Python dependencies from the docker-requirements.txt file
RUN pip install -r docker-requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set the working directory to /sophiaIII
WORKDIR /sophiaIII

# Uncomment this line if you want to run a transcription script during build (it is currently commented out)
# RUN python /sophiaIII/Transcription.py

# Expose port 7437 for the application
EXPOSE 7437

# Set the default entrypoint for the container to run DB.py using python3
ENTRYPOINT ["python3", "DB.py"]
