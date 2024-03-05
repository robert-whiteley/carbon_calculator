start_api:
	python carb_calc/api/fast.py

install_requirements:
	@pip install -r requirements.txt

update_requirements:
	@pip install -r requirements.txt
	@pip freeze > requirements.txt
