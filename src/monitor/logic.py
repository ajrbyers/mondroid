from django.template.loader import get_template
from django.template import Context
from django.utils import timezone
import models

def render_email_content(up, outage):
	return get_template('email/end.html' if up else 'email/start.html').render(
        Context({
            'outage': outage,
        })
    )

def chunklist(somelist, splitter):
    prevobj = None
    objlist = []
    for obj in somelist:
        if splitter(obj) != splitter(prevobj):
            # current object is different from previous
            # start a new group
            objlist.append([])
        objlist[-1].append(obj)
        prevobj = obj
    return objlist

def chunked_history1(monitor):
    splitter = lambda obj: getattr(obj, 'up', None)
    return chunklist(models.Check.objects.all(), splitter)

def chunked_history2(monitor):
    # TODO: a recursive version of Monitor.time_in_state jumping
    # through history would be interesting. More queries, but 
    # the opportunity to do it lazily and forever - Luke
    pass
