import os, subprocess, sys
from datetime import datetime
SCRIPT_DIR = str(os.path.dirname(os.path.realpath(__file__)))

sys.path.append(SCRIPT_DIR)
import program_utils
import file_utils

def run_main( pargs ):
    # time the duration of module container run
    run_start = datetime.now()
    run_start_string = str(run_start).replace(' ','-').replace(':','-').split('.')[0]
    print('Container running...')
    print('Program arguments: {}'.format(str(pargs)))

    # initialize program run - create input and output directories, format program arguments, etc
    params = program_utils.init_program( dict(program_args=pargs))

    # download any cloud files
    pargs_list_updated = program_utils.download_files( dict(program_args=params['program_args'], localdir=params['inputdir']))
    print('Program arguments after download: {}'.format(str(pargs_list_updated)))

    # run main program - run within output directory
    os.chdir(params['outputdir'])
    stdout_file = program_utils.create_stdout_file( dict(working_dir=params['outputdir']))
    program_log_name_list = []
    cmd_order = 1
    for pargs_updated in pargs_list_updated:
        program_log_name = os.path.join(params['outputdir'], 'program.{}.{}.{}.log'.format(str(pargs_updated.split(' ')[0]), run_start_string, str(cmd_order)))
        program_utils.run_program( dict(command=pargs_updated, logfile=program_log_name, printfile=stdout_file ))
        program_log_name_list.append(program_log_name)
        cmd_order += 1

    # create run log that includes program run duration
    run_end = datetime.now()
    run_log_name = os.path.join(params['outputdir'], 'run.{}.log'.format(str(run_start_string)))
    program_utils.log_run( dict(command=pargs_list_updated, program_logfile=program_log_name_list,
                                run_logfile=run_log_name,
                                run_duration=str(run_end - run_start)))

    # upload output data files
    program_utils.upload_output( dict(local_outputdir=params['outputdir'], remote_outputdir=params['remote_outputdir']))
    print('Container finished in {}'.format(str(run_end - run_start)))
    return


if __name__ == '__main__':
    run_main(sys.argv[1:]) if len(sys.argv) > 1 else run_main([])
