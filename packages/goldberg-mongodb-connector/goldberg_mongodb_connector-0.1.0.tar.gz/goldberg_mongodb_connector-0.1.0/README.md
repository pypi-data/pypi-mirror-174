# project-goldberg-mongodb

This repo should be used as connection to the MongoDB database for the Goldberg project.

## Setup repository for development

1. Create an environment with poetry

    ```bash
    poetry install
    ```

2. Create a `.env` file with the following content:

    ```bash
    MONGO_URI=mongodb://localhost:27017
    MONGO_DB=goldberg
    ```

3. Run the tests

    ```bash
    poetry run pytest
    ```
