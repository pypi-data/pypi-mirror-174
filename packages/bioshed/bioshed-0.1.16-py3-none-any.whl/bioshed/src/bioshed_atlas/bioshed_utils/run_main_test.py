import os, subprocess, sys
from datetime import datetime
import program_utils
import file_utils

def run_main( pargs ):
    # time the duration of module container run
    run_start = datetime.now()
    print('Container running...')
    print('Program arguments: {}'.format(str(pargs)))
    # initialize program run
    # program_params = program_utils.init_program()

    # download any cloud files
    # pargs_updated = file_utils.download_files( dict(program_arguments=pargs) )

    # run main program
    # program_utils.run_program( pargs_updated )

    # create run log that includes program run duration
    run_end = datetime.now()
    # program_utils.log_run( dict(program_arguments=pargs,
    #                            run_duration=str(run_end - run_start)))

    # upload output data files
    # program_utils.upload_output()
    print('Container finished in {}'.format(str(run_end - run_start)))
    return


if __name__ == '__main__':
    run_main(sys.argv[1:]) if len(sys.argv) > 1 else run_main([])
