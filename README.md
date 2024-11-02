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
    
## Testing
* With **PDM**, run `pdm run tests`
* With **python**, run `pytest -v`
