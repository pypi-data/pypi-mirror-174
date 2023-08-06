import os, boto3, subprocess, uuid, json, datetime
from dateutil.tz import *
import quick_utils

SCRIPT_DIR = str(os.path.dirname(os.path.realpath(__file__)))
HOME_PATH = os.path.expanduser('~')
AWS_CONFIG = quick_utils.loadJSON(os.path.join(HOME_PATH,'.bioshedinit/','aws_config_constants.json')) \
             if os.path.exists(os.path.join(HOME_PATH,'.bioshedinit/','aws_config_constants.json')) \
             else quick_utils.loadJSON(os.path.join(SCRIPT_DIR,'aws_config_constants.json'))

# initialize S3 access
if os.environ.get('AWS_ACCESS_KEY_ID') not in [None, ''] and os.environ.get('AWS_SECRET_ACCESS_KEY') not in [None, ''] and os.environ.get('HOME') not in [None, '']:
    if not os.path.exists(os.path.join(str(os.environ.get('HOME')), '.aws/')):
        os.mkdir(os.path.join(str(os.environ.get('HOME')), '.aws/'))
    if not os.path.exists(os.path.join(str(os.environ.get('HOME')), '.aws/credentials')):
        with open(os.path.join(str(os.environ.get('HOME')), '.aws/credentials'),'w') as f:
            f.write('[default]\naws_access_key_id = {}\naws_secret_access_key = {}\n'.format(str(os.environ.get('AWS_ACCESS_KEY_ID')), str(os.environ.get('AWS_SECRET_ACCESS_KEY'))))

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')

def _findMatches(f, patterns, matchAll = False):
    """ Wrapper for _findMatch to search for multiple patterns. If matchAll is True, must match all patterns.
    f: file name, e.g. 'hello.txt', STR
    patterns: patterns to search, e.g. '^.txt', ['^bam', 'myfile'], STR or LIST
    matchAll: do we need to match all patterns? BOOL
    RETURN: whether file matches patterns - True/False BOOL

    >>> _findMatches('myfile.txt', '^.txt')
    True
    >>> _findMatches('myfile.txt', 'myf^')
    True
    >>> _findMatches('myfile.txt', 'file^')
    False
    >>> _findMatches('myfile.bam', 'bam')
    True
    >>> _findMatches('myfile.txt', ['^.txt', 'super'])
    True
    >>> _findMatches('myfile.txt', ['^.txt', 'super'], True)
    False
    """
    matches = []
    if type(patterns) == str:
        patterns = [patterns] if patterns != '' else []

    # if patterns is empty, we return True by default
    if patterns == []:
        return True

    for p in patterns:
        matches.append(_findMatch(f, p))
    if matchAll == False:
        if True in matches:
            return True
        else:
            return False
    elif matchAll == True:
        if False in matches:
            return False
        else:
            return True


def _findMatch(f, p):
    """ function for searching for a pattern match for a file name f.
    Pattern can have the following:
    'bam': file name f contains 'bam'
    '^.txt': file name f ends in .txt
    'myfile^': file name begins with myfile

    f: file name, e.g. 'hello.txt' STR
    p: pattern to search, e.g. '^.txt' STR
    RETURN: if pattern is in file name BOOL

    >>> _findMatch('hello.fastq','^fastq')
    True
    >>> _findMatch('myfile.txt', '^.txt')
    True
    >>> _findMatch('myfile.txt', 'myf^')
    True
    >>> _findMatch('myfile.txt', 'file^')
    False
    >>> _findMatch('myfile.txt', 'file')
    True
    >>> _findMatch('myfile.txt', '')
    True
    """
    # print('FINDMATCH: file {}, pattern {}'.format(str(f), str(p)))
    _isMatch = False
    f = str(f).lower()
    p = str(p).lower()
    # if empty string
    if p == '[]' or p == "['']" or p == '':
        _isMatch = True
    # suffix - file extension at end of filename
    elif p[0]=='^' and p[-1]!='^':
        if f.endswith(p[1:]):
            _isMatch = True
    # prefix - file extension at beginning of filename
    elif p[-1]=='^' and p[0]!='^':
        if f.startswith(p[0:-1]):
            _isMatch = True
    # search pattern somewhere in file extension, separated from base file name by one of [_,-,.]
    elif p.rfind('^') > p.find('^'):
        i = p.find('^')
        j = p.rfind('^')
        if (f[f.find('_'):].find(p[i+1:j]) >= 0) or (f[f.find('.'):].find(p[i+1:j]) >= 0) or (f[f.find('-'):].find(p[i+1:j]) >= 0):
            _isMatch = True
    # search pattern anywhere in file name
    else:
        if f.find(p) >= 0:
            _isMatch = True
    return _isMatch

def get_aws_id():
    """ Uses boto3 to get the AWS account ID.
    """
    return boto3.client("sts").get_caller_identity()["Account"]


def transfer_file_s3( args ):
    """ Transfers object(s) from one S3 path to another S3 folder.

    path: S3 file path(s), STR or LIST
    outpath: S3 output path. Must be a folder, not a file extension.
    ---
    outfiles: S3 path of all output files, STR or LIST

    >>> transfer_file_s3( dict(path='s3://hubscratch/test.R', outpath='s3://hubscratch2/'))
    Transfering from s3://hubscratch/test.R to s3://hubscratch2/
    copy: s3://hubscratch/test.R to s3://hubscratch2/test.R
    's3://hubscratch2/test.R'

    [TODO] try except for subprocess
    """
    s3path = args['path']
    outpath = args['outpath']
    return_type = type(s3path)

    s3path = quick_utils.format_type(s3path, 'list')
    outfiles = []

    for s3p in s3path:
        if s3p.startswith('s3://'):
            print('Transfering from {} to {}'.format(s3p, outpath))
            cmd = ['aws','s3','cp',s3p,outpath]
            subprocess.call(cmd)
            outfiles.append(os.path.join(outpath,quick_utils.get_file_only(s3p)))
        else:
            print('{} needs to start with S3'.format(s3p))
    
    if return_type == type(''):
        outfiles = quick_utils.format_type(outfiles, 'str')
    return outfiles

