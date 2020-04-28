#!/usr/bin/zsh

chdir tests
coverage run -m pytest test_postgres_restorer.py
