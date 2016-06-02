#! /usr/bin/python
'''
Simple Python Utilities to check details from Mantl for deploying apps.

Supported Tasks:
# TODO UPDATE THIS LIST
  ./tropo_utils.py numbercheck <prefix>
    - See if there are available numbers for a given prefix
  ./tropo_utils.py applicationcheck <application name>
    - See if there is already a created application of a given name
  ./tropo_utils.py listprefixes <count>
    - Return a list of supported prefixes
'''


import urllib2, json, sys, os, ssl, base64

# Marathon Utilities
def get_marathon_applications():
    u = marathon_host + "/v2/apps"

    # create_urlopener(u, mantl_user, mantl_password)

    req = urllib2.Request(u)
    req.add_header("Authorization", authheader)
    output = urllib2.urlopen(req, context=ctx)
    apps = json.loads(output.read())
    return apps['apps']

def get_marathon_application(appname):
    u = marathon_host + "/v2/apps/%s" % (appname)

    try:
        req = urllib2.Request(u)
        req.add_header("Authorization", authheader)
        output = urllib2.urlopen(req, context=ctx)
        apps = json.loads(output.read())
        return apps
    except urllib2.HTTPError:
        return False

# Utility Functions
def chelp():
    print("Supported Commands are:")
    print("\tnumbercheck <prefix>")
    print("\tapplicationcheck <application name>")
    print("\tlistprefixes <count>")

def create_urlopener(host, user, password):
    authinfo = urllib2.HTTPPasswordMgrWithDefaultRealm()
    authinfo.add_password(None, host, user, password)
    handler = urllib2.HTTPBasicAuthHandler(authinfo)
    myopener = urllib2.build_opener(handler)
    opened = urllib2.install_opener(myopener)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

try:
    mantl_control = os.environ["MANTL_CONTROL"]
    mantl_user = os.environ["MANTL_USER"]
    mantl_password = os.environ["MANTL_PASSWORD"]
    mantl_domain = os.environ["MANTL_DOMAIN"]
    deployment_name = os.environ["DEPLOYMENT_NAME"]
    command = sys.argv[1]
    input = sys.argv[2]
except:
    print("Command takes 2 parameters.  First is the command, second is the input to command.")
    chelp()
    sys.exit(1)

marathon_host = "https://%s:8080" % (mantl_control)
base64string = base64.encodestring('%s:%s' % (mantl_user, mantl_password)).replace('\n', '')
authheader =  "Basic %s" % base64string

if command == "applicationexists":
    if get_marathon_application(input):
        sys.exit(0)
    else:
        sys.exit(1)
else:
    print("Command Not Understood.")
    chelp()
