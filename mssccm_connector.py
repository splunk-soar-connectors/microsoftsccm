# --
# File: mssccm_connector.py
#
# Copyright (c) Phantom Cyber Corporation, 2016
#
# This unpublished material is proprietary to Phantom Cyber.
# All rights reserved. The methods and
# techniques described herein are considered trade secrets
# and/or confidential. Reproduction or distribution, in whole
# or in part, is forbidden except by express written permission
# of Phantom Cyber Corporation.
#
# --

# Phantom imports
import phantom.app as phantom
import re
from phantom.base_connector import BaseConnector
from phantom.action_result import ActionResult

# THIS Connector imports
from mssccm_consts import *

import simplejson as json
import socket
import ssl
import netifaces
import copy
from parse import parse


class MsSccmConnector(BaseConnector):

    # actions supported by this script
    ACTION_ID_GET_AVAILABLE_UPDATES = "list_updates"
    ACTION_ID_INSTALL_AVAILABLE_UPDATES = "install_updates"

    def __init__(self):

        # Call the BaseConnectors init first
        super(MsSccmConnector, self).__init__()

        self._ip = None
        self._port = None
        self._sock = None
        self._installer_used = None

    def _fill_action_result(self, sout, serr, cmd_ret_code, message, action_result, append_output=False):

        if (cmd_ret_code != 0):

            # Command failed
            action_result.set_status(phantom.APP_ERROR, message)
            # The message should contain all the info
            action_result.append_to_message(sout.strip('\r\n '))
            action_result.append_to_message(serr.strip('\r\n '))
        else:
            # Command succeeded
            action_result.set_status(phantom.APP_SUCCESS, message)

        return phantom.APP_SUCCESS

    def _install_service(self, username, password, remote_machine, action_result):

        if (not phantom.is_ip(remote_machine) and not phantom.is_hostname(remote_machine)):
            return (action_result.set_status(phantom.APP_ERROR, MSSCCM_ERR_INVALID_MACHINE_NAME_IP), None)

        # Create a list of parameters to pass to the installer, deepcopy since we'll be adding to the list
        # and don't want SVC_INST_PARAMS to change
        installer_params = copy.deepcopy(SVC_INST_PARAMS)

        # Parse the ip and port that the agent should connect to
        installer_params.append(SVC_PARAMS.format(ip=self._ip, port=self._port))

        # username/password and ip address
        installer_params.extend(['-U', '{0}%{1}'.format(username, password), '//{0}'.format(remote_machine)])

        # First try the win7 and above command
        self._installer_used = WIN7_INSTALLER
        local_command = [self._installer_used]

        # Rest of the params
        local_command.extend(installer_params)

        self.save_progress(phantom.APP_PROG_CONNECTING_TO_ELLIPSES, remote_machine)

        self.debug_print("Trying the Win7 Installer ")

        # self.debug_print("win7 local command", local_command)
        sout, serr, cmd_ret_code = phantom.run_ext_command(local_command)

        # self.debug_print("sout: {0}\n, serr: {1}\n, cmd_ret_code: {2}".format(sout, serr, cmd_ret_code))

        if (cmd_ret_code != 0):
            # Try xp
            self._installer_used = WINXP_INSTALLER
            local_command = [self._installer_used]

            # Rest of the params
            local_command.extend(installer_params)

            # TODO: remove this from the installer command required for xp
            local_command.append(' ')

            self.debug_print("Trying the XP Installer ")
            # self.debug_print("xp local command", local_command)
            sout, serr, cmd_ret_code = phantom.run_ext_command(local_command)
            # self.debug_print("sout: {0}\n, serr: {1}\n, cmd_ret_code: {2}".format(sout, serr, cmd_ret_code))

        if (cmd_ret_code != 0):
            self._fill_action_result(sout, serr, cmd_ret_code,
                    MSSCCM_ERR_SERVICE_INSTALLATION,
                    action_result)
            return (phantom.APP_ERROR, None)

        return (phantom.APP_SUCCESS, self._installer_used)

    def _uninstall_known_service(self, username, password, remote_machine, installer_used, action_result=None):

        local_command = "{0} {1} -U {2}%{3} //{4} ".format(
                installer_used,
                SVC_UNINST_PARAMS,
                username,
                password,
                remote_machine)

        self.save_progress(MSSCCM_MSG_UNINSTALLING_SERVICE)
        self.save_progress(phantom.APP_PROG_CONNECTING_TO_ELLIPSES, remote_machine)

        sout, serr, cmd_ret_code = phantom.run_ext_command(local_command)

        if (cmd_ret_code != 0):
            if (action_result):
                self._fill_action_result(sout, serr, cmd_ret_code,
                        MSSCCM_ERR_SERVICE_UNINSTALLATION,
                        action_result)
            return phantom.APP_ERROR

        return phantom.APP_SUCCESS

    def _send_command(self, curr_machine, command, action_result):

        self.save_progress(MSSCCM_MSG_PROG_SENDING_COMMAND_TO, machine=curr_machine)
        self.debug_print('command', command)

        # The socket should have already been created
        if (self._sock is None):
            return (action_result.set_status(phantom.APP_ERROR, MSSCCM_ERR_SOCKET_NOT_CONNECTED), None)

        try:
            self.save_progress(MSSCCM_LISTENING_FOR_CONNECTIONS, ip=self._ip, port=self._port)
            self._sock.settimeout(LISTEN_TIMEOUT)
            self._sock.listen(1)
            newsocket, fromaddr = self._sock.accept()
            self.save_progress(MSSCCM_ACCEPTED_CONNECTION_FROM, ip=fromaddr[0], port=fromaddr[1])
            sslsoc = ssl.wrap_socket(newsocket, server_side=True, certfile=CERT_PATH, keyfile=CERT_KEY_PATH, ssl_version=ssl.PROTOCOL_SSLv23)
            self.debug_print(MSSCCM_SSL_CONNECTION_ESTABLISHED)
        except Exception as e:
            self._sock.close()
            return (action_result.set_status(phantom.APP_ERROR, MSSCCM_ERR_SOCKET_CONNECT, e), None)

        # Now keep recving till we se a \r\n
        response = ''

        try:
            self.save_progress(MSSCCM_COMMUNICATING_CHANNEL)
            sslsoc.write(json.dumps(command) + '\n')
            response = ''
            while True:
                data = sslsoc.recv(RECV_BUF_SIZE)
                if (not data):
                    break
                if (data):
                    response += data
                    if (data.find('\n') != -1):
                        break

        except Exception as e:
            return (action_result.set_status(phantom.APP_ERROR, MSSCCM_ERR_SOCKET_DATA, e), None)

        self.debug_print('response', response)

        if (len(response)):
            response = json.loads(unicode(response, errors='replace'))
        else:
            response = []
            action_result.append_to_message(MSSCCM_ERR_NO_DATA)

        sslsoc.close()
        self._sock.close()

        return (phantom.APP_SUCCESS, response)

    def _get_ip_to_bind(self, action_result):

        # get the app config
        app_config = self.get_app_config()
        interface = app_config.get("interface")

        if (interface is None):
            interface = DEFAULT_INTERFACE_NAME

        try:
            # get the ip of an interface
            addrs = netifaces.ifaddresses(interface)
            addr = addrs[netifaces.AF_INET]
        except Exception as e:
            action_result.set_status(phantom.APP_ERROR, "Failed to get IP for the interface", e, interface=interface)
            return None

        # pick up the first ip address
        if (len(addr) == 0):
            action_result.set_status(phantom.APP_ERROR, "IP not found", interface=interface)
            return None

        ip = addr[0]['addr']

        return ip

    def execute_script(self, script, action_result, username, password, endpoint):
        script_code = script
        # init the command dict, with the parameters
        command = dict()
        command[phantom.APP_JSON_PARAMETERS] = {WINAGENT_CMD_PS_SCRIPT_CODE: script_code}
        command[phantom.APP_JSON_ACTION_IDENTIFIER] = WINAGENT_CMD_RUN_PS_SCRIPT

        # Bind on an ip/port
        ret_val = self._bind(action_result)
        if (phantom.is_fail(ret_val)):
            return phantom.APP_ERROR, "Error trying to connect to the endpoint"

        # Install the service
        ret_val, installer_used = self._install_service(username, password, endpoint, action_result)

        if (phantom.is_fail(ret_val)):
            return phantom.APP_ERROR, "Error trying to install service on the endpoint"

        ret_val, response = self._send_command(endpoint, command, action_result)
        self._uninstall_known_service(username, password, endpoint, installer_used)

        if (phantom.is_success(ret_val)):
            return phantom.APP_SUCCESS, response
        return phantom.APP_ERROR, "Error trying to execute script on the endpoint"

    def get_names(self, response_data):
        clean_data = []
        name_data = response_data.get("data", [None])[0]
        for i in (" ", "-", "\\"):
            name_data = name_data.replace(i, "")
        name_data = name_data.split("\n")
        for name in name_data:
            if not name:
                continue
            clean_data.append(str(name))
        if clean_data:
            print clean_data
            return phantom.APP_SUCCESS, clean_data[1:-1]
        return phantom.APP_ERROR, []

    def get_comp_names(self, action_result, username, password, endpoint):
        script = """
        [Environment]::UserName
        """
        ret_val, response = self.execute_script(script, action_result, username, password, endpoint)
        if (phantom.is_fail(ret_val)):
            return phantom.APP_ERROR, []
        ret_val, comp_names = self.get_names(response)
        if (phantom.is_success(ret_val)):
            return phantom.APP_SUCCESS, comp_names
        return phantom.APP_ERROR, []

    def process_update_data(self, update_data, action_result):
        update_string_data = update_data.get("data", [None])[0]

        if len(update_string_data) == 0:
            return phantom.APP_ERROR, "There is no update data"
        kb_data = (re.findall(re.compile("KB[0-9]+"), update_string_data))

        if len(kb_data) == 0:
            return phantom.APP_ERROR, "The update data is void of KB IDs"

        update_dict = {}
        kb_list_count = [None, ]

        for entry in update_string_data.replace("  ", "").split("\n"):
            if ":" not in entry:
                continue
            temp_split = entry.split(":")
            if len(temp_split) == 1:
                update_dict[temp_split[0]] = ""
            else:
                update_dict[temp_split[0]] = temp_split[1]
            if "IsMandatory".lower() in temp_split[0].lower():
                if "True" in temp_split[1]:
                    update_dict[temp_split[0]] = "Mandatory"
                else:
                    update_dict[temp_split[0]] = "Optional"
            else:
                update_dict["IsMandatory"] = "NA"

            if update_dict.get("KB") in kb_list_count:
                continue
            kb_list_count.append(update_dict.get("KB"))
            action_result.add_data(copy.deepcopy(update_dict))
        return phantom.APP_SUCCESS, "Successfully extracted the KBs"

    def get_updates_handle(self, param):

        self.save_progress("Preparing for fetching update list...")
        config = self.get_config()
        action_result = self.add_action_result(ActionResult(param))
        username = config[phantom.APP_JSON_USERNAME]
        password = config[phantom.APP_JSON_PASSWORD]
        endpoint = param[phantom.APP_JSON_IP_HOSTNAME]

        get_update = get_update_definition + "\n\n\n" + "Get-WUList"
        ret_val, response = self.execute_script(get_update, action_result, username, password, endpoint)

        if (phantom.is_fail(ret_val)):
            return action_result.set_status(phantom.APP_ERROR, response)

        ret_val = self.process_update_data(response, action_result)

        if (phantom.is_fail(ret_val)):
            return action_result.set_status(phantom.APP_ERROR, "Error when trying to process update data please check the connection")

        return action_result.set_status(phantom.APP_SUCCESS, "List of all updates acquired")

    def perform_updates_handle(self, param):

        self.save_progress("Preparing for installing updates...")
        config = self.get_config()
        action_result = self.add_action_result(ActionResult(param))
        username = config[phantom.APP_JSON_USERNAME]
        password = config[phantom.APP_JSON_PASSWORD]
        endpoint = param[phantom.APP_JSON_IP_HOSTNAME]

        get_update = "$KBList = "
        kbid_list = param.get("list_of_updates", None)

        if not kbid_list:
            return action_result.set_status(phantom.APP_ERROR, "Update list empty")

        for kbid in kbid_list.split(","):
            get_update += "'{0}', ".format(kbid.strip())

        get_update = get_update[:-2]
        perform_update = get_update + "\n\n\n" + perform_update_definition + UPDATE_PERFORM_COMMAND

        ret_val, response = self.execute_script(perform_update, action_result, username, password, endpoint)

        if (phantom.is_fail(ret_val)):
            return action_result.set_status(phantom.APP_ERROR, response)
        resp_data = {}
        for i in response["data"].strip().replace("  ", "").split("\n"):
            if ":" in i:
                resp_data[i.split(":")[0]] = i.split(":")[-1]
        action_result.add_data(copy.deepcopy(resp_data))
        return action_result.set_status(phantom.APP_SUCCESS, "Updates Triggered")

    def _bind(self, action_result):

        # first get the ip
        ip = self._get_ip_to_bind(action_result)

        if (ip is None):
            return action_result.get_status()

        self._ip = ip

        # try binding on a port
        self._port = None

        min_port = None
        max_port = None

        app_config = self.get_app_config()
        port_range = app_config.get(MSSCCM_JSON_PORT_RANGE)

        if (port_range is None):
            min_port = DEFAULT_MIN_PORT
            max_port = DEFAULT_MAX_PORT
        else:
            try:
                port_parsed = parse("{min_port}-{max_port}", port_range)
                min_port = int(port_parsed['min_port'])
                max_port = int(port_parsed['max_port'])
            except Exception as e:
                return action_result.set_status(phantom.APP_ERROR, MSSCCM_ERR_PARSE_PORT_RANGE, e)

        self._sock = socket.socket()
        for curr_port in xrange(min_port, max_port):

            try:
                self._sock.bind((ip, curr_port))
            except Exception as e:
                continue

            self._port = curr_port
            break

        if (self._port is None):
            return action_result.set_status(phantom.APP_ERROR, MSSCCM_ERR_FAILED_TO_GET_FREE_PORT)

        return phantom.APP_SUCCESS

    def handle_action(self, param):

        action = self.get_action_identifier()
        if (action == self.ACTION_ID_GET_AVAILABLE_UPDATES):
            self.get_updates_handle(param)

        elif (action == self.ACTION_ID_INSTALL_AVAILABLE_UPDATES):
            self.perform_updates_handle(param)

        return self.get_status()

if __name__ == '__main__':

    import sys
    with open(sys.argv[1]) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=' ' * 4))

        connector = MsSccmConnector()
        connector.print_progress_message = True
        result = connector._handle_action(json.dumps(in_json), None)

        print result

    exit(0)
