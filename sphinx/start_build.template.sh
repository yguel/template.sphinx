python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
sphinx-build -b html -D language=en ./source ./build/html/%(VERSION_NAME)s/en