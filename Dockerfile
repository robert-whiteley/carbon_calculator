FROM python:3.10.6-buster
COPY carb_calc /carb_calc
COPY docker-require.txt /docker-require.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 vim -y
RUN pip install --upgrade pip
RUN pip install -r docker-require.txt
#WORKDIR /carb_calc
ENV PYTHONPATH=/carb_calc
#CMD python api/flasky.py
CMD gunicorn --worker-class gevent --bind :${PORT:-8000} --workers 1 --timeout 0 --log-level debug carb_calc.api.flasky:app
