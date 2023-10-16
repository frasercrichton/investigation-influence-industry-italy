# Investigation-Influence-Industry

## Install and Setup

Install:

`mamba env create -f environment.yml`

Activate the environment:

`mamba activate investigation-influence-industry` 

Updates to Python Package 

`mamba env update --file environment.yml --prune``

## Prerequisite 

Create a .env file and add `ms_token` from cookies to it and then run:

'source .env'

## Retrieve the original

Run the Python file:

`python ./src/DownloadTikTokPosts.py`

## Analyse the data with the Jupyter Notebook

The Notebook 

- extract and clean the data
- translate from Italian to English
- download resources like cover images and videos
- do OCR text extraction on cover images 
  
Run some basic analytics including:

- how often and when did Meloni post?
- which posts were the most liked and shared
- what were the most common words used
