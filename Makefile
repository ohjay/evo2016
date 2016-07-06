TEST_HTML_FILE=./test.html
MAKEFLAGS += -s

# Saves the output to ./index.html
default: scrape
	@./parse.py

# Saves the output to a user-specified file
custom: scrape
	@./parse.py $(filter-out $@, $(MAKECMDGOALS))

# Saves the output to $(TEST_HTML_FILE)
test: scrape
	@./parse.py $(TEST_HTML_FILE)

# Scrapes player information
scrape:
	@./scrape.py players

# Generates an HTML file
parse:
	@./parse.py $(filter-out $@, $(MAKECMDGOALS))
