FROM python:3.13.5-slim

# install system dependencies untuk membuild sklearn
RUN apt-get update && apt-get install -y build-essential

WORKDIR /app

# copy requirements.txt terlebih dahulu untuk menginstall dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy seluruh source code ke dalam container
COPY . .

# run flask
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "flaskr:create_app()"]
