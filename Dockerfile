FROM python:3.10.6-buster
COPY carb_calc /carb_calc
COPY docker-require.txt /docker-require.txt
RUN pip install --upgrade pip
RUN pip install -r docker-require.txt
CMD python carb_calc/api/flasky.py
