# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.11.3

# Assign work directory
WORKDIR /app
COPY . /app

# Install pip requirements
RUN pip install -r requirements.txt

# Execute
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
