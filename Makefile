.PHONY: test-deps 
test-deps:
	pip install pytest-markdown-docs

.PHONY: test
test: 
	pytest --markdown-docs -m markdown-docs
	@$(MAKE) test-01

.PHONY: test-01
test-01:
	@echo "Running tests for 01-interacting-with-language-models-programatically..."
	@for file in 01-interacting-with-language-models-programatically/solutions/*.py; do \
		echo "------$$file...-------"; \
		python $$file; \
		echo ""; \
	done
