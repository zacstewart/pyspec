.PHONY: test

test:
	coverage run --source pyspec setup.py test --test-suite tests
