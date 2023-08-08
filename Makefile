help:
	@grep -E '^[a-zA-Z_-]+:.*?# .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?# "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install:  # Install base requirements to run project
	pip install -r requirements.txt

setup:  # Set up the project database
	python db/build_db.py
	echo 'DISCORD_TOKEN=' > .env

wipe-db:  # Delete's the project database
	rm -rf db/db.sqlite