from django.template.loader import get_template
from django.template import Context
from django.utils import timezone
import models

from datetime import timedelta

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

def chunked_history1(m, *args, **kwargs):
    splitter = lambda obj: getattr(obj, 'up', None)
    return chunklist(m.check_set.filter(*args, **kwargs), splitter)

def chunked_history2(monitor):
    # TODO: a recursive version of Monitor.time_in_state jumping
    # through history would be interesting. More queries, but 
    # the opportunity to do it lazily and forever - Luke
    pass

def average_latency(history_list):
    "returns the average latency for the Check objects in the given history_list in milliseconds"
    def safe_float(string):
        try:
            if ':' in string: # looks like 0:00:01.342342
                string = string[5:]
            return float(string)
        except ValueError:
            return 0.0
    floats = map(lambda c: safe_float(c.elapsed_time), history_list)
    return int((sum(floats) / len(floats)) * 1000)

def summarise_history(grouped_history):
    "takes a grouped history list as output by chunked_history and returns the min and max of each group"
    x = []
    for group in grouped_history:
        span = (group[0], group[-1])
        x.append({
            "span_struct": span,
            "start": span[-1], # we're going backwards in time
            "end": span[0],
            "span": span[0].capture - span[1].capture,
            "up": span[0].up_or_down(),
            "avg_latency": "%sms" % average_latency(group),
        })
    return x

def uptime(monitor):
    twenty_four_hours = timezone.now() - timedelta(hours=24)
    last_week = timezone.now() - timedelta(days=7)
    last_month = timezone.now() - timedelta(days=28)
    last_year = timezone.now() - timedelta(days=365)

    uptime_dict = {
        'tfh_history': summarise_history(chunked_history1(monitor, capture__gte=twenty_four_hours)),
        'lw_history': summarise_history(chunked_history1(monitor, capture__gte=last_week)),
        'lm_history': summarise_history(chunked_history1(monitor, capture__gte=last_month)),
        'ly_history': summarise_history(chunked_history1(monitor, capture__gte=last_year)),
    }

    results = {}
    for k, v in uptime_dict.iteritems():
        down = timedelta()
        up = timedelta()
        for status_span in uptime_dict[k]:
            if status_span.get('up') == 'up':
                up += status_span.get('span')
            elif status_span.get('up') == 'down':
                down += status_span.get('span')

        total = up.total_seconds() + down.total_seconds()
        results[k] = (up.total_seconds() / total) * 100

    return results



