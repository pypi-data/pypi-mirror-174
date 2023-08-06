import sys, os, yaml, json, subprocess
from pathlib import Path
# from decouple import config # pip install python-decouple
import aws_batch_utils
import quick_utils
import file_utils

SCRIPT_DIR = str(os.path.dirname(os.path.realpath(__file__)))
PKG = yaml.safe_load(Path(os.path.join(SCRIPT_DIR, 'packages.yaml')).read_text())
HOME_PATH = os.path.expanduser('~')
AWS_CONFIG = quick_utils.loadJSON(os.path.join(HOME_PATH,'.bioshedinit/','aws_config_constants.json')) \
             if os.path.exists(os.path.join(HOME_PATH,'.bioshedinit/','aws_config_constants.json')) \
             else quick_utils.loadJSON(os.path.join(SCRIPT_DIR,'aws_config_constants.json'))
CONTAINER_REGISTRY_URL = AWS_CONFIG['ecr_registry']
UTILS = ['program_utils.py', 'file_utils.py', 'aws_s3_utils.py', 'quick_utils.py', 'aws_config_constants.json', 'specs.json']

def run_container_local( args ):
    """ Runs a container on the local system (docker run)
    name: name of container
    tag: (optional) tag of container image
    args: program arguments
    need_sudo: (optional)
    dockerargs: arguments to docker run (optional)
    ---
    status: status code

    [TODO] try except

    >>> run_container_local( dict(name='test'))
    'sudo docker run test:latest '

    """
    # sudo docker run test:latest
    cname = args['name']
    ctag = args['tag'] if 'tag' in args else 'latest'
    pargs = quick_utils.format_type(args['args'], 'string_space') if 'args' in args else ''
    need_sudo = args['need_sudo'] if 'need_sudo' in args else 'y'
    dockerargs = str(args['dockerargs']).strip()+' ' if 'dockerargs' in args else ''
    container_registry = str(CONTAINER_REGISTRY_URL).rstrip('/')

    pullcmd = f'docker pull {container_registry}/{cname}:{ctag}'
    pullcmd = 'sudo '+pullcmd if need_sudo.lower()[0]=='y' else pullcmd
    subprocess.call(pullcmd, shell=True)

    cmd = f'docker run {dockerargs}{container_registry}/{cname}:{ctag} {pargs}'
    cmd = 'sudo '+cmd if need_sudo.lower()[0]=='y' else cmd
    subprocess.call(cmd, shell=True)
    return cmd

def run_container_remote( args ):
    """ Runs a container in a remote system
    name: name of container
    args: program arguments
    system: (optional) which system to run in (awsbatch, kubernetes,...)
    ---
    status: status code
    """
    cname = args['name']
    pargs = args['args'] if 'args' in args else ''
    system = args['system'] if 'system' in args else 'awsbatch'
    job_info = {}

    if system=='awsbatch':
        job_info = aws_batch_utils.submit_job_awsbatch( dict(name=cname, program_args=pargs))
    return job_info

def create_dockerfile( args ):
    """ Creates a Dockerfile for a container
    [TODO] create a global dict of {library: install command }
    [TODO] create a global dict of {dockerbase: dockerbaseimage }
    [TODO] update to adjust install command based on OS (apt-get for Ubuntu, yum for Red Hat)
    [NOTE] run_main.py - ENTRYPOINT for python and command-line programs
    [NOTE] support for simple installs from package repos. Custom installs of downloaded programs to come later.
    name: desired name of container
    requirements: path to package/lib/command requirements file
    base: (optional) base to use for Dockerfile - python2, python3, R, ubuntu, conda (default)
    ---
    dockerfile: path to dockerfile

    >>> create_dockerfile( dict(name="test", requirements="test/requirements.test.txt", base="conda"))
    'test.Dockerfile'

    """
    cname = args['name']
    req_file = args['requirements']
    image_base = args['base'] if 'base' in args else 'conda'
    reqs = []
    cmds = []

    # get package install definitions
    with open(req_file,'r') as f:
        for r in f:
            r = r.strip()
            if r in PKG['ubuntu']:
                # e.g., bedtools
                reqs.append(PKG['ubuntu'][r])
            elif r in PKG['R']:
                reqs.append(PKG['R'][r])
            else:
                # direct command - e.g., conda install -c anaconda bedtools
                # e.g., wget http://myfiles.tar.gz
                cmds.append(r)

    args['dockerfile'] = f'{cname}.Dockerfile'
    args['packages'] = reqs
    args['utils'] = UTILS
    args['commands'] =  cmds
    if image_base in ['python', 'conda', 'ubuntu', 'linux']:
        write_dockerfile_conda( args )
    elif image_base.upper()=='R':
        write_dockerfile_R( args )
    return args['dockerfile']

