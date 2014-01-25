.PHONY: all

all:
	-@$(RM) words.db
	@echo "Running initdb.py. This may take a while."
	./initdb.py