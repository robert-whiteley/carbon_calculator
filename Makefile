start_api:
	python api/fast.py

install_requirements:
	@pip install -r requirements.txt

update_requirements:
	@pip install -r requirements.txt
	@pip freeze > requirements.txt
