# Flights

A quick analysis project to determine possible destinations for the heidedagen 2024

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This project is created to determine the possible flights from Amsterdam schiphol during the stated period of the heidedagen in 2024.

## Features

- **Flight search**: Users can search for all flights departing from amsterdam schiphol between a depart from and to datetime window


## Getting Started

To get started with Flights, follow these steps:

1. Clone the repository: `git clone https://github.com/your-username/flights.git`
2. Create a personal virtual environment:
    - On Windows: `python -m venv venv`
    - On macOS and Linux: `python3 -m venv venv`
3. Install all requirements from the requirements.txt file:
    `pip install -r requirements.txt`
4. go to www.developer.schiphol.nl and create an account to get your personal app_id and app_key
5. Create a file named 'api_settings.py' in the 'src' directory and add the following code:
    ```python
    from pydantic import BaseModel
    from loguru import logger


    class API_settings(BaseModel):
        api_id: str = your_app_id
        api_key: str = your_app_key


    settings = API_settings()
    logger.add(settings.logfile, level=settings.loglevel)

    ```
    

## Usage

Once you have installed the requirements, you can run the application using the following command.
To run the complete application, use the following command:
```bash
python src/main.py
```

To only update the database with the latest flights, use the following command:
```bash
python src/flights.py
```

To run the preprocessing of the data (only necessary with new flight data), use the following command:
```bash
python src/preprocessing.py
```

To recreate the map of the flights, use the following command:
```bash
python src/map.py
```

## Contributing

We welcome contributions from the community to enhance Flights. To contribute, please follow these guidelines:

- Fork the repository and create a new branch for your feature or bug fix.
- Make your changes and ensure that the code passes all tests.
- Submit a pull request with a clear description of your changes and the problem it solves.

## License

Flights is distributed under the [MIT License](https://opensource.org/licenses/MIT). You are free to use, modify, and distribute this software.
