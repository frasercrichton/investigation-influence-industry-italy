# Investigation-Influence-Industry

## Install and Setup

Install:

`mamba env create -f environment.yml`

Activate the environment:

`mamba activate investigation-influence-industry` 

Updates to Python Package 

`mamba env update --file environment.yml --prune``

Run Jupyter Notebook:

'jupyter notebook'

And then in Visual Studio Code:

`cmd+shft+p` `Jupyter: Specify Jupyter Server for Connections`

And copy the Jupyter Notebook start up url e.g. http://localhost:8889/?token=b53e209ebb6ccb01b721de9a597a45a69f6b6fb2fe479a88 into the input box. 

Create a .env file and add `ms_token` from cookies to it

'source .env'

Run the Python file:

`python ./src/TikTok.py`


