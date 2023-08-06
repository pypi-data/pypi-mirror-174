import os, sys, uuid, json, boto3
import quick_utils
from datetime import datetime

SCRIPT_DIR = str(os.path.dirname(os.path.realpath(__file__)))
HOME_PATH = os.path.expanduser('~')
AWS_CONFIG = quick_utils.loadJSON(os.path.join(HOME_PATH,'.bioshedinit/','aws_config_constants.json')) \
             if os.path.exists(os.path.join(HOME_PATH,'.bioshedinit/','aws_config_constants.json')) \
             else quick_utils.loadJSON(os.path.join(SCRIPT_DIR,'aws_config_constants.json'))
SPECS_CONFIG = quick_utils.loadJSON(os.path.join(SCRIPT_DIR, 'specs.json'))

def submit_job_awsbatch( args ):
    """
    name: name of container
    tag: (optional) version tag of container
    program_args: program arguments (as a string)
    dependent_job_ids: (optional) list of IDs of dependent jobs
    ---
    jobinfo: JSON of submitted job info

    >>> submit_job_awsbatch( dict(name='test', program_args=''))
    0
    """
    def setJobProperties( module_name, module_version ):
        job_properties = {}
        job_properties['image'] = f"{AWS_CONFIG['ecr_registry']}/{module_name}:{module_version}"
        job_properties['vcpus'] = int(SPECS_CONFIG[module_name]['vcpu']) if (module_name in SPECS_CONFIG and 'vcpu' in SPECS_CONFIG[module_name]) else 1
        job_properties['memory'] = int(SPECS_CONFIG[module_name]['mem']) if (module_name in SPECS_CONFIG and 'mem' in SPECS_CONFIG[module_name]) else 1000
        job_properties['jobRoleArn'] = AWS_CONFIG['aws_ecs_job_role']
        return job_properties

    def setContainerOverrides( program_args ):
        overrides = [program_args] if program_args != '' else ['-test']
        return overrides

    def createDependentIdList( jobid_list ):
        jobid_list_final=[]
        jobid_list = jobid_list.split(',') if type(jobid_list)==str else jobid_list
        for jobid in jobid_list:
            if jobid != '':
                jobid_list_final.append({'jobId': jobid})
        return jobid_list_final

    cname = args['name']
    pargs = quick_utils.format_type(args['program_args'], 'string_space') if 'program_args' in args else ''
    ctag = args['tag'] if 'tag' in args else 'latest'
    dependent_job_ids = args['dependent_job_ids'] if 'dependent_job_ids' in args else []
    jobinfo = {}

    # unique ID for this job
    uid = str(uuid.uuid4())

    # initialize Batch boto3 client access
    print('\nSetting up boto3 client in {}...'.format(AWS_CONFIG['aws_region']))
    client = boto3.client('batch', region_name=AWS_CONFIG['aws_region'])

    # set properties for this job
    job_properties = setJobProperties( cname, ctag )
    job_name = f'job_{cname}_{uid}'
    print('Setting job properties for job: '+str(job_name))

    # get dependent ids
    dependent_ids = createDependentIdList( dependent_job_ids )

    # get the date and time stamp right before we submit job
    job_submission_timestamp = str(datetime.now())

    # set input and compute parameters for job submission - save this job submission info
    job_json = {}
    job_overrides = {'command': setContainerOverrides(pargs)}
    job_json['container_overrides'] = job_overrides
    job_json['jobqueue'] = AWS_CONFIG['jobqueue']
    job_json['jobname'] = job_name
    job_json['job_submission_timestamp'] = job_submission_timestamp

    # register job definition
    job_def_name = f'jdef_{cname}_{uid}'
    job_def_response = client.register_job_definition( jobDefinitionName = job_def_name,
                                                       type='container',
                                                       retryStrategy={'attempts': 3},
                                                       containerProperties=job_properties)
    print('\nRegistering Job Definition: '+str(job_def_name))

    # submit job
    job_submit_response = client.submit_job( jobName = job_name,
                                             jobQueue = AWS_CONFIG['jobqueue'],
                                             jobDefinition = job_def_name,
                                             containerOverrides = job_overrides,
                                             dependsOn=dependent_ids)
    job_name_submitted = str(job_submit_response['jobName'])
    job_id_final = str(job_submit_response['jobId'])

    return dict(module=cname, jobid=job_id_final, jobqueue=AWS_CONFIG['jobqueue'],
                joboverrides=job_overrides, program_args=pargs)
