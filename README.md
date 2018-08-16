[![Build Status](https://travis-ci.org/Mirr77/stackoverflowliteAPI.svg?branch=develop)](https://travis-ci.org/Mirr77/stackoverflowliteAPI)
[![Coverage Status](https://coveralls.io/repos/github/Mirr77/stackoverflowliteAPI/badge.svg?branch=develop)](https://coveralls.io/github/Mirr77/stackoverflowliteAPI?branch=develop)


# StackOverflowLite

StackOverflowLite enables users to ask questions, receieve answers for their questions and answer oother people's questions.


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What you need to get started:

- [Python 3](https://www.python.org/download/releases/3.0/)

- [virtualenv](https://virtualenv.pypa.io/en/stable/)

- [virtualenv-wrapper](http://virtualenvwrapper.readthedocs.io/en/latest/)

### Installing

Enter the following commands on your terminal one by one:

- *Clone this repo :*

    ```$ git clone https://github.com/Mirr77/stackoverflowliteAPI.git```

- *Move to working directory :*

    ``` $ cd stackoverflowlite ```

- *Create your Virtual Environment :*

    ```$ mkvirtualenv -p python3 [environment-name] ```

- *Activate your virtual environment :*

    ```$ workon [environment-name] ```

- *Install project requirements :*

    ```$ pip install -r requirements.txt ```

- *Start the app :*

    ```$ python3 run.py ```

- *Finally navigate to ```http://localhost:5000/``` on your browser*

## Running the tests

- With Coverage Report:

    ```$ coverage run -m pytest ```

- Without Coverage:

    ```$ pytest ```

## Built With

- [Flask](http://flask.pocoo.org/)

## Authors

- [Mirr77](https://github.com/Mirr77)
