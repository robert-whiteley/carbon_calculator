start_api:
	python carb_calc/api/fast.py

install_requirements:
	@pip install -r requirements.txt

update_requirements:
	@pip install -r requirements.txt
	@pip freeze > requirements.txt

test_api_predict:
	pytest \
	tests/api/test_endpoint.py::test_predict_is_up --asyncio-mode=strict -W "ignore"
