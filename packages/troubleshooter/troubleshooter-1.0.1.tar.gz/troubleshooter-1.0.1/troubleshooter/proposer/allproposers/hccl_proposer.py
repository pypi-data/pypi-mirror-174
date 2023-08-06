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
"""The hccl proposer."""
import re
import traceback
from troubleshooter.proposer.allproposers.base_proposer import Proposer
from troubleshooter.proposer.knowledge_base.hccl_exp_lib import hccl_experience_list_cn


class HcclProposer(Proposer):
    """The hccl proposer."""

    def __init__(self):
        super().__init__()
        self.expert_experience_library = hccl_experience_list_cn

    def analyze(self, exc_type, exc_value, traceback_obj):
        """

        Args:
            exc_type:
            exc_value:
            traceback_obj:

        Returns:

        """
        error_message = str(exc_value) if exc_value is not None else traceback.format_exc()
        for expert_experience in self.expert_experience_library:
            match_count = 0
            key_log_info = expert_experience['Key Log Information']
            key_python_stack_info = expert_experience['Key Python Stack Information']
            key_cpp_stack_info = expert_experience['Key C++ Stack Information']
            if key_log_info and re.search(key_log_info, error_message):
                match_count = match_count + 1
            if key_python_stack_info and re.search(key_python_stack_info, error_message):
                match_count = match_count + 1
            if key_cpp_stack_info and re.search(key_cpp_stack_info, error_message):
                match_count = match_count + 1
            if match_count >= 2:
                return expert_experience
        return None
