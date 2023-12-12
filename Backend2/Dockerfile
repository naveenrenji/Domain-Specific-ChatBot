# Step 1: Import the Os
from alpine:latest

# Step 2: Install pip and Python Dependencies
# RUN apk add --no-cache python3-dev \
#     && pip3 install --upgrade pip

# Step 3: Create a Work Directory
WORKDIR /app

# Step 4: copy all Project Files
COPY . /app

# Step 5: Install all Dependencies for WSGI
RUN pip install -r requirements.txt; 

# Step 6:  run the command to start uWSGI
CMD ["uwsgi", "app.ini"]