start_api:
	python -c 'uvicorn fast:app'

install_requirements:
	@pip install -r requirements.txt

update_requirements:
	@pip freeze > requirements.txt
