source venv/bin/activate
python3 clear_database.py
python3 database_helper.py test
python3 database_populator.py
python3 test_endpoints.py