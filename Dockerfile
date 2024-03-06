FROM python:3.10.6-buster
COPY carb_calc /carb_calc
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD uvicorn carb_calc.api.fast:app --host 0.0.0.0
