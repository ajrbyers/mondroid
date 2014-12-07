from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
import models

def create_many_states(monitor, starting_at=None, number=10, offset=5, up=True, status_code=200, elapsed_time='0.1'):
    if not starting_at:
        starting_at = timezone.now()
    for i in range(1, number + 1):
        c = models.Check(**{
            'monitor': monitor,
            'status_code': status_code,
            'history': '[]',
            'elapsed_time': elapsed_time,
            'up': up,
            
            'capture': starting_at - timedelta(minutes=offset * i)
        })
        c.save()
        print 'created %r' % c

    return c # the last one created

class MonitorLogic(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_monitors_time_in_current_state(self):
        m = models.Monitor(name='foo', url='http://example.org')
        m.save()
        last_c = create_many_states(m, number=10, up=True)
        last_c = create_many_states(m, number=5, up=False, starting_at=last_c.capture)
        last_c = create_many_states(m, number=10, up=True, starting_at=last_c.capture)
        #print m.check_set.all()[:]
        
        