def download_file_s3( args ):
    """ Downloads object(s) from S3 to a local file.
        Can be used to download multiple objects if list or comma-delim str is provided.
        Returns full file path of downloaded local file.

    path: S3 file path, s3://bioshed/myfile.bam, STR
    localdir: local directory to download to, /local/dir, STR
    ---
    localpath: (RETURN) full path of downloaded local file, e.g. '/local/dir/myfile.bam'
        - return type is same as input path type
        - if not a valid S3 path, then an empty string is returned

    >>> download_file_s3( dict(path='s3://hubpublicinternal/test/aws_s3_utils/test-R1.fastq.gz', localdir='./testout/'))
    Downloading from S3 - s3://hubpublicinternal/test/aws_s3_utils/test-R1.fastq.gz to ./testout/
    './testout/test-R1.fastq.gz'

    >>> download_file_s3( dict(path='s3://hubpublicinternal/test/aws_s3_utils/test-R1.fastq.gz,s3://hubpublicinternal/test/aws_s3_utils/test-R2.fastq.gz', localdir='./testout/'))
    Downloading from S3 - s3://hubpublicinternal/test/aws_s3_utils/test-R1.fastq.gz to ./testout/
    Downloading from S3 - s3://hubpublicinternal/test/aws_s3_utils/test-R2.fastq.gz to ./testout/
    './testout/test-R1.fastq.gz,./testout/test-R2.fastq.gz'

    >>> download_file_s3( dict(path=['s3://hubpublicinternal/test/aws_s3_utils/test-R1.fastq.gz','s3://hubpublicinternal/test/aws_s3_utils/test-R2.fastq.gz'], localdir='./testout/'))
    Downloading from S3 - s3://hubpublicinternal/test/aws_s3_utils/test-R1.fastq.gz to ./testout/
    Downloading from S3 - s3://hubpublicinternal/test/aws_s3_utils/test-R2.fastq.gz to ./testout/
    ['./testout/test-R1.fastq.gz', './testout/test-R2.fastq.gz']
    """
    s3path = args['path']
    localdir = args['localdir']
    return_type = type(s3path)

    s3path = quick_utils.format_type(s3path, 'list')
    localpath = []

    for s3p in s3path:
        if s3p.startswith('s3://'):
            print('Downloading from S3 - {} to {}'.format(s3p, localdir))
            bucket = s3p.split('/')[2]
            key = '/'.join(s3p.split('/')[3:])

            object_filename = key.split('/')[-1]
            local_filename = os.path.join(localdir, object_filename)

            s3.Object(bucket,key).download_file(local_filename)
            localpath.append(local_filename)
        else:
            print('{} needs to start with S3'.format(s3p))

    if return_type == type(''):
        localpath = quick_utils.format_type(localpath, 'str')
    return localpath

