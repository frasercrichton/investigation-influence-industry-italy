from dotenv import dotenv_values
import boto3
from botocore.exceptions import ClientError
from boto3 import client

import os
import pandas as pd
import logging
config = dotenv_values(".env")


# warnings.filterwarnings("ignore", message="Glyph (.*) missing from current font")
# sns.set_theme(style="darkgrid")

logger = logging.getLogger(__name__)

class Transcription:
    
    def __init__(self):
        self.transcribe_client = boto3.client('transcribe')
        self.s3_resource = boto3.resource('s3')
        self.s3_client = boto3.client('s3')
       
    def start_job(self, 
            job_name, media_uri, media_format, language_code, transcribe_client,
            vocabulary_name=None):
        """
        Starts a transcription job. This function returns as soon as the job is started.
        To get the current status of the job, call get_transcription_job. The job is
        successfully completed when the job status is 'COMPLETED'.

        :param job_name: The name of the transcription job. This must be unique for
                        your AWS account.
        :param media_uri: The URI where the audio file is stored. This is typically
                        in an Amazon S3 bucket.
        :param media_format: The format of the audio file. For example, mp3 or wav.
        :param language_code: The language code of the audio file.
                            For example, en-US or ja-JP
        :param transcribe_client: The Boto3 Transcribe client.
        :param vocabulary_name: The name of a custom vocabulary to use when transcribing
                                the audio file.
        :return: Data about the job.
        """
        try:
            job_args = {
                'TranscriptionJobName': job_name,
                'Media': {'MediaFileUri': media_uri},
                'MediaFormat': media_format,
                'LanguageCode': language_code}
            if vocabulary_name is not None:
                job_args['Settings'] = {'VocabularyName': vocabulary_name}
            response = self.transcribe_client.start_transcription_job(**job_args)
            job = response['TranscriptionJob']
            logger.info("Started transcription job %s.", job_name)
        except ClientError:
            logger.exception("Couldn't start transcription job %s.", job_name)
            raise
        else:
            return job
    
    def transcribe_bucket_contents(self, bucket_name : str ):
        for s3_object in self.s3_client.list_objects(Bucket=bucket_name)['Contents']:
            file_name = s3_object['Key']
            file_id = os.path.splitext(file_name)[0]
            s3_object_url = f'https://{bucket_name}.s3.amazonaws.com/{file_name}'
            print(s3_object_url)
            
            self.start_job(job_name=f'TranscribeTikTokAudio{file_id}', media_uri= s3_object_url, media_format='mp3', language_code='it-IT', transcribe_client=transcribe_client, vocabulary_name=None)

    def get_job_list(self, status: str, job_name_contains: str, max_results: str):
          # 'QUEUED'|'IN_PROGRESS'|'FAILED'|'COMPLETED'
        # Paginated Results
        # First Request made with no token
        response = self.transcribe_client.list_transcription_jobs(
            Status=status,
            JobNameContains=job_name_contains,
            MaxResults=max_results)
        transcription_job_summaries = response['TranscriptionJobSummaries']
        
        # TranscriptionJobSummaries
        # if there are more results "NextToken" is present so page forward 
        while ("NextToken" in response):
            next_token = response['NextToken']
            response = self.transcribe_client.list_transcription_jobs(
                Status=status,
                JobNameContains=job_name_contains,
                NextToken=next_token,
            MaxResults=max_results)        
            transcription_job_summaries.append(response['TranscriptionJobSummaries'])
        # print(transcription_job_summaries)    
        # df = pd.DataFrame(transcription_job_summaries)
        # df.to_json(f'./debug.json')

        return transcription_job_summaries
    
    def get_transcription_job(self, job_name: str):
        return self.transcribe_client.get_transcription_job(TranscriptionJobName=job_name)

    def download_transcript(self, job_id: str):
        transcription_job = transcription.get_transcription_job(job_id)
        uri = transcription_job['TranscriptionJob']['Transcript']['TranscriptFileUri']

        df = pd.read_json(uri)
        df.to_json(f'./data/processed/transcription/original/{job_id}.json')

if __name__ == "__main__":
    bucket_name = 'frasercrichton-com-audio-transcription'
    transcription = Transcription()
    
    transcription_results = transcription.get_job_list(status='COMPLETED', job_name_contains = 'TranscribeTikTokAudio', max_results = 100) 
    print(len(transcription_results))    
    for job in transcription_results:
        transcription.download_transcript(job['TranscriptionJobName'])
