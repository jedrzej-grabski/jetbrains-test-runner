# Controller-generator task

## To run:

### Using PDM
* run `pdm install` to install dependencies
* run `pdm run controller` – to run the controller program
* run `pdm run generator` – to test the generator interactively

### Using Python
* create a virtual environment with `python -m venv .venv`
* activate a virtual environment with `source .venv/bin/activate`
* install dependencies with `pip install -r requirements.txt`
* run `python src/controller.py` – to run the controller program
* run `python src/generator.py` – to test the generator interactively

#### Using a custom generator:
* You can use a custom generator executable that adheres to the specification, by passing it to the controller through the `-g GENERATOR_EXECUTABLE` flag

## Testing
* With **PDM**, run `pdm run test`
* With **python**, run `pytest -v`
