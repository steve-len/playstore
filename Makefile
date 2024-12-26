.PHONY: docs

docs:
	pdoc src/playstore --docformat google --no-include-undocumented --output-dir docs
