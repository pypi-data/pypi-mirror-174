# vim: sw=4:ts=4:et

#
# library for Falcon Sandbox
# Author: John Davison
# Originally written for https://github.com/ace-ecosystem/ACE
#

import io
import os
import logging
import json

try:
    from falconpy import FalconXSandbox
except ImportError as no_falconpy:
    raise SystemExit(
        "CrowdStrike FalconPy must be installed in order to use this application."
        ) from no_falconpy

# environment IDs
FS_ENV_LINUX_UBUNTU_16_64BIT = 300
FS_ENV_ANDROID = 200
FS_ENV_WIN_10_64BIT = 160
FS_ENV_WIN_7_64BIT = 110
FS_ENV_WIN_7_32BIT = 100

# sample submission status
FS_STATUS_UNKNOWN = 'unknown'
FS_STATUS_CREATED = 'created'
FS_STATUS_RUNNING = 'running'
FS_STATUS_ERROR = 'error'
FS_STATUS_SUCCESS = 'success'

# action scripts
FS_ACTION_SCRIPT_DEFAULT = 'default'
FS_ACTION_SCRIPT_MAX_ANTIEVASTION = 'default_maxantievasion'
FS_ACTION_SCRIPT_RANDOM_FILES = 'default_randomfiles'
FS_ACTION_SCRIPT_RANDOM_THEME = 'default_randomtheme'
FS_ACTION_SCRIPT_OPEN_IE = 'default_openie'

logger = logging.getLogger('falcon_sandbox')

