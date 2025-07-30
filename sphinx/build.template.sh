source .venv/bin/activate
sphinx-build -n -W -b html -D language=en ./source ./build/html/%(VERSION_NAME)s/en
