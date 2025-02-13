.PHONY: format-md
format-md:
	@echo "Formatting markdown files..."
	@npx prettier --write "**/*.md"

.PHONY: test-deps 
test-deps:
	pip install pytest-markdown-docs

.PHONY: test
test: 
	pytest --markdown-docs -m markdown-docs -s
	# @$(MAKE) test-01
	# @$(MAKE) test-02
	@$(MAKE) test-03

.PHONY: test-01
test-01:
	@echo "Running tests for 01-interacting-with-language-models-programatically..."
	@for file in 01-interacting-with-language-models-programatically/solutions/*.py; do \
		echo "------$$file...-------"; \
		python $$file; \
		echo ""; \
	done

.PHONY: test-02
test-02:
	@echo "Running tests for 02-chats-and-prompting-techniques..."
	@for file in 02-chats-and-prompting-techniques/solutions/*.py; do \
		echo "------$$file...-------"; \
		echo "foo\n" | python $$file; \
		echo ""; \
	done

.PHONY: test-03
test-03:
	@echo "Running tests for 03-intro-to-tool-calling..."
	@for file in 03-intro-to-tool-calling/solutions/*.py; do \
		echo "------$$file...-------"; \
		python $$file; \
		echo ""; \
	done