def download_folder_s3( args ):
    """ Downloads a folder (and sub-folders) from S3 to a local directory.
        Can specify multiple folders.
        Can search for a pattern by passing this into the 'pattern' key
        Returns the local directory containing the download files.

    path: S3 folder path(s), e.g., 's3://bioshed/test/'
    localdir: local directory to download to, e.g. '/local/dir/'
    *pattern: restrict download to files that match a certain pattern (e.g., '*.fastq.gz')
    *excludepattern: do not download files that match a certain pattern (e.g., '*.fastq.gz')
        - can pass a list to pattern
    ---
    localdir: (RETURN) full path of local folder, e.g. '/local/dir/'

    [TODO] try except for subprocess

    >>> download_folder_s3( dict(path='s3://hubpublicinternal/test/aws_s3_utils/', localdir='./testout/'))
    ['aws', 's3', 'cp', '--recursive', 's3://hubpublicinternal/test/aws_s3_utils/', './testout/']
    download: s3://hubpublicinternal/test/aws_s3_utils/test.create_fastq.log to testout/test.create_fastq.log
    download: s3://hubpublicinternal/test/aws_s3_utils/test-R1.fastq.gz to testout/test-R1.fastq.gz
    download: s3://hubpublicinternal/test/aws_s3_utils/test-R2.fastq.gz to testout/test-R2.fastq.gz
    download: s3://hubpublicinternal/test/aws_s3_utils/test-upload-R2.fastq.gz to testout/test-upload-R2.fastq.gz
    download: s3://hubpublicinternal/test/aws_s3_utils/test-upload-R1.fastq.gz to testout/test-upload-R1.fastq.gz
    download: s3://hubpublicinternal/test/aws_s3_utils/test-upload.create_fastq.log to testout/test-upload.create_fastq.log
    './testout/'

    >>> download_folder_s3( dict(path=['s3://hubpublicinternal/test/aws_s3_utils/', 's3://hubpublicinternal/test/file_utils/run_test1/sample_test1/mpileup/'], localdir='./testout2/'))
    ['aws', 's3', 'cp', '--recursive', 's3://hubpublicinternal/test/aws_s3_utils/', './testout2/']
    download: s3://hubpublicinternal/test/aws_s3_utils/test-R1.fastq.gz to testout2/test-R1.fastq.gz
    download: s3://hubpublicinternal/test/aws_s3_utils/test-R2.fastq.gz to testout2/test-R2.fastq.gz
    download: s3://hubpublicinternal/test/aws_s3_utils/test-upload-R1.fastq.gz to testout2/test-upload-R1.fastq.gz
    download: s3://hubpublicinternal/test/aws_s3_utils/test-upload.create_fastq.log to testout2/test-upload.create_fastq.log
    download: s3://hubpublicinternal/test/aws_s3_utils/test.create_fastq.log to testout2/test.create_fastq.log
    download: s3://hubpublicinternal/test/aws_s3_utils/test-upload-R2.fastq.gz to testout2/test-upload-R2.fastq.gz
    ['aws', 's3', 'cp', '--recursive', 's3://hubpublicinternal/test/file_utils/run_test1/sample_test1/mpileup/', './testout2/']
    download: s3://hubpublicinternal/test/file_utils/run_test1/sample_test1/mpileup/mpileup.sample_test1.job.log to testout2/mpileup.sample_test1.job.log
    download: s3://hubpublicinternal/test/file_utils/run_test1/sample_test1/mpileup/sample_test1.mpileup.pileup to testout2/sample_test1.mpileup.pileup
    ['./testout2/']

    >>> download_folder_s3( dict(path='s3://hubpublicinternal/test/aws_s3_utils/', localdir='./testout2/', pattern='*.fastq.gz'))
    aws s3 cp --recursive s3://hubpublicinternal/test/aws_s3_utils/ ./testout2/ --exclude "*" --include "*.fastq.gz"
    download: s3://hubpublicinternal/test/aws_s3_utils/test-upload-R1.fastq.gz to testout2/test-upload-R1.fastq.gz
    download: s3://hubpublicinternal/test/aws_s3_utils/test-R2.fastq.gz to testout2/test-R2.fastq.gz
    download: s3://hubpublicinternal/test/aws_s3_utils/test-R1.fastq.gz to testout2/test-R1.fastq.gz
    download: s3://hubpublicinternal/test/aws_s3_utils/test-upload-R2.fastq.gz to testout2/test-upload-R2.fastq.gz
    './testout2/'

    >>> download_folder_s3( dict(path='s3://hubpublicinternal/test/aws_s3_utils/', localdir='./testout2/', excludepattern='*.fastq.gz'))
    aws s3 cp --recursive s3://hubpublicinternal/test/aws_s3_utils/ ./testout2/ --exclude "*.fastq.gz"
    download: s3://hubpublicinternal/test/aws_s3_utils/test-upload.create_fastq.log to testout2/test-upload.create_fastq.log
    download: s3://hubpublicinternal/test/aws_s3_utils/test.create_fastq.log to testout2/test.create_fastq.log
    './testout2/'
    """
    s3path = args['path']
    localdir = args['localdir'].rstrip('/')+'/'
    searchpattern = args['pattern'] if 'pattern' in args else ''
    excludepattern = args['excludepattern'] if 'excludepattern' in args else ''
    return_type = type(s3path)

    s3path = quick_utils.format_type(s3path, 'list')
    searchpattern = quick_utils.format_type(searchpattern, 'list')
    excludepattern = quick_utils.format_type(excludepattern, 'list')

    for s3p in s3path:
        if s3p.startswith('s3://'):
            if searchpattern in ['',[]] and excludepattern in ['',[]]:
                cmd = ['aws','s3','cp','--recursive',s3p.rstrip('/')+'/',localdir]
                print(cmd)
                subprocess.check_call(cmd)
            else:
                cmd = 'aws s3 cp --recursive {} {}'.format(s3p, localdir)
                if searchpattern not in ['',[]]:
                    cmd += ' --exclude "*"'
                    for pattern in searchpattern:
                        pattern_with_quotes = '"'+pattern+'"'
                        cmd += ' --include {}'.format(pattern_with_quotes)
                elif excludepattern not in ['',[]]:
                    for pattern in excludepattern:
                        pattern_with_quotes = '"'+pattern+'"'
                        cmd += ' --exclude {}'.format(pattern_with_quotes)
                print(cmd)
                subprocess.call(cmd, shell=True)
    return localdir

def upload_file_s3( args ):
    """ Securely uploads local file(s) to a path in S3.
        Full path of localfile should be specified in the input.

    localfile: local file(s) to upload
    path: S3 folder path to upload to, e.g., 's3://bioshed/test/'

    >>> upload_file_s3( dict(localfile='./testout/test-R1.fastq.gz', path='s3://hubpublicinternal/test/upload/'))
    Uploading to s3 - ./testout/test-R1.fastq.gz to s3://hubpublicinternal/test/upload/
    's3://hubpublicinternal/test/upload/test-R1.fastq.gz'

    >>> upload_file_s3( dict(localfile='./testout/test-R1.fastq.gz,./testout/test-R2.fastq.gz', path='s3://hubpublicinternal/test/upload/'))
    Uploading to s3 - ./testout/test-R1.fastq.gz to s3://hubpublicinternal/test/upload/
    Uploading to s3 - ./testout/test-R2.fastq.gz to s3://hubpublicinternal/test/upload/
    's3://hubpublicinternal/test/upload/test-R1.fastq.gz,s3://hubpublicinternal/test/upload/test-R2.fastq.gz'

    >>> upload_file_s3( dict(localfile=['./testout/test-R1.fastq.gz', './testout/test-R2.fastq.gz'], path='s3://hubpublicinternal/test/upload/'))
    Uploading to s3 - ./testout/test-R1.fastq.gz to s3://hubpublicinternal/test/upload/
    Uploading to s3 - ./testout/test-R2.fastq.gz to s3://hubpublicinternal/test/upload/
    ['s3://hubpublicinternal/test/upload/test-R1.fastq.gz', 's3://hubpublicinternal/test/upload/test-R2.fastq.gz']
    """
    s3path = args['path']
    localfile = args['localfile']
    return_type = type(localfile)

    localfile = quick_utils.format_type(localfile, 'list')
    remotefile = []

    if s3path.startswith('s3://'):
        for f in localfile:
            print('Uploading to s3 - {} to {}'.format(str(f), str(s3path)))
            bucket = s3path.split('/')[2]
            key = os.path.join('/'.join((s3path.rstrip('/')+'/').split('/')[3:-1]),f.split('/')[-1])
            response = s3.Object(bucket,key).upload_file(f, ExtraArgs=dict(ServerSideEncryption='AES256'))
            # maybe check response here
            remotefile.append(os.path.join(s3path, quick_utils.get_file_only(f)))

    if return_type == type(''):
        remotefile = quick_utils.format_type(remotefile, 'str')

    return remotefile

