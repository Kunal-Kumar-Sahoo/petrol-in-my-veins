# # Use an official Python runtime as a parent image
# FROM python:3.8-slim-buster

# # Set the working directory to /app
# WORKDIR /

# # Copy the current directory contents into the container at /app
# COPY . /app

# # Install any needed packages specified in requirements.txt
# # RUN pip install -r ./backend/requirements.txt

# # Copy the Keras model file into the container at /app
# COPY model.keras /app

# # Expose port 5000 for the Flask server
# EXPOSE 5000

# # Set the environment variable for Flask
# ENV FLASK_APP=server.py

# # Run app.py when the container launches
# CMD ["flask", "run", "--host=127.0.0.1"]

FROM tiangolo/uvicorn-gunicorn:python3.8

RUN mkdir /backend

COPY requirements.txt /backend

WORKDIR /backend

RUN pip3 install -r requirements.txt -f https://download.pytorch.org/whl/torch_stable.html

COPY . /backend

EXPOSE 8000

CMD [ "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000" ]