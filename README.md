# Simple LangGraph Project

## How to run
1. Install python, pip, virtualenv in your system.
2. Clone the project `git clone https://github.com/arshiahaeri89/simple_langgraph_project && cd simple_langgraph_project`
3. Create a virtualenv named venv using `virtualenv venv`
4. Connect to virtualenv using `cd venv/Scripts && activate`
5. From the project folder, install packages using `pip install -r requirements.txt`
6. In the project folder, rename the `.env.example` to `.env` and replace `YOUR_API_KEY` with your LangSmith API key.
7. Now environment is ready. Run it by `langgraph dev`


Note: This runs the project in langgraph dev studio and you can give it any input from you in langgraph studio. if you want to run the input that is set in the *graph.py* file, you can run the file separately using `python graph.py`

## Running tests:
you can run unittests in tests.py using this command:
`python -m unittest -v test.py`
