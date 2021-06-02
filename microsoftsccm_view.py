# --
# File: microsoftsccm_view.py
# Copyright (c) 2017-2021 Splunk Inc.
# SPLUNK CONFIDENTIAL - Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.
#
#
# --

#


def _get_ctx_result(provides, result):
    """ Function to get ctx result.

    :param provides: action name
    :param result: result
    :return: context response
    """

    ctx_result = {}

    param = result.get_param()
    summary = result.get_summary()
    data = result.get_data()

    ctx_result['param'] = param
    if summary:
        ctx_result['summary'] = summary

    if not data:
        ctx_result['data'] = {}
        return ctx_result

    ctx_result['action'] = provides
    ctx_result['data'] = parsed_data(provides, data)

    return ctx_result


def parsed_data(provides, data):
    """ Function that parse data.

    :param provides: action name
    :param data: response data
    :return: parsed response
    """

    boolean_dict = {"True": "Yes", "False": "No"}
    if provides == "list patches":
        for item in data:
            try:
                item["IsDeployed"] = boolean_dict[item["IsDeployed"]]
                item["IsSuperseded"] = boolean_dict[item["IsSuperseded"]]
                item["IsExpired"] = boolean_dict[item["IsExpired"]]
            except ValueError:
                pass

    return data


def display_view(provides, all_app_runs, context):
    """ Function that display flows.

    :param provides: action name
    :param all_app_runs: all_app_runs
    :param context: context
    :return: html page name
    """
    context['results'] = results = []
    for summary, action_results in all_app_runs:
        for result in action_results:
            ctx_result = _get_ctx_result(provides, result)
            if not ctx_result:
                continue
            results.append(ctx_result)

    return_page = "microsoftsccm_patches.html"

    if provides == "list device groups":
        return_page = "microsoftsccm_device_groups.html"

    return return_page
