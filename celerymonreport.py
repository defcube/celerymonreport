#!/usr/bin/env python
from gattlib.safeurllib import safeurlopen
import json
import math

def load_report(url):
    rawdata = safeurlopen(url)
    data = json.loads(rawdata)
    r = {}
    ignoredcnt = 0
    for row in data:
        rowd = row[1]
        if not rowd['started']:
            continue
        if not rowd['name']:
            ignoredcnt += 1
            continue
        rowr = r.setdefault(rowd['name'], {'executions': []})
        rowr['executions'].append(rowd['runtime'])
    items = r.items()
    items.sort(key=lambda x: sum(x[1]['executions']), reverse=True)
    for k, d in items:
        executions = d['executions']
        mean = float(sum(executions)) / len(executions)
        maximum = max(executions)
        print "{0}: {1} executions. Average: {2} Max: {3} "\
              .format(k, len(executions), mean, maximum)
    print "Ignored {0} messages".format(ignoredcnt)

if __name__ == '__main__':
    import optparse
    parser = optparse.OptionParser()
    (options, args) = parser.parse_args()
    if len(args) == 0:
        path = ""
        while not path:
            path = raw_input("What is the url? ").strip()
    elif len(args) != 1:
        print "You must specify the URL for the celerymon data"
        exit()
    else:
        path = args[0]
    load_report(path)
    
