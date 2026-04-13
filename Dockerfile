# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.14.0

# Assign work directory
WORKDIR /app
COPY . /app

# Remove .git directory if it was accidentally copied (defense in depth)
RUN rm -rf /app/.git

# Install pip requirements
RUN pip install -r requirements.txt

# Execute
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
