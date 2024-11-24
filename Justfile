# Default goal: help
help:
    @just --list

# Dump brew bundle
brew:
    brew bundle dump -f --no-vscode --file=utils/config/Brewfile
