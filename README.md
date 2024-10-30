# Controller-generator task

## To run:

### Setup
* using `pdm`
    * run `pdm install` to install dependencies
    * run `pdm venv activate` to enter a virtual environment
    
* using bare python
    * create a virtual environment with `python -m venv .venv`
    * activate with `source .venv/bin/activate`
    * install dependencies with `pip install -r requirements.txt`
    

### Running
* To test-run the controller, run `python src/controller.py -g GENERATOR_EXECUTABLE`
* `GENERATOR_EXECUTABLE` defaults to `src/generator.py` 
* You can also directly interact with the generator via the standard input/output by running `python src/generator.py`


## Testing
* To run test, run `python -m pytest -v` in the root directory.