def upload_folder_s3( args ):
    """ Uploads all files in a folder (and sub-folders) from S3 to a local directory.
        Can specify multiple folders.
        Automatically use server-side encryption.
        Returns path to upload folder.

    localfolder: local folder(s) to upload
    path: S3 folder path to upload to, e.g., 's3://bioshed/test/'
    *pattern: restrict upload to files that match a certain pattern (e.g., '*.fastq.gz')
    *excludepattern: do not upload files that match a certain pattern (e.g., '*.fastq.gz')
        - can pass a list to pattern
    ---
    path: S3 upload folder

    >>> upload_folder_s3( dict(localfolder='./testout/', path='s3://hubpublicinternal/test/upload/'))
    ['aws', 's3', 'cp', '--recursive', '--sse', 'AES256', './testout/', 's3://hubpublicinternal/test/upload/']
    upload: testout/test-R1.fastq.gz to s3://hubpublicinternal/test/upload/test-R1.fastq.gz
    upload: testout/test-upload-R1.fastq.gz to s3://hubpublicinternal/test/upload/test-upload-R1.fastq.gz
    upload: testout/test-upload.create_fastq.log to s3://hubpublicinternal/test/upload/test-upload.create_fastq.log
    upload: testout/test.create_fastq.log to s3://hubpublicinternal/test/upload/test.create_fastq.log
    upload: testout/test-upload-R2.fastq.gz to s3://hubpublicinternal/test/upload/test-upload-R2.fastq.gz
    upload: testout/test-R2.fastq.gz to s3://hubpublicinternal/test/upload/test-R2.fastq.gz
    's3://hubpublicinternal/test/upload/'

    >>> upload_folder_s3( dict(localfolder='./testout/', path='s3://hubpublicinternal/test/upload/', pattern='*.fastq.gz'))
    ['aws', 's3', 'cp', '--recursive', '--sse', 'AES256', './testout/', 's3://hubpublicinternal/test/upload/', '--exclude', '*', '--include', '*.fastq.gz']
    upload: testout/test-R1.fastq.gz to s3://hubpublicinternal/test/upload/test-R1.fastq.gz
    upload: testout/test-R2.fastq.gz to s3://hubpublicinternal/test/upload/test-R2.fastq.gz
    upload: testout/test-upload-R2.fastq.gz to s3://hubpublicinternal/test/upload/test-upload-R2.fastq.gz
    upload: testout/test-upload-R1.fastq.gz to s3://hubpublicinternal/test/upload/test-upload-R1.fastq.gz
    's3://hubpublicinternal/test/upload/'

    >>> upload_folder_s3( dict(localfolder=['./testout/', './testout2/'], path='s3://hubpublicinternal/test/upload/', pattern='*.fastq.gz'))
    ['aws', 's3', 'cp', '--recursive', '--sse', 'AES256', './testout/', 's3://hubpublicinternal/test/upload/', '--exclude', '*', '--include', '*.fastq.gz']
    upload: testout/test-R1.fastq.gz to s3://hubpublicinternal/test/upload/test-R1.fastq.gz
    upload: testout/test-R2.fastq.gz to s3://hubpublicinternal/test/upload/test-R2.fastq.gz
    upload: testout/test-upload-R2.fastq.gz to s3://hubpublicinternal/test/upload/test-upload-R2.fastq.gz
    upload: testout/test-upload-R1.fastq.gz to s3://hubpublicinternal/test/upload/test-upload-R1.fastq.gz
    ['aws', 's3', 'cp', '--recursive', '--sse', 'AES256', './testout2/', 's3://hubpublicinternal/test/upload/', '--exclude', '*', '--include', '*.fastq.gz']
    upload: testout2/test-upload-R1.fastq.gz to s3://hubpublicinternal/test/upload/test-upload-R1.fastq.gz
    upload: testout2/test-R1.fastq.gz to s3://hubpublicinternal/test/upload/test-R1.fastq.gz
    upload: testout2/test-R2.fastq.gz to s3://hubpublicinternal/test/upload/test-R2.fastq.gz
    upload: testout2/test-upload-R2.fastq.gz to s3://hubpublicinternal/test/upload/test-upload-R2.fastq.gz
    's3://hubpublicinternal/test/upload/'

    >>> upload_folder_s3( dict(localfolder=['./testout/', './testout2/'], path='s3://hubpublicinternal/test/upload/', excludepattern='*.fastq.gz'))
    ['aws', 's3', 'cp', '--recursive', '--sse', 'AES256', './testout/', 's3://hubpublicinternal/test/upload/', '--exclude', '*.fastq.gz']
    upload: testout/test-upload.create_fastq.log to s3://hubpublicinternal/test/upload/test-upload.create_fastq.log
    upload: testout/test.create_fastq.log to s3://hubpublicinternal/test/upload/test.create_fastq.log
    ['aws', 's3', 'cp', '--recursive', '--sse', 'AES256', './testout2/', 's3://hubpublicinternal/test/upload/', '--exclude', '*.fastq.gz']
    upload: testout2/test.create_fastq.log to s3://hubpublicinternal/test/upload/test.create_fastq.log
    upload: testout2/test-upload.create_fastq.log to s3://hubpublicinternal/test/upload/test-upload.create_fastq.log
    upload: testout2/mpileup.sample_test1.job.log to s3://hubpublicinternal/test/upload/mpileup.sample_test1.job.log
    upload: testout2/sample_test1.mpileup.pileup to s3://hubpublicinternal/test/upload/sample_test1.mpileup.pileup
    's3://hubpublicinternal/test/upload/'
    """
    s3path = args['path']
    localfolder = args['localfolder']
    return_type = type(localfolder)
    includepattern = args['pattern'] if 'pattern' in args else ''
    excludepattern = args['excludepattern'] if 'excludepattern' in args else ''

    localfolder = quick_utils.format_type(localfolder, 'list')
    includepattern = quick_utils.format_type(includepattern, 'list')
    excludepattern = quick_utils.format_type(excludepattern, 'list')

    if s3path.startswith('s3://'):
        for f in localfolder:
            cmd = ['aws','s3','cp','--recursive','--sse','AES256',f.rstrip('/')+'/',s3path.rstrip('/')+'/']
            if includepattern not in ['', []]:
                cmd += ['--exclude','*']
                for p in includepattern:
                    cmd += ['--include', p]
            elif excludepattern not in ['', []]:
                for p in excludepattern:
                    cmd += ['--exclude', p]
            print(cmd)
            response = subprocess.check_call(cmd)

    return s3path

