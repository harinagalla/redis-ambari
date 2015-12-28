import sys, os, pwd, signal, time
from resource_management import *
from subprocess import call

class Master(Script):
  	def install(self, env):

	import params
	import status_params

	stable_package='http://download.redis.io/releases/redis-3.0.6.tar.gz'

	service_packagedir = os.path.realpath(__file__).split('/scripts')[0]

	# Install packages listed in metainfo.xml
	self.install_packages(env)

	self.create_linux_user(params.redis_user, params>nifi_user)
	if params.redis_user != 'root'
		Execute('cp /etc/sudoers /etc/sudoers.bak')
		Execute('echo "'+params.redis_user+'	ALL=(ALL)	NOPASSWD: ALL" >> /etc/sudoers')
		Execute('echo Creating ' + params.redis_log_dir + ' ' + status_params.redis_pid_dir)

	#create the log dir if its not already present
	Directory([status_params.redis_pid_dir, params.redis_log_dir],
			owner=params.redis_user,
			group=params.redis_group,
			recursive=True
	)

	Execute('touch ' + params.redis_log_file, user=params.redis_user)
	Execute('rm -rf ' + params.redis_dir, ignore_failures=True)
	Execute('mkdir -p ' + params.redis_dir)
	Execute('chown -R ' + params.redis_user + ':' + params.redis_group + ' ' + params.redis_dir)

	Execute('echo Installing packages')

	if not os.path.exists(params.temp_file):
		Execute('wget ' + stable_package + ' -O ' + params.temp_file + ' -a ' + params.redis_log_file, user=params.redis_user)
	Execute('tar zxf ' + params.temp_file+' -C ' + params.redis_install_dir + ' >> ' + params.redis_log_file, user=params.redis_user)
	Execute('cd '+params.redis_install_dir)
	Execute('make')
	Execute('make test')
	Execute('make install')
	Execute('cd utils')
	Execute('chmod +x install_server.sh')
	Execute('./install_server.sh')

	self.configure(env,True)	

   	#if any other install steps were needed they can be added here


	def create_linux_user(self, user, group):
		try: pwd.getpwnam(user)
		except KeyError: Execute('adduser ' + user)
		try: grp.getgrnam(group)
		except KeyError: Execute('groupadd ' + group)
  
  	def configure(self, env, isInstall=False):
		import params
		import staus_params
		env.set_params(params)
		env.set_params(status_params)

		# write out redis.conf

	
  
  	#To stop the service, use the linux service stop command and pipe output to log file
  	def stop(self, env):
    		import params
		import status_params
    		Execute('service redis stop >>' + params.redis_log_file, user=params.redis_user)
		Execute('rm ' status_params.redis_pid_file)

  	#To start the service, use the linux service start command and pipe output to log file
  	def start(self, env):
		import params
		import status_params
		self.configure(env)
		Execute('echo pid file ' + status_params.redis_pid_file)
    		Execute('service redis start >>' + params.stack_log, user=params.redis_user)


  #To get status of the, use the linux service status command
  def status(self, env):
    import params
    import status_params
    check_process_status(status_params.redis_pid_file)
    Execute('service redis status')

def set_conf_bin(self, env):
    import params
      params.conf_dir = os.path.join(*[params.redis_install_dir,params.redis_dirname,'conf'])
      params.bin_dir = os.path.join(*[params.redis_install_dir,params.redis_dirname,'bin'])
   
if __name__ == "__main__":
  Master().execute()