class FalconSandbox(FalconXSandbox):

    def get_reports(self, debug, target_path, download, summary, *args, **kwargs):
        if summary:
            res = super().get_summary_reports(*args, parameters=None, **kwargs)
            target_path = target_path.format(type='summary.json') if '{type}' in target_path else target_path
        else:
            res = super().get_reports(*args, parameters=None, **kwargs)    
            target_path = target_path.format(type='json') if '{type}' in target_path else target_path

        assert res['body']['resources'], f"Could not get any report. Check your submission ID: \n {res}"
        res = json.dumps(res, indent=4) if debug else json.dumps(res['body']['resources'], indent=4)

        if download:
            with open(target_path, 'w') as f:
                f.write(res)
            logger.info(f"Wrote {target_path}")
        else:
            print(res)

    def get_submissions(self, debug, submitting=False, *args, **kwargs):
        res = super().get_submissions(*args, parameters=None, **kwargs)
        assert res['body']['resources'], f"Could not get submission's status. Check response: \n {res}"

        if submitting:
            return res['body']['resources'][0]['state']

        res = json.dumps(res, indent=4) if debug else json.dumps(res['body']['resources'], indent=4)
        print(res)

    def get_artifact(self, artifact_type, target_path, artifact_id=None, *args, **kwargs):
        res = super().get_reports(*args, parameters=None, **kwargs)
        assert res['body']['resources'], f"Could not get any report. Check your submission ID: \n {res}"

        if artifact_type == 'pcap':
            artifact_id = res['body']['resources'][0]['sandbox'][0].get('pcap_report_artifact_id')

        elif artifact_type == 'memdump':
            artifact_id = res['body']['resources'][0]['sandbox'][0].get('memory_strings_artifact_id')
        
        elif artifact_type == 'iocs.strict.csv':
            artifact_id = res['body']['resources'][0].get('ioc_report_strict_csv_artifact_id')

        elif artifact_type == 'iocs.broad.csv':
            artifact_id = res['body']['resources'][0].get('ioc_report_broad_csv_artifact_id')

        if not artifact_id:
            logger.error(f'{artifact_type} artifact is not available for this report')
            return

        artifact = super().get_artifacts(id=artifact_id)
        target_path = target_path.format(type=artifact_type) if '{type}' in target_path else target_path

        if isinstance(artifact, bytes):
            logger.info(f"Found artifact id {artifact_id} for {artifact_type}")
            with open(target_path, 'wb') as fp:
                f = io.BytesIO(artifact)
                while True:
                    chunk = f.read(io.DEFAULT_BUFFER_SIZE)
                    if not chunk:
                        break
                    fp.write(chunk)
            logger.info(f"Wrote {target_path}")
        else:
            loggger.error(f'Cannot get the file. Check response: {artifact}')

    def get_screenshots(self, target_dir, screenshot_ids=None, *args, **kwargs):
        res = super().get_reports(*args, parameters=None, **kwargs)
        assert res['body']['resources'], f"Could not get any report. Check your submission ID  \n {res}"

        screenshot_ids = res['body']['resources'][0]['sandbox'][0].get('screenshots_artifact_ids')
        
        if not screenshot_ids:
            print(f'Screenshots are not available for this report.')
            return

        os.makedirs(target_dir, exist_ok=True)
        for i, ss_id in enumerate(screenshot_ids):
            screenshot = super().get_artifacts(id=ss_id)
            if isinstance(screenshot, bytes):
                filepath = os.path.join(target_dir, f"screenshot{i + 1}.png")
                with open(filepath, 'wb') as fp:
                    fp.write(screenshot)
                logger.info(f"Wrote {filepath}")
            else:
                logger.error(f'Cannot get screenshot. Check response: \n {screenshot}')

    def get_sample(self, target_path, *args, **kwargs):

        if kwargs['password_protected']:
            target_path = os.path.split(target_path)[0] + 'sample.zip'

        res = super().get_sample(*args, parameters=None, **kwargs)
        if isinstance(res, bytes):
            logger.info(f"Found sample. Attempting to write it...")
            with open(target_path, 'wb') as fp:
                f = io.BytesIO(res)
                while True:
                    chunk = f.read(io.DEFAULT_BUFFER_SIZE)
                    if not chunk:
                        break
                    fp.write(chunk)
            logger.info(f"Wrote {target_path}")
        else:
            logger.error(f'Cannot get the sample. Check response: {res}')

    def delete_report(self, *args, **kwargs):
        res = super().delete_report(*args, parameters=None, **kwargs)
        if not res['body']['errors']:
            logger.info(f"Report {kwargs['ids']} was sucessfully deleted")
        else:
            raise Exception(f"Could not get delete the report. Check response: \n {res}")

    def delete_sample(self, *args, **kwargs):
        res = super().delete_sample(*args, parameters=None, **kwargs)
        if not res['body']['errors']:
            logger.info(f"Sample {kwargs['ids']} was sucessfully deleted")
        else:
            raise Exception(f"Could not get delete the sample. Check response: \n {res}")

    def submit(self, environment_id, url=None, file=None, *args, **kwargs):
        data = {'environment_id': int(environment_id), 
                'url': url}
        if file:
            logger.info("Uploading file...")
            file_name = os.path.split(file)[1]
            data['submit_name'] = file_name
            with open(file, 'rb') as fp:
                file_data = fp.read()
                res = super().upload_sample(file_data=file_data, file_name=file_name)
            assert res['body']['resources'], f"Could not retrieve the file's SHA256. Check response  \n {res}"
            data['sha256'] = res['body']['resources'][0]['sha256']
            logger.info(f"File uploaded sucessfully. Got the file's SHA256 and its name \n {res['body']['resources']}")
        
        supported_arguments = set([
            'action_script',
            'command_line',
            'document_password',
            'network_setting',
            'send_email_notifications',
            'submit_date',
            'submit_time',
            'user_tags'])

        for name, value in kwargs.items():
            if name not in supported_arguments:
                raise KeyError(f"unsupported argument {name}")
            
            if value is not None:
                data[name] = value
        res = super().submit(**data)
        submission_id = res['body']['resources'][0].get('id')
        if not submission_id:
            raise KeyError(f"Could not get submission_id. Check response \n {res}")
        logger.info(f"Got submission id {submission_id} for your submission")
        return submission_id