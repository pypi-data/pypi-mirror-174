# Copyright 2022 Tiger Miao
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""build information"""
import os
import mindspore
from mindspore import context

OUT_OF_INDEX = -1
CPP_FUN_INDEX_EXTEND = 1


def _get_ms_information(result):
    ms_version = "r" + mindspore.__version__[:3]
    result["mindspore_version"] = ms_version
    mode = context.get_context("mode")
    device = context.get_context("device_target")
    if mode == 0:
        result["mindspore_mode"] = "Graph Mode"
    else:
        result["mindspore_mode"] = "PyNative Mode"
    result["Device Type"] = device
    return result


def get_errmsg_dict(exc_type, exc_value):
    error_type = str(exc_type.__name__)
    org_err_msg = str(exc_value)
    cpp_fun_msg = None
    construct_stack_msg = None
    abstract_inner_msg = None
    construct_stack_in_file_msg = None
    err_msg = org_err_msg
    construct_stack_index = org_err_msg.find("The function call stack")
    construct_stack_in_file_index = org_err_msg.find("# In file /")
    cpp_fun_index = -1
    abstract_inner_msg_index = org_err_msg.find("The abstract type of the return value")

    cpp_fun_flag_index = org_err_msg.find("]")
    if cpp_fun_flag_index != OUT_OF_INDEX:
        cpp_flag_index = org_err_msg[0:cpp_fun_flag_index].find(".cc:")
        if cpp_flag_index != OUT_OF_INDEX:
            cpp_fun_index = cpp_fun_flag_index + CPP_FUN_INDEX_EXTEND
    if construct_stack_index != OUT_OF_INDEX and cpp_fun_index != OUT_OF_INDEX:
        cpp_fun_msg = org_err_msg[0:cpp_fun_index - CPP_FUN_INDEX_EXTEND]
        construct_stack_msg = org_err_msg[construct_stack_index:len(org_err_msg)]
        if abstract_inner_msg_index != OUT_OF_INDEX:
            err_msg = org_err_msg[cpp_fun_index:abstract_inner_msg_index]
            abstract_inner_msg = org_err_msg[abstract_inner_msg_index:construct_stack_index]
        else:
            err_msg = org_err_msg[cpp_fun_index:construct_stack_index]
    elif construct_stack_index == OUT_OF_INDEX and cpp_fun_index != OUT_OF_INDEX:
        if construct_stack_in_file_index != OUT_OF_INDEX:
            cpp_fun_msg = org_err_msg[0:cpp_fun_index - CPP_FUN_INDEX_EXTEND]
            err_msg = org_err_msg[cpp_fun_index:construct_stack_in_file_index]
            construct_stack_in_file_msg = org_err_msg[construct_stack_in_file_index:len(org_err_msg)]
        else:
            cpp_fun_msg = org_err_msg[0:cpp_fun_index - CPP_FUN_INDEX_EXTEND]
            err_msg = org_err_msg[cpp_fun_index:len(org_err_msg)]

    err_msg = error_type + ":" + err_msg
    errmsg_dict = {"cpp_fun_msg": cpp_fun_msg, "construct_stack_msg": construct_stack_msg, "err_msg": err_msg,
                   "abstract_inner_msg": abstract_inner_msg,
                   "construct_stack_in_file_msg": construct_stack_in_file_msg}
    return errmsg_dict


def base_information_build(result):
    ret_result = _get_ms_information(result)
    device_type = ret_result.get("Device Type");
    if device_type is None or len(device_type) == 0:
        ret_result["Device Type"] = "Unknow"
    return ret_result


def log_obj_bulid(log_path):
    log_name = "log"
    log_message = ""
    for root, files in os.walk(log_path):
        for name in files:
            log_file = os.path.join(root, name)
            print("log file:", log_file)
            if name == log_name and os.path.isfile(log_file):
                log_reader = open(log_file, 'r', buffering=2000000)
                log_message = log_reader.read()
    return log_message
