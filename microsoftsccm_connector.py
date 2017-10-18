# --
# File: microsoftsccm_connector.py
#
# Copyright (c) Phantom Cyber Corporation, 2017
#
# This unpublished material is proprietary to Phantom Cyber.
# All rights reserved. The methods and
# techniques described herein are considered trade secrets
# and/or confidential. Reproduction or distribution, in whole
# or in part, is forbidden except by express written permission
# of Phantom Cyber Corporation.
#
# --

# Standard library imports
import json
from winrm.protocol import Protocol
from winrm.exceptions import InvalidCredentialsError
from requests import exceptions

# Phantom App imports
import phantom.app as phantom
from phantom.base_connector import BaseConnector
from phantom.action_result import ActionResult

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
        status, response = self._execute_ps_command(action_result, MSSCCM_PS_COMMAND.format(command="ls"))

        if phantom.is_fail(status):
            self.debug_print(action_result.get_message())
            self.save_progress("{0} Error: {1}".format(MSSCCM_TEST_CONNECTIVITY_FAIL, action_result.get_message()))
            return action_result.get_status()

        # Return success
        self.save_progress(MSSCCM_TEST_CONNECTIVITY_PASS)
        return action_result.set_status(phantom.APP_SUCCESS)

    def _execute_ps_command(self, action_result, ps_command):
        """ This function is used to execute power shell command.

        :param action_result: object of ActionResult
        :param ps_command: power shell command
        :return: output of executed power shell command
        """

        resp_output = None

        if self._verify_server_cert is False:
            protocol = Protocol(endpoint=MSSCCM_SERVER_URL.format(url=self._server_url), transport='ntlm',
                                username=self._username, password=self._password,
                                server_cert_validation='ignore')
        else:
            protocol = Protocol(endpoint=MSSCCM_SERVER_URL.format(url=self._server_url), transport='ntlm',
                                username=self._username, password=self._password,
                                server_cert_validation='validate')

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

    def _handle_install_updates(self, param):
        """ This function is used to install software updates.

        :param param: dictionary of input parameters
        :return: status success/failure
        """

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        # Required values can be accessed directly
        software_update_name = param[MSSCCM_PARAM_SF_UPDATE_NAME]
        collection_name = param[MSSCCM_PARAM_COLLECTION_NAME]

        # Execute Command
        status, response = self._execute_ps_command(action_result,
                                                    MSSCCM_INSTALL_SOFTWARE_UPDATES.format(
                                                        name=software_update_name,
                                                        collection_name=collection_name, q='\\"'))

        # Something went wrong
        if phantom.is_fail(status):
            self.debug_print(action_result.get_message())
            return action_result.get_status()

        return action_result.set_status(phantom.APP_SUCCESS, "Update installed successfully")

    def _handle_list_updates(self, param):
        """ This function is used to list all software updates.

        :param param: dictionary of input parameters
        :return: status success/failure
        """

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        # Execute Command
        status, response = self._execute_ps_command(action_result, MSSCCM_GET_SOFTWARE_UPDATES.format(q='\\"'))

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
        summary['total_software_updates'] = action_result.get_data_size()

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_list_collections(self, param):
        """ This function is used to list all device collection.

        :param param: dictionary of input parameters
        :return: status success/failure
        """

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        # Execute Command
        status, response = self._execute_ps_command(action_result, MSSCCM_GET_DEVICE_COLLECTION.format(q='\\"'))

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
        summary['total_collections'] = action_result.get_data_size()

        return action_result.set_status(phantom.APP_SUCCESS)

    def handle_action(self, param):
        """ This function gets current action identifier and calls member function of its own to handle the action.

        :param param: dictionary which contains information about the actions to be executed
        :return: status success/failure
        """

        # Dictionary mapping each action with its corresponding actions
        action_mapping = {'install_updates': self._handle_install_updates,
                          'test_connectivity': self._handle_test_connectivity,
                          'list_updates': self._handle_list_updates,
                          'list_collections': self._handle_list_collections}

        action = self.get_action_identifier()
        action_execution_status = phantom.APP_SUCCESS

        if action in action_mapping.keys():
            action_function = action_mapping[action]
            action_execution_status = action_function(param)

        return action_execution_status

    def initialize(self):

        # Load the state in initialize, use it to store data
        # that needs to be accessed across actions
        self._state = self.load_state()

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
        print "No test json specified as input"
        exit(0)

    with open(sys.argv[1]) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = MicrosoftsccmConnector()
        connector.print_progress_message = True
        ret_val = connector._handle_action(json.dumps(in_json), None)
        print (json.dumps(json.loads(ret_val), indent=4))

    exit(0)
