import os, sys, subprocess, json, requests

def format_type( foo, ftype ):
    """
    foo: string or list to format
    ftype: type to format to
    ---
    modfoo: formatted based on desired format type
    """
    if (foo=='' and ftype.lower() in ['list','array']):
        modfoo = []
    elif (type(foo)==type([]) and ftype.lower() in ['space-str', 'space_string', 'string_space']):
        modfoo = ' '.join(foo)
    elif (type(foo)==type([]) and ftype.lower() in ['list','array']) or \
       (type(foo)==type('') and ftype.lower()[0:3]=='str'):
        modfoo = foo
    elif (type(foo)==type([]) and ftype.lower()[0:3]=='str'):
        modfoo = ','.join(foo)
    elif (type(foo)==type('') and ',' in foo and ftype.lower() in ['list','array']):
        modfoo = list(map(lambda x: x.strip(), foo.split(',')))
    elif (type(foo)==type('') and ftype.lower() in ['list','array']):
        modfoo = list(map(lambda x: x.strip(), foo.split(' ')))
    else:
        modfoo = foo
    return modfoo

def args_to_list( args, delim=','):
    """ Converts delimited args to a list
    """
    if type(args)==type(''):
        pargs = args.split(delim)
    elif type(args)==type([]):
        pargs = args
    else:
        pargs = []
    return pargs


def get_file_only( file_fullpath ):
    """ Gets the file only from a full file path
    Note that this assumes that a file has a '.' extension!
    >>> getFileOnly( '/this/is/a/path/to.txt' )
    'to.txt'
    >>> getFileOnly( '/this/is/a/path' )
    ''
    >>> getFileOnly( '/this/is/a/path/' )
    ''
    """
    if type(file_fullpath) == type([]):
        files_only = []
        for f in file_fullpath:
            files_only.append(f.split('/')[-1] if '.' in f.split('/')[-1] else '')
    elif type(file_fullpath) == type(''):
        files_only = file_fullpath.split('/')[-1] if '.' in file_fullpath.split('/')[-1] else ''
    else:
        files_only = ''
    return files_only

def get_file_folder( file_fullpath ):
    """ Gets folder path from a full file path
    >>> getFileFolder( '/this/is/a/path' )
    '/this/is/a/path/'
    >>> getFileFolder( '/this/is/a/path/' )
    '/this/is/a/path/'
    >>> getFileFolder( '/this/is/a/path/to.txt' )
    '/this/is/a/path/'
    >>> getFileFolder( ['/this/is/a/path/to.txt'] )
    '/this/is/a/path/'
    """
    if type(file_fullpath) == type([]) and file_fullpath != []:
        # get directory of first file
        if '.' in file_fullpath[0].split('/')[-1]:
            # if file is specified at end
            folders_only = file_fullpath[0][0:file_fullpath[0].rfind('/')]+'/'
        else:
            # if just folder path is passed
            folders_only = file_fullpath[0].rstrip('/')+'/'
    elif type(file_fullpath) == type(''):
        if '.' in file_fullpath.split('/')[-1]:
            folders_only = file_fullpath[0:file_fullpath.rfind('/')]+'/'
        else:
            folders_only = file_fullpath.rstrip('/')+'/'
    else:
        folders_only = ''
    return folders_only

def infer_file_system( filepath ):
    """ Accepts a single string or a list of filepaths. If list, all filepaths must be the same filesystem.
    RETURN: filesystem ('s3', 'local')

    >>> inferFileSystem( 's3://hubpublicinternal/')
    's3'
    >>> inferFileSystem( '/bed/my.bed' )
    'local'
    >>> inferFileSystem( ['s3://hubpublicinternal/', 's3://test/'] )
    's3'
    """
    fs = 'local'  # default is local
    if type(filepath) == list or type(filepath) == tuple:
        for f in filepath:
            if f == '' or type(f) != str:
                pass
            elif f.startswith('s3:/') or ('amazon' in f and 'aws' in f and 's3' in f):
                fs = 's3'
                break
            else:
                fs = 'local'
                break
    elif type(filepath) == str:
        if filepath.startswith('s3:/') or ('amazon' in filepath and 'aws' in filepath and 's3' in filepath):
            fs = 's3'
        else:
            fs = 'local'
    return fs

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

def add_to_json( fname, jsonadd ):
    if os.path.exists(fname):
        jsonog = loadJSON( fname )
    else:
        jsonog = {}
    for k in jsonadd:
        jsonog[k] = jsonadd[k]
    return writeJSON( jsonog, fname )

def get_request( args ):
    """ HTTP GET request.
    url: URL to GET
    type: application type - default: */*. Options include 'application/json'...
    ---
    response
    """
    myurl = args['url']
    apptype = args['type'] if 'type' in args else '*/*'
    headers = {'accept': apptype}

    response = requests.get(myurl, headers=headers)
    if apptype == 'application/json':
        return response.json()
    else:
        return response

def post_request( args ):
    """ HTTP POST request.
    url: URL to POST to (required)
    headers: headers (optional)
    body: body
    ---
    response
    """
    myurl = args['url']
    headers = args['headers'] if 'headers' in args else {}
    body = args['body'] if 'body' in args else {}

    if headers != {}:
        response = requests.post(myurl, json=body, headers=headers)
    else:
        response = requests.post(myurl, json=body)
    return json.loads(response.content)

def file_exists( f ):
    """ Check if a file exists in local system
    """
    if os.path.exists( f ):
        return True
    else:
        return False
