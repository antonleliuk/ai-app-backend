#!/bin/bash
poetry shell
poetry install
poetry run python ./src/app/start.py