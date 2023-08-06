# implements a decentralized routines worker 
# connects to worker pool
# broadcast heartbeat
# listen to commands
# environment variables:
# SOURCE_FOLDER
# WORKERPOOL_STREAM
# GIT_SERVER
# GIT_USER
# GIT_ACRONYM
# GIT_TOKEN

import os,sys,psutil,time,json,boto3,subprocess
from importlib.metadata import version
import numpy as np
from pathlib import Path

import decentralizedroutines.defaults as defaults 
from SharedData.Logger import Logger
logger = Logger(r'decentralizedroutines\worker',user='worker')
from SharedData.SharedDataAWSKinesis import KinesisStreamConsumer,KinesisStreamProducer
from decentralizedroutines.worker_lib import send_command,install_repo,restart_program

Logger.log.info('Initializing decentralizedroutines worker version %s...' % \
    (version('decentralizedroutines')))

routines = []
consumer = KinesisStreamConsumer(os.environ['WORKERPOOL_STREAM'])
producer = KinesisStreamProducer(os.environ['WORKERPOOL_STREAM'])
SLEEP_TIME = int(os.environ['SLEEP_TIME'])

Logger.log.info('decentralizedroutines worker version %s STARTED!' % \
    (version('decentralizedroutines')))

while True:
    try:
            
        for proc in routines:
            if proc.poll() is not None:
                routines.remove(proc)

        if not consumer.consume():
            Logger.log.error('Cannot consume workerpool messages!')  
            time.sleep(30)          


        for record in consumer.stream_buffer:    
            print('Received:'+str(record))    
            
            command = record
            if ('job' in command) & ('target' in command):
                if ((command['target']==os.environ['USER_COMPUTER']) | (command['target']=='ALL')):
                    
                    if command['job'] == 'command':                    
                        send_command(command['command'])

                    elif command['job'] == 'gitpwd':      
                        if 'GIT_USER' in command:
                            os.environ['GIT_USER'] = command['GIT_USER']              
                        if 'GIT_TOKEN' in command:
                            os.environ['GIT_TOKEN'] = command['GIT_TOKEN']
                        if 'GIT_ACRONYM' in command:
                            os.environ['GIT_ACRONYM'] = command['GIT_ACRONYM']
                        if 'GIT_SERVER' in command:
                            os.environ['GIT_SERVER'] = command['GIT_SERVER']
                        Logger.log.info('Updated git parameters!')

                    elif command['job'] == 'routine':
                        Logger.log.info('Running routine %s/%s' % (command['repo'],command['routine']))
                        
                        if install_repo(command):                                            
                            # RUN ROUTINE                         
                            Logger.log.info('Starting process %s/%s...' % (command['repo'],command['routine'])) 
                            
                            repo_path=Path(os.environ['SOURCE_FOLDER'])/command['repo']
                            env = os.environ.copy()
                            env['VIRTUAL_ENV'] = str(repo_path/'venv')
                            env['PATH'] = str(repo_path/'venv')+';'+str(repo_path/'venv\\Scripts')+';'+env['PATH']
                            env['PYTHONPATH'] = str(repo_path/'venv')+';'+str(repo_path/'venv\\Scripts')
                            env['GIT_TERMINAL_PROMPT'] = "0"     

                            cmd = [str(repo_path/'venv\\Scripts\\python.exe'),str(repo_path/command['routine'])]                        
                            proc = subprocess.Popen(cmd,env=env)                            
                            routines.append(proc)   
                            
                            Logger.log.info('Starting process %s/%s DONE!' % (command['repo'],command['routine'])) 
                        else:
                            Logger.log.error('Aborting routine %s, could not install repo' % (command['routine']))

                    elif command['job'] == 'install':
                        Logger.log.info('Installing %s...' % (command['repo']))
                        if install_repo(command):   
                            Logger.log.info('Installing %s DONE!' % (command['repo']))
                        else:
                            Logger.log.error('Installing %s ERROR!' % (command['repo']))

                    elif command['job'] == 'status':    
                        Logger.log.info('Running %i process' % (len(routines)))
                        for proc in routines:
                            Logger.log.info('Process id %i' % (proc.pid))

                    elif command['job'] == 'restart':                    
                        restart_program()                

                    elif command['job'] == 'ping':
                        Logger.log.info('pong')

                    elif command['job'] == 'pong':
                        Logger.log.info('ping')

        consumer.stream_buffer = []
        time.sleep(SLEEP_TIME + SLEEP_TIME*np.random.rand() - SLEEP_TIME/2)

    except Exception as e:
        consumer.stream_buffer = []
        time.sleep(SLEEP_TIME + SLEEP_TIME*np.random.rand() - SLEEP_TIME/2)
        Logger.log.error('Worker ERROR')
        Logger.log.error(str(e))
    