def object_exists_s3( args ):
    """ Checks if an object exists in S3.
    path: S3 path
    ---
    exists: (BOOL)
    """
    return False if get_objects_s3( args )==[] else True

def get_objects_s3( args ):
    """ Get objects with full metadata at a given S3 path.
    path: S3 path
    ---
    response: AWS-formatted response containing full metadata for each object
    """
    s3path = args['path']

    bucket = s3path.split('/')[2]
    key = str('/'.join(s3path.split('/')[3:])).rstrip('/') + '/'
    region = AWS_CONFIG['aws_region']
    # s3_endpoint = '{}.s3.{}.amazonaws.com/{}'.format(bucket,region,key)
    response = s3_client.list_objects_v2( Bucket=bucket, Prefix=key, Delimiter='/', MaxKeys=5000, StartAfter=key )
    return response

def list_files_s3( args ):
    """ Lists files under a given S3 path.
    path: S3 path
    pattern: file patterns to include ('*.fastq')
    excludepattern: file patterns to exclude ('*.log')
        - patterns can be lists
    """
    s3path = args['path']
    includepattern = args['pattern'] if 'pattern' in args else ''
    excludepattern = args['excludepattern'] if 'excludepattern' in args else ''

    response = get_objects_s3( args )
    files = []

    if "Contents" in response:
        files = list(map(lambda x: str(x['Key']).split('/')[-1], response['Contents']))
        ## narrow down file list if we are searching for a specific file pattern
        if includepattern not in ['',[]] or excludepattern not in ['',[]]:
            files = filter_objects( dict(objects=files, pattern=includepattern, excludepattern=excludepattern))

    return files

def list_folders_s3( args ):
    """ Lists folders under a given S3 path.
    path: S3 path
    pattern: folder patterns to include ('sample*')
    excludepattern: folder patterns to exclude ('*log')
        - patterns can be lists
    """
    s3path = args['path']
    includepattern = args['pattern'] if 'pattern' in args else ''
    excludepattern = args['excludepattern'] if 'excludepattern' in args else ''

    response = get_objects_s3( args )
    files = []

    if "CommonPrefixes" in response:
        files = list(map(lambda x: str(x['Prefix']).strip('/').split('/')[-1]+'/', response['CommonPrefixes']))
        ## narrow down file list if we are searching for a specific file pattern
        if includepattern not in ['',[]] or excludepattern not in ['',[]]:
            files = filter_objects( dict(objects=files, pattern=includepattern, excludepattern=excludepattern))

    return files

def list_objects_s3( args ):
    """ Lists objects (files and folders) under a given S3 path.
    path: S3 path
    pattern: folder patterns to include ('sample*')
    excludepattern: folder patterns to exclude ('*log')
        - patterns can be lists

    >>> list_objects_s3( dict(path='s3://hubtenants/bioshed/', excludepattern='*user'))
    ['jira.pdf', 'readme.txt', 'test/', 'testuser1/', 'testuser2/']
    >>> list_objects_s3( dict(path='s3://hubtenants/bioshed/', excludepattern='testus*'))
    ['jira.pdf', 'readme.txt', 'guestuser/', 'test/']
    >>> list_objects_s3( dict(path='s3://hubtenants/bioshed/', excludepattern='test'))
    ['jira.pdf', 'readme.txt', 'guestuser/']
    >>> list_objects_s3( dict(path='s3://hubtenants/bioshed/', pattern='test'))
    ['test/', 'testuser1/', 'testuser2/']
    >>> list_objects_s3( dict(path='s3://hubtenants/bioshed/', pattern='testuser*'))
    ['testuser1/', 'testuser2/']
    >>> list_objects_s3( dict(path='s3://hubtenants/bioshed/', pattern='*testuser'))
    []
    """
    return list_files_s3( args ) + list_folders_s3( args )

