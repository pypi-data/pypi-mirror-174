#!/usr/bin/env python3

import os
import sys
import time
import json
import base64
import logging
import argparse
import coloredlogs
import pprint

from falcon_sandbox.helpers import load_config, create_user_config
from falcon_sandbox import FS_STATUS_CREATED, FS_STATUS_RUNNING, FalconSandbox

# configure logging #
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - [%(levelname)s] %(message)s')

logger = logging.getLogger('falcon_sandbox')
coloredlogs.install(level='INFO', logger=logger)

def main():
    parser = argparse.ArgumentParser(description="A command line client for interacting with the Falcon Sandbox library written for the ACE Ecosystem.")
    parser.add_argument('-d', '--debug', action="store_true", help="Set logging to DEBUG", default=False)
    parser.add_argument('--ignore-proxy', action='store_true', default=False, help='Ignore system proxy')
    parser.add_argument('--client-id', action="store", help="Pass client id to use. Overrides config")
    parser.add_argument('--client-secret', action='store',help="Pass client secret to use. Overrides any configured client secrect")

    subparsers = parser.add_subparsers(dest='instruction')

    parser_submit = subparsers.add_parser('submit', help='Upload and submit a sample')
    parser_submit.add_argument('-f', '--file', action='store', help="file to submit")
    parser_submit.add_argument('-u', '--url', action='store', help="url to submit")
    parser_submit.add_argument('-e', '--environment_id', action='store', default='100', help='Enviroment to submit to. Default:100. Use "falcon_sandbox get system -e" to see availble environments')
    parser_submit.add_argument('-o', '--output-target-path', help="Where to write the result file (absolute path) (default: {submission_id}.falcon.{report-or-file_type})", default='{submission_id}.falcon.{type}')
    parser_submit.add_argument('--arguments', action='store', default={}, type=json.loads, help="Arguments to customize submission. Must be a dictionary")

    parser_get = subparsers.add_parser('get', help='Get samples, artifacts, and results from the server')
    parser_get_subs = parser_get.add_subparsers(dest='get_commands')
    
    parser_get_report = parser_get_subs.add_parser('report', help='Get report info')
    parser_get_report.add_argument('submission_id', nargs='+', help="The Falcon submission id")
    parser_get_report.add_argument('-o', '--output-target-path', help="Where to write the result file (absolute path) (default: {submission_id}.falcon.{report-or-file_type})", default='{submission_id}.falcon.{type}')
    parser_get_report.add_argument('-d', '--download', action='store_true', help="Download report")
    parser_get_report.add_argument('-st', '--state', action='store_true', help="Get the submission id report state")
    parser_get_report.add_argument('-sum', '--summary', action='store_true', help="Get the report summary")
    parser_get_report.add_argument('-i', '--iocs', action='store', choices=['strict', 'broad'], help="Get report IOCs")
    parser_get_report.add_argument('-p', '--pcap', action='store_true', help="Get any available pcap for this submission")
    parser_get_report.add_argument('-m', '--memory-dumps', action='store_true', help="Get any available memory dumps for this submission")
    parser_get_report.add_argument('-ss', '--screenshots', action='store_true', help="Get the submission screen shots")
    
    parser_get_sample = parser_get_subs.add_parser('sample', help='Retrieves the file associated with the given ID (SHA256)')
    parser_get_sample.add_argument('file_SHA256', help="the file SHA256")
    parser_get_sample.add_argument('-safe', '--password-protected', action='store_true', help="Zip the sample with password 'infected'")
    parser_get_sample.add_argument('-o', '--output-target-path', help="Where to write the sample file (absolute path) (default: {file_SHA256})", default='{file_SHA256}')

    parser_delete = subparsers.add_parser('delete', help="Delete reports or samples")
    parser_delete.add_argument('-r', '--report', action='store', help="Delete a report based on the submission ID")
    parser_delete.add_argument('-s', '--sample', action='store', help="Delete a sample based on the file SHA256")

    args = parser.parse_args()

    if args.debug:
        coloredlogs.install(level='DEBUG', logger=logger)

    config = load_config(required_options=['ignore_proxy', 'client_id', 'client_secret'])
    if config is None:
        set_config = input("Did not find user configuration, would you like to create one? [Y/n]") or 'Y'
        if set_config == 'Y' or set_config == 'y':
            client_id = input("Client ID of your API client: ")
            client_secret = input("Client secret associated with the client ID: ")
            ignore_proxy = input("Do you need to use the system proxy to connect to the sandbox? [Y/n] ") or 'Y'
            ignore_proxy = True if ignore_proxy.upper() == 'Y' else False
            create_user_config(client_id, client_secret, ignore_proxy)
            config = load_config(required_options=['ignore_proxy', 'client_id', 'client_secret'])
        else:
            return

    if config.getboolean('ignore_proxy') or args.ignore_proxy:
        if 'https_proxy' in os.environ:
            del os.environ['https_proxy']
    
    client_id = args.client_id if args.client_id else config['client_id']
    client_secret = args.client_secret if args.client_secret else config['client_secret']

    falcon = FalconSandbox(client_id=client_id, client_secret=client_secret)

    # if we have a submission_id after running the users commands the 
    # default behavior will be to wait for that job to complete
    # and write the results of the job to a local json file
    submission_id = None

    if args.instruction == 'submit':
        if args.file:
            submission_id = falcon.submit(args.environment_id, file=args.file, **args.arguments)
        if args.url:
            submission_id = falcon.submit(args.environment_id, url=args.url, **args.arguments)

    if args.instruction == 'get':
        if args.get_commands == 'report':
            if args.output_target_path == '{submission_id}.falcon.{type}':
                args.output_target_path = args.output_target_path.format(submission_id=args.submission_id, type='{type}').replace('[', '').replace(']', '').replace("'", '')
            if any((args.state, args.pcap, args.memory_dumps, args.iocs, args.screenshots)):            
                if args.state:
                    falcon.get_submissions(args.debug, ids=args.submission_id)
                if args.pcap:
                    falcon.get_artifact('pcap', args.output_target_path, ids=args.submission_id)
                if args.memory_dumps:
                    falcon.get_artifact('memdump', args.output_target_path, ids=args.submission_id)
                if args.iocs:
                    falcon.get_artifact(f'iocs.{args.iocs}.csv', args.output_target_path, ids=args.submission_id)
                if args.screenshots:
                    target_dir = f"{args.submission_id}.screenshots".replace('[', '').replace(']', '').replace("'", '') if '{type}' in args.output_target_path else args.output_target_path
                    falcon.get_screenshots(target_dir, ids=args.submission_id)
            else:
                falcon.get_reports(args.debug, args.output_target_path, args.download, args.summary, ids=args.submission_id)
        
        if args.get_commands == 'sample':
            if args.output_target_path == '{file_SHA256}':
                args.output_target_path = args.output_target_path.format(file_SHA256=args.file_SHA256)
            falcon.get_sample(args.output_target_path, ids=args.file_SHA256, password_protected=args.password_protected)

    if args.instruction == 'delete':
        if args.report:
            falcon.delete_report(ids=args.report)
        if args.sample:
            falcon.delete_sample(ids=args.sample)

    if submission_id:
        time.sleep(1)
        submission_state = falcon.get_submissions(args.debug, submitting=True, ids=submission_id)
        initial_time = int(time.time())
        while submission_state == FS_STATUS_CREATED or submission_state == FS_STATUS_RUNNING:
            if (int(time.time()) - initial_time) % 10 == 0:
                initial_time += 9 # essentially, log again about every 9 seconds
                logger.info(f"Submission {submission_id} is in {submission_state.upper()} state...")
                submission_state = falcon.get_submissions(args.debug, submitting=True, ids=submission_id)
        logger.info(f"Submission {submission_id} has moved to {submission_state.upper()} state")
        if args.output_target_path == '{submission_id}.falcon.{type}':
            args.output_target_path = args.output_target_path.format(submission_id=args.submission_id, type='{type}')
        falcon.get_reports(args.debug, args.output_target_path, True, False, ids=submission_id)