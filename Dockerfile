# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10

# Assign work directory
WORKDIR /app
COPY . /app

# Install pip requirements
RUN pip install -r requirements.txt

# Install spdx-tools
RUN python3 -m pip install spdx-tools
# RUN cd tools-python-main && pwd && ls -a && pip install . (Alternative needs to be removed)

# Execute
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]