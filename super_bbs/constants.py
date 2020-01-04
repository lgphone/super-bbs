import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

web_title = 'super_bbs'
web_desc = "这是另一个FakeV2EX"

# 是否打开操作记录
open_record_log = True

# 预定义角色
"""
admin   超级管理员  1
"""


# 释放锁lua脚本
release_lock_script = """
if redis.call('get', KEYS[1]) == ARGV[1] 
    then 
        return redis.call('del', KEYS[1]) 
    else 
        return 0
end
"""

default_password = '7758521'
