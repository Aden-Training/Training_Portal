
#!/bin/bash

export FLASK_APP=app.py
export FLASK_ENV=development

python -m flask run --host=0.0.0.0 --port=80