def filter_objects( args ):
    """ Filter list of objects (files or folders) based on pattern

    objects: list of objects
    pattern: pattern of objects to include (e.g., '*.fastq')
    excludepattern: file patterns to exclude ('*.log')
        - patterns can be lists
    ---
    filtered_objects: list of objects after filtering

    """
    objects = args['objects']
    includepattern = args['pattern'] if 'pattern' in args else ''
    excludepattern = args['excludepattern'] if 'excludepattern' in args else ''

    objects = quick_utils.format_type(objects, 'list')
    includepattern = quick_utils.format_type(includepattern, 'list')
    excludepattern = quick_utils.format_type(excludepattern, 'list')

    filtered_objects = []

    if includepattern not in ['',[]]:
        for o in objects:
            for p in includepattern:
                if (p.startswith('*') and o.strip('/').endswith(p.strip('*'))) or \
                   (p.endswith('*') and o.strip('/').startswith(p.strip('*'))) or \
                   (p in o):
                    filtered_objects.append(o)
    elif excludepattern not in ['',[]]:
        for o in objects:
            for p in excludepattern:
                if p.startswith('*'):
                    if not o.strip('/').endswith(p.strip('*')):
                         filtered_objects.append(o)
                elif p.endswith('*'):
                    if not o.strip('/').startswith(p.strip('*')):
                         filtered_objects.append(o)
                else:
                    if p not in o:
                        filtered_objects.append(o)
    return filtered_objects



def get_json_object( s3paths ):
    """ Gets content of JSON files in S3, specified by S3 paths.
    s3paths: string of comma-delimited S3 paths to JSON files - 'obj1,obj2,...'
    returns: corresponding list of JSON content (ordered)
    """
    json_list = []
    s3paths_list = s3paths.split(',')
    for s3path in s3paths_list:
        bucket = s3path.split('/')[2]
        key = '/'.join(s3path.split('/')[3:])

        obj = s3.Object(bucket, key)
        data = obj.get()['Body'].read().decode('utf-8')
        json_data = json.loads(data)
        json_list.append(json_data)
    return json_list

def edit_json_object( s3path, pairs2search, pairs2update ):
    """ Updates an existing S3 JSON object with new pairs.
        pairs2search: list of key:value pairs to search for in JSON object [{key1:value1}, {key2: value2},...]
        pairs2update: matched list of key:value pairs to update in JSON object

    (before: [{"a": 1, "b": 2}, {"c": 3, "d": 4, "e": 5}, {"g": 6}, {"h": 8, "i": 9}] )
    >>> aws_s3_utils.edit_json_object('s3://bioshed-db/bioshed/test.json', [{"c": 3}, {"b": 2}], [{"e": 10}, {"j": 11}])
    {'ResponseMetadata': {'RequestId': 'NR3EHTBYPPNH677N', 'HostId': 'Jt08TAQT1BCJ2TFxncN/L5p39BImVU+0Aq+g7SSRp3ltRT2d0l6DQu+xiApplYXsFtbL9XmiBZQ=', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amz-id-2': 'Jt08TAQT1BCJ2TFxncN/L5p39BImVU+0Aq+g7SSRp3ltRT2d0l6DQu+xiApplYXsFtbL9XmiBZQ=', 'x-amz-request-id': 'NR3EHTBYPPNH677N', 'date': 'Thu, 11 Aug 2022 03:57:52 GMT', 'x-amz-version-id': 'u1w6fo3dG9LSnhlX6pw__dYp.drkQ5hZ', 'x-amz-server-side-encryption': 'AES256', 'etag': '"288cbe6243118f973884cfa2d8ed7aae"', 'server': 'AmazonS3', 'content-length': '0'}, 'RetryAttempts': 1}, 'ETag': '"288cbe6243118f973884cfa2d8ed7aae"', 'ServerSideEncryption': 'AES256', 'VersionId': 'u1w6fo3dG9LSnhlX6pw__dYp.drkQ5hZ'}
    (after: [{"a": 1, "b": 2, "j": 11}, {"c": 3, "d": 4, "e": 10}, {"g": 6}, {"h": 8, "i": 9}])
    """
    bucket = s3path.split('/')[2]
    key = '/'.join(s3path.split('/')[3:])
    # current JSON data in object
    json_data = get_json_object( s3path )[0]
    for i in range(0,len(pairs2search)):
        pair = pairs2search[i]
        k2search = list(pair.keys())[0]
        v2search = list(pair.values())[0]
        pair2update = pairs2update[i]
        k2replace = list(pair2update.keys())[0]
        v2replace = list(pair2update.values())[0]
        # now search for k:v pair in json_data - yes, this is O(n^2)
        for j in range(0,len(json_data)):
            json_entry = json_data[j]
            if k2search in json_entry and json_entry[k2search]==v2search:
                json_data[j][k2replace] = v2replace
                break
    response = s3_client.put_object( Body=json.dumps(json_data).encode(), Bucket=bucket, Key=key )
    return response


def add_to_json_object( s3path, newpairs ):
    """ Adds new key value pairs to an existing S3 JSON object

    (before: test.json = [])
    >>> aws_s3_utils.add_to_json_object( "s3://bioshed-db/bioshed/test.json", [{"a": 1, "b": 2}, {"c": 3, "d": 4, "e": 5}])
    {'ResponseMetadata': {'RequestId': 'M2D5NRA0C4XZA1C4', 'HostId': 'tP75NO30/io8AtwCBSI/hkQLytdAQhF8AzQ/cCaPxwy7E+SnBd9dJ9Qw08WsBrV/KJJN8ZU3ZPo=', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amz-id-2': 'tP75NO30/io8AtwCBSI/hkQLytdAQhF8AzQ/cCaPxwy7E+SnBd9dJ9Qw08WsBrV/KJJN8ZU3ZPo=', 'x-amz-request-id': 'M2D5NRA0C4XZA1C4', 'date': 'Wed, 10 Aug 2022 23:55:21 GMT', 'x-amz-version-id': '5t9dAbPxN5mWnerG3s1BkOo_KRXJTriT', 'x-amz-server-side-encryption': 'AES256', 'etag': '"818ed2e3dd0b1c240fe0a3cdce52c7d6"', 'server': 'AmazonS3', 'content-length': '0'}, 'RetryAttempts': 1}, 'ETag': '"818ed2e3dd0b1c240fe0a3cdce52c7d6"', 'ServerSideEncryption': 'AES256', 'VersionId': '5t9dAbPxN5mWnerG3s1BkOo_KRXJTriT'}
    (after: test.json = [{"a": 1, "b": 2}, {"c": 3, "d": 4, "e": 5}])
    """
    bucket = s3path.split('/')[2]
    key = '/'.join(s3path.split('/')[3:])
    json_data = get_json_object( s3path )[0]
    # if json_data is itself a list, we can just append. Otherwise we add key by key.
    if type(json_data) == type([]):
        for newpair in newpairs:
            json_data.append( newpair )
    elif type(json_data) == type({}):
        for k, v in newpairs.items():
            if k not in json_data:
                json_data[k] = v

    response = s3_client.put_object( Body=json.dumps(json_data).encode(), Bucket=bucket, Key=key )
    return response



