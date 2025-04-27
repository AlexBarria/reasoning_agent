# reasoning_agent
## Overview
`reasoning_agent` is a project designed to test and evaluate various reasoning large language models (LLMs) to solve complex tasks. The goal is to explore the capabilities, limitations, and potential applications of these models in real-world scenarios.

## Features
- **Model Evaluation**: Compare the performance of different LLMs on reasoning tasks.
- **Task Complexity**: Test models on tasks of varying complexity.
- **Customizable Framework**: Easily add new tasks or integrate additional models.
- **Metrics and Analysis**: Generate a comparison between the response provided by the LLM and the programmatic calculation using Python to validate the accuracy of the LLM model.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/AlexBarria/reasoning_agent.git
    cd reasoning_agent
    ```
2. Install Poetry if you don't already have it:
    ```bash
    pip install poetry
    ```
3. Use Poetry to install the dependencies and create a virtual environment:
    ```bash
    poetry install
    ```

## Usage
1. Run the main script to evaluate models:
    ```bash
    poetry run python src/application.py 
    ```
2. Customize the tasks or models by editing the configuration files in the `src/` directory.

## Project Structure
```
reasoning_agent/
├── src/                  # Main source code for the project
│   ├── static/           # Contains pictures and other elements used in the UI
│   ├── templates/        # Includes model integration templates for the UI
│   ├── agent.py          # Core logic for task definitions and implementations
│   └── application.py    # Script with the definition of the app
├── poetry.lock           # Poetry lock file for dependency management
├── poetry.toml           # Poetry configuration file
├── wine_concentration_val.py # Script for specific task evaluation 
└── README.md             # Project documentation
```

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description of your changes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For questions or feedback, please contact [alexbarria14@gmail.com].

