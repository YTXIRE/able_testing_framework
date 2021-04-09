# Able Testing Framework 
This product is a framework for implementing user interface tests.

The framework includes modules for working with the UI, API, and database.

The framework is based on pytest. Selene is responsible for working with the elements on the page. Working with the database is done via ORM via the SQLAlchemy package. API requests are sent via requests.

# Getting started

1. Clone the repository to your local folder.
2. Run the command:
``pip install -r requirements.txt``
   
The framework implements the Page Object method of operation. All the necessary elements are described in the components folder. The configuration file is located in the config folder. Core contains the logic for working with the database. The models folder includes custom methods for working with the database. The pages folder stores the classes written by page object. The tests folder contains the implemented tests. The conftest file contains auxiliary methods for running tests.

This framework is distributed completely free of charge.
