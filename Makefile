push_theano:
	rsync -av . --exclude data --exclude exp-data --exclude __pycache__ chompsky:~/mcrl