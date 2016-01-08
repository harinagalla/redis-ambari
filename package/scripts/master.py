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
  	Execute('rm ' +params.temp_file, ignore_failures=True)
  	Execute('mkdir -p ' + params.redis_dir)
  	Execute('chown -R ' + params.redis_user + ':' + params.redis_group + ' ' + params.redis_dir)
  	Execute('echo Installing pachages')
  	
  	if not os.path.exists(params.temp_file):
  	  Execute('wget ' + stable_package + ' -O ' + params.temp_file + ' -a ' + params.redis_log_file, user=params.redis_user)
  	Execute('tar xvzf ' + params.temp_file+' -C ' + params.redis_install_dir + ' >> ' + params.redis_log_file, user=params.redis_user)
  	Execute('cd '+params.redis_dir+'; make', user=params.redis_user)
  	Execute('wget https://raw.githubusercontent.com/harinagalla/redis-ambari/patch-2/configuration/redis-server /opt/redis-3.0.6', user=params.redis_user)
  	Execute('rm /opt/redis-3.0.6/redis.conf; rm -rf /etc/redis; rm -rf /var/lib/redis; rm /usr/local/bin/redis-server, rm /etc/init.d/redis-server', user=params.redis_user)
  	Execute('wget https://raw.githubusercontent.com/harinagalla/redis-ambari/patch-2/configuration/redis.conf /opt/redis-3.0.6', user=params.redis_user)
  	Execute('mkdir -p /etc/redis', user=params.redis_user)
  	Execute('mkdir -p /var/lib/redis', user=params.redis_user)
  	Execute('cp /opt/redis-3.0.6/redis-server /usr/local/bin', user=params.redis_user)
  	Execute('mv /opt/redis-3.0.6/redis-server /etc/init.d', user=params.redis_user)
  	Execute('cp /opt/redis-3.0.6/redis.conf /etc/redis', user=params.redis_user)
  	Execute('chmod 755 /etc/init.d/redis-server', user=params.redis_user)
  	Execute('chkconfig --add redis-server', user=params.redis_user)
  	Execute('chkconfig --level 345 redis-server on', user=params.redis_user)
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
	  Execute('/etc/init.d/redis-server stop >> ' + params.redis_log_file, user= params.redis_user)
	  
  def start(self, env):
	  import params
	  import status_params
	  self.configure(env)
	  Execute('cd '+params.redis_dir+'; service redis-server start ', user=params.redis_user)
	
  def status(self, env):
	  import params
	  import status_params
	  Execute('service redis-server status >> ' + params.redis_log_file, user=params.redis_user)
	  
  def restart(self, env):
  	import params
  	import status_params
  	Execute('service redis-server restart >>' + params.redis_log_file, user=params.redis_user)
	
if __name__ == "__main__":
  Master().execute()