def create_makefile( args ):
    """ Creates makefile for building container
    name: desired name of container
    dockerfile: (optional) name of dockerfile
    tag: (optional) tag for container image
    ---
    makefile: path to makefile

    [TODO] push to Dockerhub instead. Won't have lowercase limitations

    >>> create_makefile( dict(name="test", dockerfile="test.Dockerfile") )
    'Makefile'
    """
    cname = args['name'].lower()  # ECR only takes lower-case
    dockerfile = args['dockerfile'] if 'dockerfile' in args else 'Dockerfile'
    ctag = args['tag'] if 'tag' in args else 'latest'

    with open('Makefile','w') as f:
        f.write(f'NAME={cname}\n')
        f.write(f'TAG={ctag}\n\n')
        f.write('all: build push\n\n')
        f.write('build:\n')
        f.write(f'\tdocker build -t $(NAME):$(TAG) -f {dockerfile} ./\n')
        f.write('\tdocker tag $(NAME):$(TAG) $(REGISTRY):$(TAG)\n\n')
        f.write('push:\n')
        f.write('\tdocker push $(REGISTRY):$(TAG)\n')
    return 'Makefile'

def run_makefile( args ):
    """ Runs makefile to build docker and create container image
    name: name of container
    url: (optional) url to main container repository to write to
    need_sudo: (optional) default yes

    [TODO] try except for subprocess
    [TODO] push to docker hub instead. Won't have lower case limitations

    >>> run_makefile( dict(name='test'))
    0
    """
    cname = args['name'].lower()
    creg_url = args['url'] if 'url' in args else CONTAINER_REGISTRY_URL
    need_sudo = args['need_sudo'] if 'need_sudo' in args else 'yes'

    cmd = f'make REGISTRY={creg_url}/{cname}'
    cmd = 'sudo '+cmd if need_sudo.lower()[0]=='y' else cmd
    subprocess.call(cmd, shell=True)
    return 0

def build_container( args ):
    """ Builds a new custom container.
    name: container name
    requirements: file listing packages and commands needed to run container
    codebase: codebase needed to run program - R, python, etc...
    ---
    status: status (integer)
    """
    cname = args['name']
    reqfile = args['requirements']
    codebase = args['codebase'] if 'codebase' in args else 'conda'

    dockerfile = create_dockerfile( dict(name=cname, requirements=reqfile, base=codebase))
    makefile = create_makefile( dict(name=cname, dockerfile=dockerfile))
    file_utils.save_files( dict(files=[dockerfile, reqfile], path='s3://hubmodules/{}/'.format(cname)))
    makestatus = run_makefile( dict(name=cname))
    return dict(status=makestatus)

def build_container_cli( cname, reqfile ):
    """ Command-line alias for build_container. Takes regular command-line args.
    cname: container name
    reqfile: requirements file
    """
    return build_container( dict(name=cname, requirements=reqfile))

def create_container( cname, reqfile ):
    """ Creates container - alias for build_container_cli
    """
    return build_container_cli( cname, reqfile )

def translate_command_to_docker( args ):
    """ Translates a command to proper dockerfile language

    name: container name
    command: cmd
    ---
    docker_commands: translated commands for use in dockerfile (as a list)
    """
    BUILT_IN_COMMANDS = ['FROM','ENV','RUN','WORKDIR','ADD','COPY','LABEL','CMD']
    args_out = {}
    docker_commands = []
    cmd = str(args['command']).strip()
    cname = args['name'] if 'name' in args else ''
    # if we already have a docker command, then we add as-is
    if cmd.split(' ')[0] in BUILT_IN_COMMANDS:
        docker_commands.append(cmd)
    elif cmd.startswith('wget'):
        docker_commands.append('RUN '+cmd)
        # get the file name only
        docker_commands.append('RUN tar -xzvf {} -C /'.format(cmd.split(' ')[-1].split('/')[-1]))
    elif cmd.endswith('.tar.gz'):
        # unzip and add to path
        docker_commands.append('RUN mkdir -p /software')
        docker_commands.append('COPY {} /software'.format(cmd))
        docker_commands.append('RUN tar -xzvf /software/{} -C /software'.format(cmd))
        docker_commands.append('ENV PATH="/software/{}/:$PATH"'.format(cmd[:-7]))
        docker_commands.append('ENV PATH="/software/{}/bin/:$PATH"'.format(cmd[:-7]))
    elif cmd.endswith('.zip'):
        # unzip and add to path
        docker_commands.append('COPY {} /'.format(cmd))
        docker_commands.append('RUN unzip /{}'.format(cmd))
        docker_commands.append('ENV PATH="/{}/:$PATH"'.format(cmd[:-7]))
        docker_commands.append('ENV PATH="/{}/bin/:$PATH"'.format(cmd[:-7]))
    elif cmd.startswith('git clone'):
        docker_commands.append('RUN conda install -c anaconda git')
        docker_commands.append('RUN {}'.format(cmd))
        docker_commands.append('ENV PATH="/{}/:$PATH"'.format(cmd.split('/')[-1][:-4]))
    elif cmd.startswith('PATH='):
        # for some programs, need to explicitly add the path
        docker_commands.append('ENV {}:$PATH"'.format(cmd.rstrip('"').rstrip("'")))
    elif cmd.startswith('install.packages('):
        # install R packages
        if '"' in cmd:
            docker_commands.append("RUN R -e '{}'".format(cmd))
        else:
            docker_commands.append('RUN R -e "{}"'.format(cmd))
    elif ('.' in cmd or cmd==cname) and len(cmd.split(' ')) <= 1:
        # assume that we are copying a file over
        docker_commands.append('COPY {} /'.format(cmd))
        docker_commands.append('ENV PATH="/:$PATH"')
    else:
        # otherwise assume we are trying to run some unix command
        docker_commands.append('RUN {}'.format(cmd))
    args_out['docker_commands'] = docker_commands
    return args_out

