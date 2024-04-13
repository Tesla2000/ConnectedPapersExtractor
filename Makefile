.PHONY: setup install_precommit activate_venv clean

setup: venv create_package_structure activate_venv install_requirements git_init git_add precommit_install build_docs

venv:
	python3 -m venv venv

activate_venv:
	. venv/bin/activate

install_requirements:
	venv/bin/python -m pip install -r requirements.txt

git_init:
	git init

git_add:
	git add .

precommit_install:
	pre-commit install

build_docs:
	sh build_docs.sh

clean:
	rm -rf venv

create_package_structure:
	$(eval package_name := $(shell basename "$(shell pwd)"))
	mkdir -p "src/$(package_name)"
	touch "src/$(package_name)/__init__.py"
