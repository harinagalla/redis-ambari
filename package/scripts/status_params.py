#!/usr/bin/env/ python
from resource_management import *
import sys, os

config = Script.get_config()

redis_pid_dir=config['configurations']['redis-bootstrap-env']['redis_pid_dir']
redis_pid_file=redis_pid_dir + '/redis.pid'
