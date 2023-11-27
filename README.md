# Investigation Influence Industry

## Install and Setup

Install:

`mamba env create -f environment.yml`

Activate the environment:

`mamba activate investigation-influence-industry` 

Updates to Python Package 

`mamba env update --file environment.yml --prune``

## Prerequisite 

Create a .env file and add:

* `ms_token` - from TikTok cookies to it for the TikTok-API (see: )
* 'openai_api_key' - add this if you are using BertTopics Open AI topic representation model.

and then run:

'source .env'

## Python Scripts

### Download original TikTok Posts

This calls the TikTok-API framework to download posts. For more info see: 

Run the Python file:

`python ./src/DownloadTikTokPosts.py`

### AWS Transcribe

This script initiates the transcription of the files in S3. Once the transcription jobs are complete the transcription text is downloaded to the `data/processed/transcription` folder.

Prerequisite - the AWS CLI and a public/private key setup to authenticate with the AWS account, all the audio to be transcribed should be uploaded to an S3 Bucket in AWS.

Run this:

`python ./src/AWSTranscribe.py`

### Analyse 

These Jupyter Notebooks  are self explanatory.