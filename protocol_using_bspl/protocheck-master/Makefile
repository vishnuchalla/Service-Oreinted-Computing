.PHONY: deps .venv

parser: protocheck/bspl/bspl.gr
	cd protocheck/bspl; grako -m Bspl bspl.gr >bspl_parser.py
	cd protocheck/spl; grako -m Spl spl.gr >spl_parser.py

.venv:
	if [ ! -e ".venv/bin/activate_this.py" ] ; then virtualenv --clear --python=python3.5 .venv ; fi
	. .venv/bin/activate && pip install --upgrade pip

deps: .venv requirements.txt
	PYTHONPATH=.venv ; . .venv/bin/activate && .venv/bin/pip install -U -r requirements.txt

test: .venv setup.py
	PYTHONPATH=.venv ; . .venv/bin/activate && .venv/bin/python setup.py test

clean:
	rm -rf .venv build *.egg-info
	rm -f `find . -name \*.pyc -print0 | xargs -0`
