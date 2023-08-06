import sys, os, json
import aws_s3_utils

### supersedes aws_s3_utils and other file utils scripts. ###

def writeJSON( myjson, fout_name ):
    """ Writes (dumps) a JSON as a string to a file.
    """
    with open(fout_name,'w') as fout:
        json.dump(myjson, fout)
    return fout_name

def getJSON( fname ):
    return loadJSON(fname)

def loadJSON( fname ):
    """ Loads JSON from file named 'fname' into a JSON object and return this object.

    >>> loadJSON( "foo.json" )
    JSON ERROR - JSON NOT FORMATTED CORRECTLY OR FILE NOT FOUND: [Errno 2] No such file or directory: 'foo.json'
    {}
    """
    try:
        if type(fname) == type([]):
            fname = fname[0] if fname != [] else ''
        with open(fname,'r') as f:
            myjson = json.load(f)
    except Exception as e:
        print('JSON ERROR - JSON NOT FORMATTED CORRECTLY OR FILE NOT FOUND: '+str(fname))
        return {}
    return myjson

def save_files( args ):
    """ Saves local files to a cloud storage provider.

    files: list of files
    path: cloud storage path
    """
    files = args['files']
    cloudpath = args['path']

    if cloudpath.startswith('s3://'):
        for f in files:
            aws_s3_utils.upload_file_s3( dict(localfile=f, path=cloudpath))
    return
