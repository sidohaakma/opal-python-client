"""
Opal Entity.
"""

import sys
import opal.core

def add_arguments(parser):
  """
  Add variable command specific options
  """
  parser.add_argument('id', help='Id of the entity.')
  parser.add_argument('--type', '-ty', required=False, help='Type of entity. Default type is Participant')
  parser.add_argument('--tables', '-ta', action='store_true', help='Get the list of tables in which the entity with given id exists.')

def do_ws(args):
    """
    Build the web service resource path
    """
    ws = '/entity/';
    if args.id:
        ws = ws + args.id + '/type/'
        if args.type:
            ws = ws + args.type
        else:
            ws = ws + 'Participant'

        if args.tables:
            ws = ws + '/tables'

    print ws
    return ws

def do_command(args):
    """
    Execute data command
    """
    # Build and send request
    try:
        request = opal.core.OpalClient(args).new_request()
        request.fail_on_error().accept_json()

        if args.verbose:
            request.verbose()

        # send request
        response = request.get().resource(do_ws(args)).send()

        # format response
        res = response.content
        if args.tables:
            res = response.pretty_json()

        # output to stdout
        print res
    except Exception,e :
        print e
        sys.exit(2)
    except pycurl.error, error:
        errno, errstr = error
        print >> sys.stderr, 'An error occurred: ', errstr
        sys.exit(2)