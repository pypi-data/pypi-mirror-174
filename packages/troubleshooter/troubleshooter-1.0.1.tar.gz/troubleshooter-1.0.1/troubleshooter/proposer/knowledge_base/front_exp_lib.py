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
# coding=utf-8

front_experience_list_cn = [
    {"ID": "Front-0001",
     "Fault Name": "加载checkpoint文件失败",
     "Key Log Information": "the checkpoint file: .* does not exist",
     "Key Python Stack Information": "load_checkpoint",
     "Key C++ Stack Information": "",
     "Fault Cause": "1. checkpoint文件路径设置错误；"
                    "2. checkpoint文件名设置错误",
     "Modification Suggestion": "检查checkpoint文件路径和文件名称是否正确，确认文件是否存在。",
     "Fault Case": "1.  load_checkpoint API: "
                   "https://www.mindspore.cn/docs/api/zh-CN/master/api_python/mindspore/mindspore.load_checkpoint.html  "
                   "2.  加載checkpoint報錯案例： "
                   "https://bbs.huaweicloud.com/forum/thread-181363-1-1.html"},
    {"ID": "Front-0002",
     "Fault Name": "加载checkpoint文件失败",
     "Key Log Information": "the checkpoint file should end with",
     "Key Python Stack Information": "load_checkpoint",
     "Key C++ Stack Information": "",
     "Fault Cause": "checkpoint文件名设置错误",
     "Modification Suggestion": "检查checkpoint文件路径和文件名称是否正确。",
     "Fault Case": "load_checkpoint API: "
                   "https://www.mindspore.cn/docs/api/zh-CN/master/api_python/mindspore/mindspore.load_checkpoint.html"},
    {"ID": "Front-0003",
     "Device Type": "All",
     "Sink Mode": "",
     "Fault Name": "加载checkpoint文件参数与网络参数不匹配",
     "Key Log Information": ".* in the argument .net. should have the same shape as .* in the argument .parameter_dict.",
     "Key Python Stack Information": "load_param_into_net",
     "Key C++ Stack Information": "",
     "Fault Cause": "网络中参数的shape和ckpt中的shape可能不一致，无法正确加载模型参数",
     "Modification Suggestion": "1.  检测网络结构与checkpoint是否对应，以及网络的超参数；           "
                                "2. 确定保存和加载checkpoint时的网络结构一致.",
     "Fault Case": "1.  load_param_into_net API:                 "
                   "https://www.mindspore.cn/docs/api/zh-CN/master/api_python/mindspore/mindspore.load_param_into_net.html "
                   "2. 网络参数shape不同报错案例：                                                "
                   "https://bbs.huaweicloud.com/forum/thread-181363-1-1.html"},
    {
        "Fault Name": "context报错",
        "Key Log Information": "context.set_context",
        "Key Python Stack Information": "mindspore.context.py",
        "Key C++ Stack Information": "",
        "Fault Cause": "context.set_context上下文设置错误",
        "Fixed Case": """
                  import mindspore as ms
                  ms.set_context(mode=ms.PYNATIVE_MODE)
                  ms.set_context(precompile_only=True)
                  ms.set_context(device_target="Ascend")
                  ms.set_context(device_id=0)
                  ms.set_context(save_graphs=True,
                     save_graphs_path="./model.ms")
                  ms.set_context(enable_reduce_precision=True)
                  ms.set_context(enable_graph_kernel=True)
                  ms.set_context(graph_kernel_flags=
                     "--opt_level=2 --dump_as_text")
                  ms.set_context(reserve_class_name_in_scope=True)
                  ms.set_context(variable_memory_max_size="6GB")
                  ms.set_context(check_bprop=True)
                  ms.set_context(max_device_memory="3.5GB")
                  ms.set_context(mempool_block_size="1GB")
                  ms.set_context(print_file_path="print.pb")
                  ms.set_context(max_call_depth=80)
                  ms.set_context(env_config_path=
                     "./env_config.json")
                  ms.set_context(auto_tune_mode="GA,RL")
                  ms.set_context(grad_for_scalar=True)
                  ms.set_context(enable_compile_cache=True, 
                     compile_cache_path="./cache.ms")
                  ms.set_context(pynative_synchronize=True)
                  ms.set_context(runtime_num_threads=10)
                  ms.set_context(disable_format_transform=True)
                  """,
        "Modification Suggestion": "参考set_context接口定义，根据报错信息修改配置项。",
        "Fault Case": "1. set_context接口定义： "
                      "https://www.mindspore.cn/docs/zh-CN/r1.8/api_python/mindspore/mindspore.set_context.html"
    }
]

general_front_experience_list_cn = [
    {
        "Fault Name": "Callback回调函数使用错误",
        "Key Log Information": "",
        "Key Python Stack Information": "",
        "Key C++ Stack Information": "mindspore.*\.cc",
        "Code Path": "callback._callback\.py",
        "Fault Cause": "mindspore callback接口错误",
        "Modification Suggestion": "1.查看callback接口定义和使用方式，分析报错位置和报错原因； "
                                   "2.查看官网callback接口官网说明，确认使用方法是否正确; "
                                   "3.在社区论坛，搜索callback相关案例或者提问",
        "Fault Case": "1. 官网Callback接口定义： "
                      "https://www.mindspore.cn/docs/zh-CN/r1.8/api_python/mindspore/mindspore.Callback.html "
                      "2. 官网Callback使用说明： "
                      "https://www.mindspore.cn/tutorials/experts/zh-CN/r1.8/debug/custom_debug.html"
    },
    {
        "Fault Name": "API接口使用错误",
        "Key Log Information": "",
        "Key Python Stack Information": "",
        "Key C++ Stack Information": "mindspore.*\.cc",
        "Code Path": "mindspore.python.mindspore.common;mindspore.python.mindspore.numpy;mindspore.python.mindspore.nn;"
                     "mindspore.python.mindspore.train",
        "Fault Cause": "API接口使用错误",
        "Modification Suggestion": "1.分析接口错误场景，场景包括：context参数设置错误、API参数错误、变量初始化失败、功能限制等 "
                                   "2.针对故障类别，查看官网资料说明及FAQ;                              "
                                   "3.在社区论坛，使用报错信息搜索相关案例. ",
        "Fault Case": "1. 接口API：                       "
                      "https://www.mindspore.cn/docs/zh-CN/r1.8/api_python/mindspore.html"
                      "2. 功能调试案例：                       "
                      "https://bbs.huaweicloud.com/forum/forum-1076-2704-1.html"}
]
