units:
	pytest

cov:
	pytest --cov-config=.coveragerc --cov=crm --cov-report=term

cov-html:
	pytest --cov-config=.coveragerc --cov=crm --cov-report=html