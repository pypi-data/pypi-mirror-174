import json
import requests
import boto3
import base64
import io
import gzip
from typing import Dict, Union, Sequence, IO, NoReturn
from time import sleep

__version__ = '1.0.7'


class Coegil:

    def __init__(self, api_key: str, instance_name: str = 'prod', auto_validate: bool = True,
                 proxy_configuration: Dict = None):
        """
        Access the Coegil Public API from code
        Args:
            api_key (str): The API Key
            instance_name (str): The name of the instance.  As Coegil Support for details.
            auto_validate (bool): Run a test to validate the API Key on construction
            proxy_configuration (Dict): Optionally pass proxy config (for the python requests library).
        """
        self._api_key: str = api_key
        self._instance_name = instance_name.lower()
        self._proxy_configuration: Dict = proxy_configuration if proxy_configuration is not None else {}
        if auto_validate:
            self.validate()

    def validate(self):
        """
        Validates your configuration.
        """
        result = self._call_api('GET', '/public/management/key/validate', {})
        return result

    def generate_temporary_api_key(self, duration_hours: int = 36) -> Dict:
        """
        Generates a temporary API key for the given user.  Temporary API keys cannot be used for this API.
        Args:
            duration_hours (int): The length of the key.  The max is 36 hours.

        Returns:
            The temporary API key and expiration info
        """
        result = self._call_api('PUT', '/public/management/key/temporary', {
            'duration_hours': duration_hours
        })
        return result

    def query_database(self, query_text: str, asset_id: str, database_name: str, engine: str = 'my_sql') -> Dict:
        """
        Runs an ad hoc database query.
        Args:
            query_text (str): The query to run.
            asset_id (str): The asset's unique identifier.
            database_name (str): Your database artifact's name.
            engine (str): The database engine (defaults to mysql)
        Returns:
            The results of the query
        """
        result = self._call_api('POST', f'/public/query/{engine}', {
            'asset_id': asset_id,
            'database_name': database_name,
            'query_text': query_text
        })
        return result

    def run_saved_database_query(self, asset_id: str, query_name: str, parameters: Dict = None) -> Dict:
        """
        Runs an ad hoc database query.
        Args:
            asset_id (str): The asset's unique identifier.
            query_name (str): Your saved query's name.
            parameters (Dict): Parameter overrides.
        Returns:
            The results of the query
        """
        result = self._call_api('POST', '/public/query/stored', {
            'asset_id': asset_id,
            'query_name': query_name,
            'query_params': parameters
        })
        return result

    def queue_schedule(self, asset_id: str, job_name: str, schedule_name: str,
                       variable_override: Dict = None) -> NoReturn:
        """
        Queues a job or pipeline schedule to be invoked.  The queue is drained in batches defined by the schedule.
        Args:
            asset_id (str): The asset's unique identifier.
            job_name (str): The name of the job artifact (pipeline, notebook, or trigger).
            schedule_name (str): Required unless you are invoking a trigger.
            variable_override (Dict): Parameter overrides.
        Returns:
        """
        self._call_api('PUT', '/public/schedule/queue', {
            'asset_id': asset_id,
            'job_name': job_name,
            'schedule_name': schedule_name,
            'variable_override': variable_override
        })

    def invoke_schedule(self, asset_id: str, job_name: str, schedule_name: str,
                        variable_override: Dict = None) -> Dict:
        """
        Invoke a job or pipeline schedule.
        Args:
            asset_id (str): The asset's unique identifier.
            job_name (str): The name of the job artifact (pipeline, notebook, or trigger).
            schedule_name (str): Required unless you are invoking a trigger.
            variable_override (Dict): Parameter overrides.
        Returns:
            An identifier to be used for tracking
        """
        return self._call_api('PUT', '/public/schedule', {
            'asset_id': asset_id,
            'job_name': job_name,
            'schedule_name': schedule_name,
            'variable_override': variable_override
        })

    def get_schedule_status(self, job_id: str) -> Dict:
        """
        Gets the status of an invoked job.
        Args:
            job_id (str): The job run id returned from the invoke call.
        Returns:
            The status of the invoked job
        """
        return self._call_api('GET', '/public/schedule/status', {
            'job_id': job_id
        })

    def list_schedules(self, asset_id: str) -> Sequence[Dict]:
        """
        List all of the schedules in a given asset.
        Args:
            asset_id (str): The asset's unique identifier.
        Returns:
            A list of schedules
        """
        return self._call_api('GET', '/public/schedule', {
            'asset_id': asset_id
        })

    def list_artifacts(self, asset_id: str) -> Sequence[Dict]:
        """
        Lists all of the artifacts in a given asset.
        Args:
            asset_id (str): The asset's unique identifier.
        Returns:
            A list of artifacts
        """
        return self._call_api('GET', '/public/artifact', {
            'asset_id': asset_id
        })

    def list_flask_services(self) -> Sequence[Dict]:
        """
        Retrieves all active flask/ploty dash sessions for the calling user.
        Returns:
            A list of active services
        """
        return self._call_api('GET', '/public/flask', {})

    def terminate_flask_service(self, session_id: str, port: int = None) -> NoReturn:
        """
        Deletes an active flask/ploty dash service.
        Args:
            session_id (str): The session id as seen in the GET method.
            port (int): Optionally pass the port.  If no port is defined, the entire service will be terminated.
        """
        return self._call_api('DELETE', '/public/flask', {
            'session_id': session_id,
            'port': port
        })

    def start_flask_service(self, session_type: str, asset_id: str = None, artifact_name: str = None, name: str = None,
                            wait_for_startup: bool = True, is_shared_session: bool = False) -> NoReturn:
        """
        Attempts to start a flask or plotly dash session.  If no artifact is passed, this endpoint will start a session on standby.  If an artifact is passed, this endpoint will do one of the following:

            1 - If the desired service is already running, nothing will happen.
            2 - If there is an available session, we will attach the service to it
            3 - If there is no available session, we will start a session and attach the service to the service.
        Args:
            session_type (str): Either PLOTLY_DASH or FLASK_SERVICE.
            asset_id (str): The asset id of your Plotly Dashboard or Flask Service artifact.  Required if using an artifact
            artifact_name (str): The name of your Plotly Dashboard or Flask Service artifact.
            name (str): Optionally name your session.  This only applies if the endpoint creates a session.
            wait_for_startup (bool): Whether or not to wait for the service to start
            is_shared_session (bool): If you are calling this from a service account, use this to start a shared session.  Talk to Coegil Support to learn more.
        """
        self._call_api('PUT', '/public/flask', {
            'session_type': session_type,
            'asset_id': asset_id,
            'artifact_name': artifact_name,
            'name': name,
            'is_shared_session': is_shared_session
        })
        if not wait_for_startup:
            return
        sleep_seconds = 5
        wait_seconds = 120
        for _ in range(int(wait_seconds / sleep_seconds)):
            all_services = self.list_flask_services()
            for status in all_services:
                if status['session']['type'] == 'FLASK_SERVICE' and status['session']['status'] == 'Running':
                    service_ret = {
                        'session': status['session'],
                        'connection_details': {
                            'host': status['session']['connection_details']['host'],
                            'query_parameters': {
                                'token': status['session']['connection_details']['token']
                            }
                        },
                        'service': None
                    }
                    if artifact_name is None:
                        return service_ret
                    else:
                        for service in status['services']:
                            service_ret['service'] = service
                            service_ret['connection_details']['host'] += f':{service["port"]}'
                            if service['asset']['id'] == asset_id and service['artifact']['name'] == artifact_name:
                                return service_ret
            sleep(sleep_seconds)
        raise Exception("The service failed to start.")

    def read_file(self, asset_id: str, artifact_name: str) -> bytes:
        """
        Reads the contents of a file artifact.
        Args:
            asset_id (str): The asset's unique identifier.
            artifact_name (str): The artifact's name.
        Returns:
            A contents of the file
        """
        s3_credentials = self._call_api('GET', '/public/artifact/credentials', {
            'asset_id': asset_id,
            'artifact_name': artifact_name
        })
        s3_bucket = s3_credentials['Bucket']
        s3_key = s3_credentials['Key']
        credential_override = s3_credentials['Credentials']
        return self._get_s3_object(s3_bucket, s3_key, credential_override=credential_override)

    def read_file_in_chunks(self, asset_id: str, artifact_name: str, chunk_size: int = 1024) -> Sequence[bytes]:
        """
        Reads the contents of a file artifact.  This call yields each chunk.  This is useful for very large artifacts.  read_file() should be used for most cases.
        Args:
            asset_id (str): The asset's unique identifier.
            artifact_name (str): The artifact's name.
            chunk_size (int): Specify how many bytes each chunk should be
        Returns:
            A contents of the file by chunk
        """
        s3_credentials = self._call_api('GET', '/public/artifact/credentials', {
            'asset_id': asset_id,
            'artifact_name': artifact_name
        })
        s3_bucket = s3_credentials['Bucket']
        s3_key = s3_credentials['Key']
        credential_override = s3_credentials['Credentials']
        return self._get_s3_object_chunks(s3_bucket, s3_key, chunk_size=chunk_size,
                                          credential_override=credential_override)

    def save_file(self, asset_id: str, artifact_name: str, contents: Union[str, bytes],
                  artifact_sub_type: str = None) -> NoReturn:
        """
        Reads the contents of a file artifact.
        Args:
            asset_id (str): The asset's unique identifier.
            artifact_name (str): The artifact's name.
            contents (Union[str, bytes]): The contents to be uploaded
            artifact_sub_type (str): Optionally pass the artifact sub type.  Talk to Coegil before using this field
        Returns:
            A contents of the file
        """
        if artifact_name.endswith('.ipynb') and artifact_sub_type is None:
            artifact_sub_type = 'jupyter_python'
        self._upload_file(asset_id, artifact_name, contents, artifact_sub_type=artifact_sub_type)

    def _call_api(self, action_method: str, endpoint: str, payload: Dict):
        url = self._build_url(endpoint)
        headers = self._get_headers()
        proxies = self._proxy_configuration
        action_method = action_method.upper()
        if action_method == 'GET':
            r = requests.get(url, headers=headers, params=payload, proxies=proxies)
        elif action_method == 'POST':
            r = requests.post(url, headers=headers, data=json.dumps(payload), proxies=proxies)
        elif action_method == 'PUT':
            r = requests.put(url, headers=headers, data=json.dumps(payload), proxies=proxies)
        elif action_method == 'DELETE':
            r = requests.delete(url, headers=headers, params=payload, proxies=proxies)
        else:
            raise Exception(f'Unknown action method.  Method={action_method}')
        return self._parse_result(r)

    def _build_url(self, endpoint: str) -> str:
        if not endpoint.startswith('/'):
            endpoint = '/' + endpoint
        instance_name = self._instance_name
        return f'https://api.{instance_name}.app-coegil.com{endpoint}'

    def _parse_result(self, r: requests.Response):
        result = r.json()
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise Exception(result) from e
        metadata = result['metaData']
        if metadata['compressData']:
            decompressed_data = self._decompress(result['data'])
        else:
            decompressed_data = result['data']
        return json.loads(decompressed_data)

    def _get_headers(self) -> Dict:
        headers = {
            'api_version': str(2),
            'coegil_api_key': self._api_key,
            'compress_results': str(True),
            'origin_url': 'PYTHON_SDK',
            'ui_version': __version__
        }
        return headers

    @staticmethod
    def _decompress(compressed_object: Union[str, bytes]) -> str:
        if isinstance(compressed_object, str):
            compressed_bytes = base64.b64decode(compressed_object)
        else:
            compressed_bytes = compressed_object
        in_ = io.BytesIO()
        in_.write(compressed_bytes)
        in_.seek(0)
        try:
            with gzip.GzipFile(fileobj=in_, mode='rb') as fo:
                gunzipped_bytes_obj = fo.read()

            return gunzipped_bytes_obj.decode()
        except OSError as e:
            if 'Not a gzipped file' in str(e):
                return compressed_object.decode() if isinstance(compressed_object, bytes) else compressed_object
            raise e

    def _upload_file(self, asset_id: str, artifact_name: str, contents: Union[str, bytes], artifact_sub_type: str = None):
        s3_credentials = self._call_api('get', '/public/artifact/credentials', {
            'asset_id': asset_id,
            'artifact_name': artifact_name,
            'artifact_sub_type': artifact_sub_type
        })
        s3_bucket = s3_credentials['Bucket']
        s3_key = s3_credentials['Key']
        artifact_id = s3_credentials['ArtifactGuid']
        credential_override = s3_credentials['Credentials']
        content_type = None
        split_file_name = artifact_name.rsplit('.', 1)
        if len(split_file_name) > 1:
            extension = split_file_name[1]
            if extension == 'xlsx' or extension == 'xls':
                content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            elif extension == 'ppt' or extension == 'pptx':
                content_type = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
            elif extension == 'docx':
                content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            elif extension == 'csv':
                content_type = 'text/csv'
            elif extension == 'json':
                content_type = 'application/json'
            elif extension == 'yml' or extension == 'yaml':
                content_type = 'text/yaml'
            elif extension == 'pdf':
                content_type = 'application/pdf'
        self._put_s3_object(s3_bucket, s3_key, contents, content_type=content_type,
                            credential_override=credential_override)
        self._call_api('POST', '/public/artifact', {
            'asset_id': asset_id,
            'artifacts': [{
                'artifact_name': artifact_name,
                'artifact_type': 'S3',
                'artifact_sub_type': artifact_sub_type,
                'artifact_id': artifact_id
            }]
        })

    def _put_s3_object(self, bucket, key, body: Union[IO, str, bytes], content_type: str = None,
                       credential_override=None):
        client = self._get_client('s3', credential_override)
        if isinstance(body, str):
            body = str.encode(body)
        if isinstance(body, bytes):
            body = io.BytesIO(body)
        params = {
            'ACL': 'private'
        }
        if content_type is not None:
            params['ContentType'] = content_type
        client.upload_fileobj(body, bucket, key, params)

    def _get_s3_object_chunks(self, bucket, key, chunk_size: int = 1024, credential_override=None) -> Sequence[bytes]:
        client = self._get_client('s3', credential_override)
        ret = client.get_object(
            Bucket=bucket,
            Key=key
        )
        body = ret.get('Body')
        return body.iter_chunks(chunk_size=chunk_size)

    def _get_s3_object(self, bucket, key, credential_override=None) -> bytes:
        client = self._get_client('s3', credential_override)
        body = None
        try:
            ret = client.get_object(
                Bucket=bucket,
                Key=key
            )
            body = ret.get('Body')

            # https://bugs.python.org/issue42853
            # We can only download < 2GB this way - otherwise we have to use the slow method
            content_length_bytes = ret['ContentLength']
            two_gb_bytes = 2000000000
            if content_length_bytes >= two_gb_bytes:
                # 1 GB chunks
                chunk_size = 1000000000
                ret_bytes = bytearray()
                for chunk in body.iter_chunks(chunk_size=chunk_size):
                    ret_bytes.extend(chunk)
            else:
                ret_bytes = ret.get('Body').read()
            return ret_bytes
        finally:
            if body is not None:
                body.close()

    @staticmethod
    def _get_client(name, credential_override):
        if credential_override is None:
            return boto3.client(name)
        else:
            params = {
                'aws_access_key_id': credential_override['AccessKeyId'],
                'aws_secret_access_key': credential_override['SecretAccessKey'],
            }
            session_token = credential_override.get('SessionToken')
            if session_token is not None:
                params['aws_session_token'] = session_token
            session = boto3.Session(**params)
            client = session.client(name)
            return client
