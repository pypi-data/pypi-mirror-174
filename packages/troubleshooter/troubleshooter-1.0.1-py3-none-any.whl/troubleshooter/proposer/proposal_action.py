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

"""The Proposal Action."""
import sys
import traceback
import functools

from troubleshooter.common.information_build import base_information_build
from troubleshooter.common.format_output import print_result
from troubleshooter.proposer.proposer_factory import ProposerFactory
from troubleshooter.proposer.allproposers import proposer_list
from troubleshooter.common.format_output import print_format_exception
from troubleshooter.common.util import get_ms_log_path


class ProposalAction:
    """Get the proposals from multiple different proposers."""

    def __init__(self, level=None, print_org_exception=False):
        self.print_org_exception = print_org_exception
        self.proposer_list = proposer_list
        self.level = level
        self.ms_log_path = get_ms_log_path()
        # self.options = {"level": self.level, "ms_log_path": self.ms_log_path}

    def __call__(self, func):
        @functools.wraps(func)
        def proposal_wrapper(*args, **kw):
            try:
                return func(*args, **kw)
            except Exception as e:
                self.run()
        return proposal_wrapper

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback_obj):
        if exc_type is None or exc_value is None:
            return True
        if self.print_org_exception:
            traceback.print_exc()
        else:
            print_format_exception(exc_type, exc_value, exc_traceback_obj)
            self.run_proposers(exc_type, exc_value, exc_traceback_obj)
        return True

    def run(self):
        exc_type, exc_value, exc_traceback_obj = sys.exc_info()
        if self.print_org_exception:
            traceback.print_exc()
        else:
            print_format_exception(exc_type, exc_value, exc_traceback_obj)
        self.run_proposers(exc_type, exc_value, exc_traceback_obj)

    def run_proposers(self, exc_type, exc_value, traceback_obj):
        """
        Run proposers.
        Args:
            options (dict): options for proposal.
        Examples:
            :param traceback_obj:
            :param exc_value:
            :param exc_type:
        """
        for proposer in self.proposer_list:
            proposer = ProposerFactory.instance().get_proposer(proposer)
            if proposer is None:
                continue
            # Write the result of proposals.
            expert_experience_result = proposer.analyze(exc_type, exc_value, traceback_obj)
            if expert_experience_result:
                break

        if expert_experience_result is None:  # default
            proposer = ProposerFactory.instance().get_proposer("default")
            expert_experience_result = proposer.analyze(exc_type, exc_value, traceback_obj)

        expert_experience_result = base_information_build(expert_experience_result)
        print_result(expert_experience_result)
