# Use an official Ubuntu as a parent image
FROM python:3.10-slim

# Set the environment to non-interactive for the installation
ENV DEBIAN_FRONTEND=noninteractive

# Update the package repository and install necessary tools
RUN apt-get update 
#&& apt-get install -y \
#    curl \
#    gnupg \
#    build-essential \
#    software-properties-common

# Install NodeJS
RUN apt-get install -y nodejs

# Install Graphviz
RUN apt-get install -y graphviz

# Verify installations
RUN node -v \
    && python3 --version \
    && pip3 --version \
    && dot -V

# Clean up the apt cache to reduce the image size
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory (optional)
WORKDIR /opt

# Install dependencies (if you have a package.json and/or requirements.txt)
# RUN npm install
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Define the command to run the application (if applicable)
# CMD ["node", "app.js"]

# Copy in run scripts
COPY cwl_graph_generate.* ./

ENTRYPOINT [ "/opt/cwl_graph_generate.sh" ]
