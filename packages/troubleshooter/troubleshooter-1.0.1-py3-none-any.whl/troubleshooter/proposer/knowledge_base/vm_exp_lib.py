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

vm_experience_list_cn = [
   {"Fault Type": "device设备OOM",   # 设备侧内存的定义， Ascend 内存，GPU 内存
    "Key Log Information": "Allocate continuous memory failed",
    "Key Python Stack Information": "",
    "Key C++ Stack Information": "",
    "Fault Cause": "内存占用过多导致分配内存失败，可能原因有：batch_size的值设置过大；"
                   "引入了异常大的Parameter，例如：例如单个数据shape为[640,1024,80,81]，"
                   "数据类型为float32，单个数据大小超过15G，两个如此大小的数据相加时，"
                   "占用内存超过3*15G，容易造成Out of Memory",
    "Modification Suggestion": "1. 检查batch_size的值，尝试将batch_size的值设置减小. "
                               "2. 检查参数的shape，尝试减少shape. "
                               "3. 如果以上操作还是未能解决，可以上官方论坛发帖提出问题. ",
    "Fault Case": ": https://bbs.huaweicloud.com/forum/thread-169771-1-1.html"
                  ": https://www.mindspore.cn/docs/faq/zh-CN/master/implement_problem.html?highlight=out%20memory"},
   {"Fault Type": "device设备占用报错",
    "Key Log Information": "Malloc device memory failed",
    "Key Python Stack Information": "",
    "Key C++ Stack Information": "",
    "Fault Cause": "执行网络脚本的设备可能被其他任务占用",
    "Modification Suggestion": "Ascend设备使用npu-smi info查询设备的使用情况, GPU设备使用nvidia-smi查询。当设备被占用时:"
                               "1. 重新设置其他设备, 设置方法参考官网方法. "
                               "2. 查询哪些程序占用设备: ps -ef | grep python, 对占用进程进行处理. ",
    "Fault Case": "https://bbs.huaweicloud.com/forum/thread-183730-1-1.html"}
]

vm_general_experience_list_cn = [
    {"Fault Type": "网络执行报错",
     "Key Log Information": "run task error",
     "Key Python Stack Information": "",
     "Key C++ Stack Information": "",
     "Code Path":"ascend_session.cc",
     "Fault Cause": "网络执行报错，某个算子执行失败。",
     "Modification Suggestion": "1.查看最开始的ERROR报错信息，确认报错基本信息； "
                                "2.查找报错日志中关键字'Dump node'，确认报错的报错的算子名称 "
                                "3.根据算子名称，结合计算图IR信息，分析可能对应的报错代码行，区分是用户代码报错还是框架代码报错 "
                                "4.使用Dump功能，保存算子的输入和输出数据，按官网说明进行代码调试，分析算子报错的引入位置 ",
     "Fault Case": "1.Dump功能说明： "
                   "https://www.mindspore.cn/tutorials/experts/zh-CN/r1.8/debug/dump.html "
                   "2.自定义调试信息: "
                   "https://www.mindspore.cn/tutorials/experts/zh-CN/r1.8/debug/custom_debug.html"}
]
# Launch graph failed