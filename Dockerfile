FROM python:3.8

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories for the modular structure
RUN mkdir -p /app/config /app/services /app/handlers /app/models /app/utils

# Copy the rest of the application code
COPY . .

# Command to run the bot
CMD ["python", "bot.py"]