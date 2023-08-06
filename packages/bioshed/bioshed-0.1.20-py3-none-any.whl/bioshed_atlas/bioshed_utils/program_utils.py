import sys, os, subprocess, json
import aws_s3_utils
import quick_utils

def init_program( args ):
    """ Initialize program run.

    program_args: raw program arguments (as list)
    ---
    workingdir: working directory of container
    inputdir: input directory (where files are downloaded)
    outputdir: output directory (these files will be uploaded)
    remote_outputdir: remote output directory to eventually upload to
    program_args: formatted program arguments (list of commands)
       - // can be used to delimit multiple commands
       - e.g. cat hello.txt // echo hello

    [TODO] currently a hack-fix for checking pargs passed in - make cleaner
    """
    cwd = os.getcwd()
    inputdir = os.path.join(cwd,'hubinput/')
    outputdir = os.path.join(cwd,'huboutput/')
    os.mkdir(inputdir)
    os.mkdir(outputdir)
    pargs_passed_in = args['program_args']
    if type(pargs_passed_in)==type([]) and len(pargs_passed_in)==1:
        # program arguments passed in as a single-entry list (by Batch)
        pargs_passed_in = pargs_passed_in[0]
        pargs = quick_utils.args_to_list( pargs_passed_in, ' ')
    elif type(pargs_passed_in)==type([]) and len(pargs_passed_in)>1:
        # arguments passed in as a full list:
        pargs = pargs_passed_in
    else:
        # arguments passed in as a space-delimited string
        pargs = quick_utils.args_to_list( pargs_passed_in, ' ')

    pargs_all = []
    pargs_formatted = []
    for parg in pargs:
        if not parg.startswith('out::') and not parg.startswith('arg://') and parg.strip(' ')!='//':
            pargs_formatted.append(parg)
        elif parg.strip(' ')=='//' and pargs_formatted != []:
            # user passed multiple commands
            pargs_all.append(' '.join(pargs_formatted) )
            pargs_formatted = []
    if pargs_formatted != []:
        pargs_all.append( ' '.join(pargs_formatted) )

    remote_outputdir = get_remote_outputdir( dict(program_args=pargs))
    alt_inputs = get_alternate_inputs( dict(program_args=pargs, localdir=inputdir))

    params = {}
    params['workingdir'] = cwd.rstrip('/')+'/'
    params['inputdir'] = inputdir
    params['outputdir'] = outputdir
    params['remote_outputdir'] = remote_outputdir
    params['program_args'] = pargs_all
    params['alt_inputs'] = alt_inputs
    return params

def get_remote_outputdir( args ):
    """ Given program arguments, gets explicit remote output directory (or infers)

    program_args: program arguments
    cloud: remote cloud prefix (s3:// gcp:// )
    ---
    remote_outputdir: remote output directory
    """
    pargs = quick_utils.args_to_list( args['program_args'], ' ')
    cloud_prefix = args['cloud'] if 'cloud' in args else 's3://'
    remote_alt = ''
    remote_explicit = ''
    for parg in pargs:
        if parg.startswith(cloud_prefix):
            remote_alt = quick_utils.get_file_folder(parg)
        elif parg.startswith('out::'):
            remote_explicit = parg[5:]
    return remote_explicit if remote_explicit!='' else remote_alt

def get_alternate_inputs( args ):
    """ Given program arguments, downloads alternate input files if provided

    program_args: program arguments
    localdir: local directory to download files to
    ---
    alt_inputs: space-separated string of alternate input files
    """
    pargs = quick_utils.args_to_list( args['program_args'], ' ')
    localdir = args['localdir'] if 'localdir' in args else '/hubinput/'
    alt_files = ''
    for parg in pargs:
        if parg.startswith('alt::'):
            alt_files += parg[5:]+' '
    alt_files_local = download_files( dict(program_args=alt_files.strip(), localdir=localdir))
    return alt_files_local


def download_files( args ):
    """ Given program arguments, downloads any cloud files.
    program_args: program arguments (as a list of space-separated string of args)
    localdir: directory to download to
    ---
    program_args_out: formatted program arguments

    >>> download_files( dict(program_args=['cat s3://hubscratch/test-policies.txt', 'echo hello'], localdir='./'))

    """
    localdir = args['localdir']
    pargs_list = args['program_args']

    # a list of commands is passed in as program_args, so we iterate through this list
    program_args_out_all = []
    for pargs_command in pargs_list:
        pargs = quick_utils.args_to_list( pargs_command, ' ')
        program_args_out = []
        for p in pargs:
            # download from AWS
            if p.startswith('s3://') and aws_s3_utils.object_exists_s3( dict(path=p)):
                # download a file
                if '.' in p.split('/')[-1] and not p.endswith('/'):
                    out = aws_s3_utils.download_file_s3( dict(path=p, localdir=localdir))
                # download a folder
                else:
                    out = aws_s3_utils.download_folder_s3( dict(path=p, localdir=localdir))
                program_args_out.append(out)
            # download from GCP
            elif p.startswith('gcp://'):
                # placeholder for now
                program_args_out.append(p)
            else:
                program_args_out.append(p)
        if program_args_out != []:
            program_args_out_all.append(' '.join(program_args_out))

    return program_args_out_all


def run_program( args ):
    """ Runs program on command line.
    command: full command with program args to run (string)
    logfile: run log file name
    ---

    [TODO] try except for subprocess
    """
    try:
        cmd = args['command']
        logfile = args['logfile']

        subprocess.call(cmd+' > {}'.format(logfile), shell=True)
        if len(cmd.split(' ')) <= 1:
            subprocess.call(cmd+' --help', shell=True)
        return
    except:
        print('Error in running program: '+str(cmd))
        return

def log_run( args ):
    """ Logs program run with other information.
    command: full command with program args (string)
    program_logfile: name of program output log file
    run_logfile: name of entire run log file (contains additional metadata for this run)
    run_duration: ...
    ---

    """
    cmd = args['command']
    program_logfile = args['program_logfile']
    run_logfile = args['run_logfile']
    run_duration = args['run_duration']

    out = {'command': cmd, 'program_logfile': program_logfile,
           'run_logfile': run_logfile, 'run_duration': run_duration}
    quick_utils.writeJSON( out, run_logfile )
    return

def upload_output( args ):
    """ Upload all files in output directory to remote cloud

    local_outputdir: local output directory
    remote_outputdir: remote output directory
    ---
    remote_outputdir: ...
    """
    out = aws_s3_utils.upload_folder_s3( dict(localfolder=args['local_outputdir'], path=args['remote_outputdir']))
    return dict(remote_outputdir=out)
