# Define installation directories
PREFIX ?= /usr/local
BINDIR ?= $(PREFIX)/bin

# Define the name of the script
SCRIPT_NAME = passive

.PHONY: all install uninstall help

all: help

help:
	@echo "Usage:"
	@echo "  make install     Install the CLI application"
	@echo "  make uninstall   Uninstall the CLI application"
	@echo "  make help        Show this help message"

install:
	@echo "Installing the CLI application..."
	@echo '#!/bin/sh' > $(SCRIPT_NAME)
	@echo 'python3 $(shell pwd)/main.py $$@' >> $(SCRIPT_NAME)
	chmod +x $(SCRIPT_NAME)
	sudo mv $(SCRIPT_NAME) $(BINDIR)/$(SCRIPT_NAME)
	@echo "Installation complete. You can now use the '$(SCRIPT_NAME)' command."

uninstall:
	@echo "Uninstalling the CLI application..."
	sudo rm -f $(BINDIR)/$(SCRIPT_NAME)
	@echo "Uninstallation complete. The '$(SCRIPT_NAME)' command has been removed."
