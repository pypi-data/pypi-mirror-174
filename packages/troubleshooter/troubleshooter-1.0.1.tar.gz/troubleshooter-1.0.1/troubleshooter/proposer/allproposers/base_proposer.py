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

"""The proposer base class."""
from abc import ABC, abstractmethod
import re

REQUIRE_A_COND = 0
REQUIRE_MULTIPLE_COND = 1

class Proposer(ABC):
    # pylint: disable=W0612,W0613
    """The proposer base class."""

    @abstractmethod
    def analyze(self, exc_type, exc_value, traceback_obj):
        """analysis and get proposal."""
        return None

    def compare_key_words(self, err_msg, key_word):
        """Find out whether the key log information is in the exception or not."""
        return key_word and re.search(key_word, err_msg)

    def base_case_analyze(self, error_message, experience_list):
        for experience in experience_list:
            key_words = experience['Key Log Information']
            python_stack_info = experience['Key Python Stack Information']
            cplusplus_stack_info = experience['Key C++ Stack Information']
            if self.compare_key_words(error_message, key_words) and \
                    self.compare_stack_infos(error_message, python_stack_info, cplusplus_stack_info):
                return experience
        return None

    def base_scene_analyze(self, error_message, experience_list, condition_flag=0):
        """
        Error analysis execution
        Args:
            error_message:
            experience_list:
            condition_flag:

        Returns:

        """

        result = None
        key_matching = False
        path_matching = False

        for experience in experience_list:
            code_paths = experience['Code Path']
            code_paths = code_paths.split(";")
            key_words = experience['Key Log Information']
            for code_path in code_paths:
                # analyze with code path where throw exception
                if code_path and re.search(code_path, error_message):
                    path_matching = True
                    break

            if key_words and re.search(key_words, error_message):
                key_matching = True

            if condition_flag == REQUIRE_A_COND and (key_matching or path_matching):
                result = experience

            if condition_flag == REQUIRE_MULTIPLE_COND and key_matching and path_matching:
                result = experience

        return result

    def compare_stack_infos(self, err_msg, python_stack, cplusplus_stack):
        """Compare python stack and c++ stack of the experience with the error message's """
        if python_stack and not re.search(python_stack, err_msg):
            # print("compare python stack failed.")
            return False
        if cplusplus_stack and not re.search(cplusplus_stack, err_msg):
            # print("compare c++ stack failed.")
            return False
        return True
