import sys, os, pwd, grp, signal, time, glob
from resource_management import *
from subprocess import call

class Master(Script):
  def install(self, env):
  	import params
  	import status_params
  	stable_package = 'http://download.redis.io/releases/redis-3.0.6.tar.gz'
  	service_packagedir = os.path.realpath(__file__).split('/scripts')[0]
  	
  	self.install_packages(env)
  	self.create_linux_user(params.redis_user, params.redis_group)
  	if params.redis_user != 'root':
  		Execute('cp /etc/sudoers /etc/sudoers.bak')
  		Execute('echo "'+params.redis_user+' ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers')
  		Execute('echo Creating ' + params.redis_log_dir + ' ' + status_params.redis_pid_dir)
  	
  	Directory([status_params.redis_pid_dir, params.redis_log_dir],
  	  owner=params.redis_user,
  	  group=params.redis_group,
  	  recursive=True
  	  )
  	Execute('touch ' + params.redis_log_file, user=params.redis_user)
  	Execute('rm -rf ' + params.redis_dir, ignore_failures=True)
  	Execute('mkdir -p ' + params.redis_dir)
  	Execute('chown -R ' + params.redis_user + ':' + params.redis_group + ' ' + params.redis_dir)
  	Execute('echo Installing pachages')
  	
  	if not os.path.exists(params.temp_file):
  	  Execute('wget ' + stable_package + ' -O ' + params.temp_file + ' -a ' + params.redis_log_file, user=params.redis_user)
  	  Execute('tar xvzf ' + params.temp_file+' -C ' + params.redis_install_dir + ' >> ' + params.redis_log_file, user=params.redis_user)
  	  Execute('cd '+params.redis_install_dir+'/redis-3.0.6')
  	  Execute('chmod +x '+params.redis_install_dir+'/redis-3.0.6')
  	  Execute('make'+ ' -a ' + params.redis_log_file, user=params.redis_user)
  	  Execute('make test'+ ' -a ' + params.redis_log_file, user=params.redis_user)
  	  Execute('wget https://raw.githubusercontent.com/harinagalla/redis-ambari/patch-2/configuration/redis-server'+ ' -a ' + params.redis_log_file, user=params.redis_user)
  	  Execute('rm redis.conf')
  	  Exwcute('wget https://raw.githubusercontent.com/harinagalla/redis-ambari/patch-2/configuration/redis.conf'+ ' -a ' + params.redis_log_file, user=params.redis_user)
  	  Execute('mkdir -p /etc/redis')
  	  Execute('mkdir -p /var/lib/redis')
  	  Execute('cp redis-server /usr/local/bin')
  	  Execute('cp redis.conf /etc/redis')
  	  Execute('mv redis-server /etc/init.d')
  	  Execute('chmod 755 /etc/init.d/redis-server')
  	  Execute('chkconfig --add redis-server')
  	  Execute('chkconfig --level 345 redis-server on')
  	self.configure(env,True)
	
  def create_linux_user(self, user, group):
	  try: pwd.getpwnam(user)
	  except KeyError: Execute('adduser ' + user)
	  try: grp.getgrnam(group)
	  except KeyError: Execute('groupadd ' + group)
	  
  def configure(self, env, isInstall=False):
	  import params
	  import status_params
	  env.set_params(params)
	  env.set_params(status_params)
	  
  def stop(self, env):
	  import params
	  import status_params
	  Execute('service redis-server stop >>' + params.redis_log_file, user= params.redis_user)
	  Execute('rm ' + status_params.redis_pid_file)
	  
  def start(self, env):
	  import params
	  import status_params
	  self.configure(env)
	  Execute('echo pid file ' + status_params.redis_pid_file)
	  Execute('/etc/init.d/redis-server start >>' + params.redis_log_file, user=params.redis_user)
	
  def status(self, env):
	  import params
	  import status_params
	  check_process_status(status_params.redis_pid_file)
	  Execute('service redis-server status >>' + params.redis_log_file, user=params.redis_user)
	  
  def restart(self, env):
  	import params
  	import status_params
  	Execute('service redis-server restart >>' + params.redis_log_file, user=params.redis_user)
	
  def set_conf_bin(self, env):
	  import params
	  params.conf_dir = os.path.join(*[params.redis_install_dir,params.redis_dirname,'conf'])
	  params.bin_dir = os.path.join(*[params.redis_install_dir,params.redis_dirname,'bin'])

if __name__ == "__main__":
  Master().execute()
