#!/usr/bin/env python

import beanstalkc
import daemon
from django.core.management import setup_environ

import os
import sys
project_dir = os.path.dirname(os.path.abspath(os.path.basename(__file__)))
sys.path.append(project_dir)
import settings
setup_environ(settings)
from feeds.tools import populate_feed
from feeds.models import Feed

log = open('probe.log', 'w+')
def out(msg):
    log.write('%s\n' % msg)

def probe():
    beanstalk = beanstalkc.Connection()
    # log.close()
    while True:
        out("Waiting for job...")
        job = beanstalk.reserve()
        out("Job found")
        try:
            feed = Feed.objects.get(slug=job.body)
        except Feed.DoesNotExist:
            out('cannot find feed: %s\n' % job.body)
        else:
            list(populate_feed(feed))
            out('updated %s\n' % feed)
        job.delete()
        log.flush()

context = daemon.DaemonContext(working_directory=settings.PROJECT_PATH,
                              stderr=open('errors.log', 'w+'))
# with context:
probe()
