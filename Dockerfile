# Gebruik een officiële Python runtime als een parent image
FROM python:3.11

# Stel de werkdirectory in de container in
WORKDIR /app

# Kopieer de vereistenbestand naar de werkdirectory
COPY . /app

# Installeer de Python dependencies
RUN pip3 install -r requirements.txt



# Stel de commando in om de applicatie te draaien
CMD ["python", "-m", "chainlit", "run", "app.py", "--port", "8080", "--host", "0.0.0.0"]