def list_objects_nested( s3path, searchpattern ):
    """ Similar to list_objects but will list objects in nested subfolders
    Nested subfolders are found in the "CommonPrefixes" key:
    {
    "CommonPrefixes": [
        {
            "Prefix": "bioshed/guestuser/"
        },
        {
            "Prefix": "bioshed/test/"
        },...
        ]
    }
    """

    return

def get_metadata( s3paths ):
    """ Gets metadata for objects (files or folders) at the given S3 paths (string-list)
    s3paths: string of comma-delimited S3 paths - 'obj1,obj2,...'
    returns: corresponding list of tags
    """
    metadata_list = []
    s3paths_list = s3paths.split(',')
    for s3path in s3paths_list:
        bucket = s3path.split('/')[2]
        key = '/'.join(s3path.split('/')[3:])
        response = s3_client.get_object_tagging(Bucket=bucket,Key=key)
        if 'TagSet' in response:
            metadata = response['TagSet']
        else:
            metadata = {}
        metadata_list.append( metadata )
    return metadata_list

def set_metadata( s3paths, tags_dict, overwrite = 'True' ):
    """ Sets metadata for objects (files or folders) at the given S3 paths as the passed in tags.
        If tags exist, it overwrites if overwrite = True (default).
        Currently, can have up to 10 tags.
        All objects will get the same tags.

        s3paths: string of comma-delimited objects in S3 - 'obj1,obj2,...'
        tags_dict: DICT - e.g., {'project': 'epigenome', 'id': 'ID-01', 'tissue': 'heart'}
        returns: set tags (list)
    """
    def getCurrentTag( k, tags ):
        """ List of tags format as [{'Key': k, 'Value': v}, {'Key2': k2, 'Value2': v2},...]
            return value for key k
        """
        for t in tags:
            if k == t['Key']:
                return t
        return {}

    tag_sets = []
    s3paths_list = s3paths.split(',')
    for s3path in s3paths_list:
        bucket = s3path.split('/')[2]
        key = '/'.join(s3path.split('/')[3:])
        # get the current tags, and only overwrite if overwrite = True
        current_tags = get_metadata( s3path )[0]
        tag_set = []
        for k, v in tags_dict.items():
            new_tag = {'Key': k, 'Value': v}
            # only overwrite if we specify so, or if tag key does not exist
            if overwrite[0].upper()=='T' or (k not in list(map(lambda kv: kv['Key'], current_tags))):
                tag_set.append(new_tag)
            else:
                # otherwise keep the current tag
                current_tag = getCurrentTag( k, current_tags )
                tag_set.append( current_tag )
        # update metadata for S3 object
        response = s3_client.put_object_tagging(Bucket=bucket,Key=key, Tagging={'TagSet': tag_set})
        tag_sets.append(tag_set)
    return tag_sets

def dateConverter(json_object):
    """ AWS response objects often contain datetime objects.
    For proper JSON stringify, need to convert these datetime objects to string date format.
    """
    if isinstance(json_object, datetime.datetime):
        return json_object.__str__()

####### LEGACY FUNCTIONS (for compatibility) #######
def downloadFile_S3(s3path, dir_to_download):
    return download_file_s3( dict(path=s3path, localdir=dir_to_download))

def downloadFiles_S3(s3paths, dir_to_download):
    return download_file_s3( dict(path=s3paths, localdir=dir_to_download))

def downloadFolder_S3(s3path, localdir):
    return download_folder_s3( dict(path=s3path, localdir=localdir))

def downloadFiles_Pattern_S3(s3_path, directory_to_download, pattern):
    return download_folder_s3( dict(path=s3_path, localdir=directory_to_download, pattern=pattern))

def uploadFile_S3(localfile, s3path):
    return upload_file( dict(path=s3path, localfile=localfile))

def uploadFiles_S3(localfiles, s3path):
    return upload_file( dict(path=s3path, localfile=localfiles))

def uploadFolder_S3(localdir, s3path, files2exclude = ''):
    return upload_folder_s3( dict(path=s3path, localdir=localdir, pattern=files2exclude))