###########################################################

def write_dockerfile_conda( args ):
    """
    dockerfile: name of dockerfile
    ---
    dockerfile: name of dockerfile
    """
    dockerfile_name = args["dockerfile"]
    container_name = args["name"]
    pkg2install = args['packages']
    cmd2run = args['commands']
    utils_files = args['utils']

    with open(dockerfile_name,'w') as f:
        f.write("FROM continuumio/miniconda3\n")
        f.write('LABEL container.base.image = "miniconda3:python3.9"\n')
        f.write(f'LABEL software.name = "{container_name}"\n')
        f.write('RUN apt-get -y update && apt-get -y install python3-pip zip unzip\n')
        f.write('RUN pip install awscli boto3\n')
        # install a few core libraries
        f.write('RUN conda install -c bioconda bedtools\n')
        f.write('RUN conda install -c bioconda bcftools\n')
        # f.write('RUN conda install -c bioconda bedops\n')
        # package installs from requirements
        for p in pkg2install:
            f.write(f'RUN {p}\n')
        # extra docker commands to run
        for c in cmd2run:
            dclist = translate_command_to_docker(dict(command=c, name=container_name))['docker_commands']
            for dc in dclist:
                f.write(dc+'\n')
        # samtools
        f.write('RUN mkdir /samtools\n')
        f.write('ENV PATH="/samtools/:$PATH"\n')
        f.write('COPY samtools/bin/* /samtools/\n')
        # copy scripts
        f.write('WORKDIR /\n')
        for u in utils_files:
            f.write(f'COPY {u} /\n')
        f.write('COPY run_main.py /\n')
        f.write('ENV PATH="/usr/local/bin/:$PATH"\n')
        f.write('ENTRYPOINT ["python", "/run_main.py"]\n')
    return dict(dockerfile=dockerfile_name)

def write_dockerfile_R( args ):
    """
    dockerfile: name of dockerfile
    ---
    dockerfile: name of dockerfile
    """
    dockerfile_name = args["dockerfile"]
    container_name = args["name"]
    pkg2install = args['packages']
    cmd2run = args['commands']
    utils_files = args['utils']

    with open(dockerfile_name,'w') as f:
        f.write("FROM rocker/tidyverse:4.1.0\n")
        f.write('LABEL container.base.image = "rocker:tidyverse"\n')
        f.write(f'LABEL software.name = "{container_name}"\n')
        f.write('RUN apt-get -y update && apt-get -y install python3-pip zip unzip\n')
        f.write('RUN pip install awscli boto3\n')
        # install a few core libraries
        f.write('RUN echo \'local({r <- getOption("repos"); r["CRAN"] <- "http://cran.r-project.org"; options(repos=r)})\' > /.Rprofile\n')
        f.write('RUN ln -s /usr/local/lib/R/lib/libR.so /lib/x86_64-linux-gnu/libR.so\n')
        f.write('RUN R -e \'install.packages("png")\'\n')
        # package installs from requirements
        for p in pkg2install:
            if 'install.packages' in p:
                f.write(f"RUN R -e '{p}'\n")
            else:
                f.write(f"RUN {p}\n")
        # extra docker commands to run
        for c in cmd2run:
            dclist = translate_command_to_docker(dict(command=c))['docker_commands']
            for dc in dclist:
                f.write(dc+'\n')
        # samtools
        f.write('RUN mkdir /samtools\n')
        f.write('ENV PATH="/samtools/:$PATH"\n')
        f.write('COPY samtools/bin/* /samtools/\n')
        # copy scripts
        f.write('WORKDIR /\n')
        for u in utils_files:
            f.write(f'COPY {u} /\n')
        f.write('COPY run_main.py /\n')
        f.write('ENV PATH="/usr/local/bin/:$PATH"\n')
        f.write('ENTRYPOINT ["python3", "/run_main.py"]\n')
    return dict(dockerfile=dockerfile_name)
