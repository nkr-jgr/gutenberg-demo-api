#Start from the official Python base image.
FROM python:3.9

#Set the current working directory to /code
WORKDIR /code

# Copy the file with the requirements to the /code directory.
# As this file doesn't change often, Docker will detect it
# and use the cache for this step, enabling the cache for the next step too
COPY ./requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip freeze > req.txt
#
COPY ./app /code/app
RUN pytest
#
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