def listSubFiles(s3_path, patterns2include, patterns2exclude):
    """
    Lists files from S3 that match a specific pattern
    :param s3_path: s3 folder path
    :param patterns2include: LIST of file patterns to search for.
    :param patterns2exclude: LIST of file patterns to exclude.
    :return: found files matching pattern

    patterns follow this notation: e.g., ['^.bam', 'hepg2^', 'I1'] where
                 '^.bam' => file ends with BAM
                 'hepg2^' => file begins with hepg2
                 '^fastq^' => file contains fastq in file extension (sep from base file name by [-,_,.]: e.g., myfile.fastq.gz
                 'I1' => file contains the word I1 anywhere

    >>> listSubFiles('s3://hubpublicinternal/test/aws_s3_utils/', 'test', 'R1')
    ['test-R2.fastq.gz', 'test-upload-R2.fastq.gz', 'test-upload.create_fastq.log', 'test.create_fastq.log']
    >>> listSubFiles('s3://hubpublicinternal/test/aws_s3_utils/', 'test', ['^R1^','^R2^'])
    ['test-upload.create_fastq.log', 'test.create_fastq.log']
    """
    if type(patterns2include) == str:
        patterns2include = [patterns2include]
    if type(patterns2exclude) == str:
        patterns2exclude = [patterns2exclude]

    if type(s3_path) == type([]) and s3_path != []:
        s3_path = s3_path[0]
    elif type(s3_path) == type([]) and s3_path == []:
        s3_path = ''

    cmd = 'aws s3 ls %s' % (s3_path.rstrip('/')+'/')
    dfiles = []
    uid = str(uuid.uuid4())[0:6]  # prevents race conditions on tmp file
    # output of S3 copy to temporary file
    try:
        # I think calledprocesserror will be called if file not found
        with open(uid+'_dfilestmptmp.tmp','w') as fout:
            subprocess.check_call(cmd.split(' '), stdout=fout)
        # get a list of all downloaded files
        with open(uid+'_dfilestmptmp.tmp','r') as f:
            for r in f:
                rp = r.split(' ')[-1].lstrip(' \t').rstrip(' \t\n')
                # '.' indicates its a file
                if '.' in rp and _findMatches(rp, patterns2include) and not (patterns2exclude != [] and _findMatches(rp, patterns2exclude)):
                    dfiles.append(rp)

        # remove temporary file
        rm_command = ['rm',uid+'_dfilestmptmp.tmp']
        subprocess.check_call(rm_command)
    except subprocess.CalledProcessError:
        print('CALLED PROCESS ERROR in aws_s3_utils.listSubFiles() or FILES NOT FOUND')
        if os.path.exists(uid+'_dfilestmptmp.tmp'):
            rm_command = ['rm',uid+'_dfilestmptmp.tmp']
            subprocess.check_call(rm_command)
        return []
    return dfiles

def _filter_list_objects_response( response, search_pattern ):
    """ private function
    Narrow down file list response object if we are searching for a specific file pattern
    """
    files2remove = []
    for file_info in response["Contents"]:
        if "Key" in file_info and search_pattern not in file_info["Key"]:
            files2remove.append(file_info)
    for file2remove in files2remove:
        response["Contents"].remove(file2remove)
    return response


def list_objects( s3path, searchpattern = '' ):
    """ List objects in an S3 object path. Returns a JSON response with format:
      {'ResponseMetadata':
         {'RequestId': ...,
          'HostId': ...
          'HTTPStatusCode': 200,
          'HTTPHeaders': ...
          'IsTruncated': False,
          'Contents':
            [{'Key': '<filename>' 'LastModified': ...', 'Size': '...'...},
             {'Key': '...
            ]
         }}}

    searchpattern: only include files that contain the passed searched pattern (optional)

    example of returned file info:
    {"Contents": [
        {
            "Key": "bioshed/jira.pdf",
            "LastModified": "2022-07-27 23:11:22+00:00",
            "ETag": "\"46213a6178ac104ba811cc5bb0133218\"",
            "Size": 159226,
            "StorageClass": "STANDARD"
        },...
    ]}
    """
    bucket = s3path.split('/')[2]
    key = str('/'.join(s3path.split('/')[3:])).rstrip('/') + '/'
    region = AWS_CONFIG['aws_region']
    # s3_endpoint = '{}.s3.{}.amazonaws.com/{}'.format(bucket,region,key)
    response = s3_client.list_objects_v2( Bucket=bucket, Prefix=key, Delimiter='/', StartAfter=key )
    ## narrow down file list if we are searching for a specific file pattern
    if searchpattern != '' and "Contents" in response:
        return _filter_list_objects_response( response, searchpattern )
    else:
        return response

def listSubFolders(s3_path, folders2include = [], folders2exclude = [], options = ''):
    """ Lists all immediate subfolders under a given S3 path.
    :param s3_path: s3 folder path
    :param folders2include: LIST, if specified, only include these folders
    :param folders2exclude: LIST of folders to exclude
    :param options: options to include with ls call
    :return: found subfolders
    >>> listSubFolders('s3://hubpublicinternal/test/', ['aws_s3_utils'])
    ['aws_s3_utils']
    """
    if type(s3_path) == type([]) and s3_path != []:
        s3_path = s3_path[0]
    elif type(s3_path) == type([]) and s3_path == []:
        s3_path = ''
    cmd = 'aws s3 ls {} {}'.format(options, (s3_path.rstrip('/')+'/'))
    dfolders = []
    uid = str(uuid.uuid4())[0:6]  # prevents race conditions on tmp file
    try:
        fout = open(uid+'_dfolderstmptmp.tmp','w')
        subprocess.check_call(cmd.split(' '), stdout=fout)
        fout.close()
        with open(uid+'_dfolderstmptmp.tmp','r') as f:
            for r in f:
                rp = r.lstrip(' \t').rstrip(' \t\n')
                if rp.startswith('PRE'):  # tags a folder - hopefully this doesn't change on AWS side with aws s3 ls
                    folder = rp.split(' ')[1].rstrip('/')
                    if (folder not in folders2exclude) and (folders2include == [] or folder in folders2include):
                        dfolders.append(folder)

        # remove temporary file
        rm_command = ['rm',uid+'_dfolderstmptmp.tmp']
        subprocess.check_call(rm_command)
        return dfolders
    except subprocess.CalledProcessError:
        return []
