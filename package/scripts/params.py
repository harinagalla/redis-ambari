#!/usr/bin/env python
from resource_management import *
from resource_management.libraries.script.script import Script
import sys, os, glob
from resource_management.libraries.functions.version import format_hdp_stack_version
from resource_management.libraries.functions.default import default

# config object that holds the configurations declared in the config xml file
config = Script.get_config()

redis_dirname = 'redis-3.0.6'

#params from redis-ambari-config
redis_install_dir = config['configurations']['redis-ambari-config']['redis.install_dir']
redis_port = config['configurations']['redis-ambari-config']['redis.port']
redis_log = config['configurations']['redis-ambari-config']['redis.log']

redis_dir = os.path.join(*[redis_install_dir,redis_dirname])
conf_dir=''
bin_dir=''

# params from redis-bootstrap
# redis_bootstrap_content = config['configurations']['redis-bootstrap-env']['content']
redis_user = config['configurations']['redis-bootstrap-env']['redis_user']
redis_group = config['configurations']['redis-bootstrap-env']['redis_group']
redis_log_dir = config['configurations']['redis-bootstrap-env']['redis_log_dir']
redis_log_file = os.path.join(redis_log_dir,'redis_setup.log')
redis_lock_file = '/var/lock/subsys/redis'

temp_file='/tmp/'+redis_dirname+'.zip'
