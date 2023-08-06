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

hccl_experience_list_cn = [
    {"Fault Name": "hccl初始化故障", "Key Log Information": "ranktable is invalid",
     "Key Python Stack Information": "init_hccl()", "Key C++ Stack Information": "hccl_adapter.cc",
     "Fault Cause": "1. rank table文件内容可能不正确; 2.训练脚本中环境变量DEVICE_ID和RANK_ID可能与rank table文件配置的不一致",
     "Modification Suggestion": "1. 使用models/utils/hccl_tools重新生成rank table文件; 2.检查训练脚本，保证与rank table文件配置一致",
     "Fault Case": "1. 分布式并行训练基础样例: "
                   "https://www.mindspore.cn/tutorials/experts/zh-CN/r1.8/parallel/train_ascend.html "
                   "2. 生成hccl 配置文件: "
                   "https://gitee.com/mindspore/models/tree/master/utils/hccl_tools "
                   ""},
    {"Fault Name": "hccl p2p建链超时故障", "Key Log Information": "connected p2p timeout", "Key Python Stack Information": "",
     "Key C++ Stack Information": "load task fail",
     "Fault Cause": "1. ",
     "Modification Suggestion": "1. 查询rank table信息，比较设置的卡数与训练脚本启动的进程的数量是否匹配",
     "Fault Case": ""},
    {"Fault Name": "hccl socket建链超时故障", "Key Log Information": "socket times out",
     "Key Python Stack Information": "",
     "Key C++ Stack Information": "",
     "Fault Cause": "网络编译阶段，某卡编译速度慢或报错终止，其他卡与其通信超时报错。",
     "Modification Suggestion": "1. 对比多卡训练日志中状态信息，检查编译阶段哪个卡的状态与其他卡不同步。",
     "Fault Case": "1. mindspore状态信息定位错误节点："
                   "https://bbs.huaweicloud.com/forum/thread-180967-1-1.html "
                   "2. 分布式并行训练基础样例: "
                   "https://www.mindspore.cn/tutorials/experts/zh-CN/r1.8/parallel/train_ascend.html"},
    {"Fault Name": "hccl notify wait超时故障",
     "Key Log Information": "Notify wait execute failed",
     "Key Python Stack Information": "",
     "Key C++ Stack Information": "Launch graph failed",
     "Fault Cause": "网络执行阶段，某卡执行报错终止，其他卡出现notify wait timeout报错。 ",
     "Modification Suggestion": "1. 对比多卡训练日志，检查执行阶段哪个卡的进程被误杀",
     "Fault Case":  "1.mindspore状态信息定位错误节点： "
                    "https://bbs.huaweicloud.com/forum/thread-180967-1-1.html "
                    "2. 分布式并行训练基础样例: "
                    "https://www.mindspore.cn/tutorials/experts/zh-CN/r1.8/parallel/train_ascend.html"},
    {"Fault Name": "hccl notify wait超时故障",
     "Key Log Information": "the Notify register times out",
     "Key Python Stack Information": "",
     "Key C++ Stack Information": "Launch graph failed",
     "Fault Cause": "网络执行阶段，某卡执行报错终止，其他卡出现notify wait execute failed报错。 ",
     "Modification Suggestion": "1. 对比多卡训练日志，检查执行阶段哪个卡的进程被误杀",
     "Fault Case":  "1. 分布式并行训练基础样例: "
                    "https://www.mindspore.cn/tutorials/experts/zh-CN/r1.8/parallel/train_ascend.html "
                    "2.mindspore状态信息定位错误节点： "
                    "https://bbs.huaweicloud.com/forum/thread-180967-1-1.html "}
]
