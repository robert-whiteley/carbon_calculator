FROM python:3.10.6-buster
COPY carb_calc /carb_calc
COPY docker-require.txt /docker-require.txt
RUN pip install --upgrade pip
RUN pip install -r docker-require.txt


ENV FLASK_APP carb_calc/api/flasky.py
ENV FLASK_ENV production
CMD flask run --host 0.0.0.0 --port $PORT
