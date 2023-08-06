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
"""Tracker"""
import os
from pysnooper.tracer import Tracer
from pysnooper.tracer import get_path_and_source_from_frame
from troubleshooter import log as logger

_NO_RESULT = -1
_FRAMEWORK_MS = 1


class Tracker(Tracer):
    """
    Framework Code Execution Tracking
    Args:
        framework (bool): Framework type
        filter (dict): Tracking filtering
        *args: Tracer args
        **kwargs: Tracer args
    """

    def __init__(self, level=1, depth=5, event_list=None, framework=1, max_variable_length=150, **kwargs):
        super(Tracker, self).__init__(depth=depth, max_variable_length=max_variable_length, **kwargs)
        self.ms_func_blacklist = {"deco": ["ops/primitive.py"], "__init__": ["ops/primitive.py", "common/tensor.py"],
                                  "__new__": ["common/parameter.py"], "__setattr__": ["nn/cell.py"],
                                  "__getattr__": ["nn/cell.py"]}
        self.func_whitelist = []
        self.path_whitelist = []
        self.framework = framework
        self.level = level
        self.event_list = event_list or []
        self.root_file = ""
        self.root_path = ""

        if self.event_list and 'call' in self.event_list and 'return' not in self.event_list:
            self.event_list.append('return')

        if self.level == 2:
            blacklist = {"__setattr__": "nn/cell.py", "__getattr__": "nn/cell.py"}
            self.ms_func_blacklist.update(blacklist)

        #if tracking_filter:
        #    self.func_whitelist += tracking_filter.get('func_whitelist') or []
        #    self.path_whitelist += tracking_filter.get('path_whitelist') or []
        #    self.ms_func_blacklist.update(tracking_filter.get('ms_func_blacklist') or [])

    def _frame_filter(self, frame, event):
        if self.framework == _FRAMEWORK_MS:
            return self._frame_filter_ms(frame, event)
        return True

    def _frame_filter_ms(self, frame, event):
        """
        Filter the frame information of
        Args:
            frame: The python frame
            event: Reserved Fields
            arg: Reserved Fields

        Returns (bool): frame information
        """
        result = True
        # line_no = frame.f_lineno
        func_name = frame.f_code.co_name
        source_path = get_path_and_source_from_frame(frame)
        source_path = source_path if not self.normalize else os.path.basename(source_path)

        if self.root_file == "":
            self.root_file = source_path[0]
            self.root_func = func_name
            self.root_path = os.path.dirname(self.root_file)
            logger.info("the root_file is {}".format(self.root_file))
            logger.info("the root_func is {}".format(self.root_func))
            logger.info("the root_path is {}".format(self.root_path))
            return result

        # for windows path.
        # if self.root_file.rfind(".\\") == 0:
        #    self.root_file = self.root_file[2:]

        if self.level == 1 and (func_name not in ["construct", "_run_op"]):
            return False

        logger.info("the path_name is {}".format(source_path[0]))
        logger.info("the func_name is {}".format(func_name))

        if self.level == 2 and source_path[0].find("site-packages/mindspore") == _NO_RESULT and \
                source_path[0].find(self.root_path) == _NO_RESULT:
            return False

        if self.event_list and event not in self.event_list:
            return False

        # ignore the mindspore backlist function
        ignore_path_list = self.ms_func_blacklist.get(func_name)
        if ignore_path_list:
            for ignore_path in ignore_path_list:
                if source_path[0].find(ignore_path) != _NO_RESULT:
                    return False

        return result

    def trace(self, frame, event, arg):
        if not self._frame_filter(frame, event):
            return None
        return super(Tracker, self).trace(frame, event, arg)
