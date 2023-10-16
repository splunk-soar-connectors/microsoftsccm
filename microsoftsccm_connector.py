# File: microsoftsccm_connector.py
#
# Copyright (c) 2017-2023 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.
#
#
# Standard library imports
import json

# Phantom App imports
import phantom.app as phantom
from phantom.action_result import ActionResult
from phantom.base_connector import BaseConnector
from requests import exceptions
from winrm.exceptions import InvalidCredentialsError, WinRMTransportError
from winrm.protocol import Protocol

# Usage of the consts file is recommended
from microsoftsccm_consts import *


class MicrosoftsccmConnector(BaseConnector):

    def __init__(self):

        # Call the BaseConnectors init first
        super(MicrosoftsccmConnector, self).__init__()

        self._state = None

        # Configuration variables
        self._server_url = None
        self._username = None
        self._password = None
        self._verify_server_cert = False

    def _handle_test_connectivity(self, param):
        """ This function tests the connectivity of an asset with given credentials.

        :param param: (not used in this method)
        :return: status success/failure
        """

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        self.save_progress(MSSCCM_CONNECTING_ENDPOINT_MSG)
        # Execute power shell command
        status, _ = self._execute_ps_command(action_result, MSSCCM_PS_COMMAND.format(command="ls"))

        if phantom.is_fail(status):
            self.debug_print(action_result.get_message())
            self.save_progress(MSSCCM_TEST_CONNECTIVITY_FAIL)
            return action_result.get_status()

        # Return success
        self.save_progress(MSSCCM_TEST_CONNECTIVITY_PASS)
        return action_result.set_status(phantom.APP_SUCCESS)

    def _get_fips_enabled(self):
        try:
            from phantom_common.install_info import is_fips_enabled
        except ImportError:
            return False

        fips_enabled = is_fips_enabled()
        if fips_enabled:
            self.debug_print('FIPS is enabled')
        else:
            self.debug_print('FIPS is not enabled')
        return fips_enabled

    def _execute_ps_command(self, action_result, ps_command):
        """ This function is used to execute power shell command.

        :param action_result: object of ActionResult
        :param ps_command: power shell command
        :return: output of executed power shell command
        """

        resp_output = None
        server_cert_validation = 'ignore'
        transport = 'ntlm'

        if self._get_fips_enabled():
            transport = 'basic'

        if self._verify_server_cert:
            server_cert_validation = 'validate'

        protocol = Protocol(endpoint=MSSCCM_SERVER_URL.format(url=self._server_url), transport=transport,
                            username=self._username, password=self._password,
                            server_cert_validation=server_cert_validation)

        try:
            shell_id = protocol.open_shell()
        except InvalidCredentialsError as credentials_err:
            self.debug_print(MSSCCM_INVALID_CREDENTIAL_ERR, credentials_err)
            return action_result.set_status(phantom.APP_ERROR, MSSCCM_INVALID_CREDENTIAL_ERR,
                                            credentials_err), resp_output
        except exceptions.SSLError as ssl_err:
            self.debug_print(MSSCCM_ERR_BAD_HANDSHAKE, ssl_err)
            return action_result.set_status(phantom.APP_ERROR, MSSCCM_ERR_BAD_HANDSHAKE,
                                            ssl_err), resp_output
        except exceptions.ConnectionError as conn_err:
            self.debug_print(MSSCCM_ERR_SERVER_CONNECTION, conn_err)
            return action_result.set_status(phantom.APP_ERROR, MSSCCM_ERR_SERVER_CONNECTION,
                                            conn_err), resp_output
        except WinRMTransportError as transport_err:
            self.debug_print(MSSCCM_TRANSPORT_ERR, transport_err)
            return action_result.set_status(phantom.APP_ERROR, MSSCCM_TRANSPORT_ERR,
                                            transport_err), resp_output
        except Exception as e:
            self.debug_print(MSSCCM_EXCEPTION_OCCURRED, e)
            return action_result.set_status(phantom.APP_ERROR, MSSCCM_EXCEPTION_OCCURRED,
                                            e), resp_output

        try:
            command_id = protocol.run_command(shell_id, ps_command)
            resp_output, resp_err, status_code = protocol.get_command_output(shell_id, command_id)
            protocol.cleanup_command(shell_id, command_id)
            protocol.close_shell(shell_id)
        except Exception as err:
            self.debug_print(MSSCCM_EXCEPTION_OCCURRED, err)
            return action_result.set_status(phantom.APP_ERROR, MSSCCM_EXCEPTION_OCCURRED,
                                            err), resp_output

        if status_code:
            return action_result.set_status(phantom.APP_ERROR, MSSCCM_EXCEPTION_OCCURRED,
                                            resp_err), resp_output

        return action_result.set_status(phantom.APP_SUCCESS), resp_output

    def _handle_deploy_patch(self, param):
        """ This function is used to deploy software patches.

        :param param: dictionary of input parameters
        :return: status success/failure
        """

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        # Required values can be accessed directly
        software_patch_name = param[MSSCCM_PARAM_PATCH_NAME]
        device_group_name = param[MSSCCM_PARAM_DEVICE_GROUP_NAME]

        # Execute Command
        status, _ = self._execute_ps_command(action_result,
                                                    MSSCCM_DEPLOY_SOFTWARE_PATCHES.format(
                                                        name=software_patch_name,
                                                        device_group_name=device_group_name, q='\\"'))

        # Something went wrong
        if phantom.is_fail(status):
            self.debug_print(action_result.get_message())
            message = action_result.get_message()

            if "ItemNotFoundException" in message:
                message = "Software patch or Device group not found"

            if "ObjectIsNotDownloaded" in message:
                message = "Software patch is not downloaded on the SCCM server"

            action_result.set_status(phantom.APP_ERROR, status_message=message)
            return action_result.get_status()

        return action_result.set_status(phantom.APP_SUCCESS, "Patch deployed successfully")

    def _handle_list_patches(self, param):
        """ This function is used to list all software patches.

        :param param: dictionary of input parameters
        :return: status success/failure
        """

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        # Execute Command
        status, response = self._execute_ps_command(action_result, MSSCCM_GET_SOFTWARE_PATCHES.format(q='\\"'))

        # Something went wrong
        if phantom.is_fail(status):
            self.debug_print(action_result.get_message())
            return action_result.get_status()

        # Add data to action_result
        try:
            if response:
                response = json.loads(response)
                # Filter response to get only new alerts
                for item in response:
                    action_result.add_data(item)
        except Exception as e:
            self.debug_print(MSSCCM_JSON_FORMAT_ERROR)
            return action_result.set_status(phantom.APP_ERROR, MSSCCM_JSON_FORMAT_ERROR, e)

        # Update summary
        summary = action_result.update_summary({})
        summary['total_software_patches'] = action_result.get_data_size()

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_list_device_groups(self, param):
        """ This function is used to list all device groups.

        :param param: dictionary of input parameters
        :return: status success/failure
        """

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        # Execute Command
        status, response = self._execute_ps_command(action_result, MSSCCM_GET_DEVICE_GROUPS.format(q='\\"'))

        # Something went wrong
        if phantom.is_fail(status):
            self.debug_print(action_result.get_message())
            return action_result.get_status()

        # Add data to action_result
        try:
            if response:
                response = json.loads(response)
                # Filter response to get only new alerts
                for item in response:
                    action_result.add_data(item)
        except Exception as e:
            self.debug_print(MSSCCM_JSON_FORMAT_ERROR)
            return action_result.set_status(phantom.APP_ERROR, MSSCCM_JSON_FORMAT_ERROR, e)

        # Update summary
        summary = action_result.update_summary({})
        summary['total_device_groups'] = action_result.get_data_size()

        return action_result.set_status(phantom.APP_SUCCESS)

    def handle_action(self, param):
        """ This function gets current action identifier and calls member function of its own to handle the action.

        :param param: dictionary which contains information about the actions to be executed
        :return: status success/failure
        """

        # Dictionary mapping each action with its corresponding actions
        action_mapping = {
            'deploy_patch': self._handle_deploy_patch,
            'test_connectivity': self._handle_test_connectivity,
            'list_patches': self._handle_list_patches,
            'list_device_groups': self._handle_list_device_groups
        }

        action = self.get_action_identifier()
        action_execution_status = phantom.APP_SUCCESS

        if action in list(action_mapping.keys()):
            action_function = action_mapping[action]
            action_execution_status = action_function(param)

        return action_execution_status

    def initialize(self):

        # Load the state in initialize, use it to store data
        # that needs to be accessed across actions
        self._state = self.load_state()

        # Get the asset config
        config = self.get_config()

        # Required config parameter
        self._server_url = config[MSSCCM_CONFIG_SERVER_URL]
        self._username = config[MSSCCM_CONFIG_USERNAME]
        self._password = config[MSSCCM_CONFIG_PASSWORD]

        # Optional config parameter
        self._verify_server_cert = config.get(MSSCCM_CONFIG_VERIFY_SSL, False)

        return phantom.APP_SUCCESS

    def finalize(self):

        # Save the state, this data is saved accross actions and app upgrades
        self.save_state(self._state)
        return phantom.APP_SUCCESS


if __name__ == '__main__':

    import sys

    import pudb
    pudb.set_trace()

    if (len(sys.argv) < 2):
        print("No test json specified as input")
        sys.exit(0)

    with open(sys.argv[1]) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = MicrosoftsccmConnector()
        connector.print_progress_message = True
        ret_val = connector._handle_action(json.dumps(in_json), None)
        print(json.dumps(json.loads(ret_val), indent=4))

    sys.exit(0)
