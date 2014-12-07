from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
import models
import logic

def create_many_states(monitor, starting_at=None, number=10, offset=5, up=True, status_code=200, elapsed_time='0.1'):
    if not starting_at:
        starting_at = timezone.now()
    ch = []
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
        ch.append(c)
        #print "%r" % c
    return ch

class MonitorLogic(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_monitors_time_in_current_state(self):
        m = models.Monitor(name='foo', url='http://example.org')
        m.save()
        ch1 = create_many_states(m, number=10, up=True)
        ch2 = create_many_states(m, number=5, up=False, starting_at=ch1[-1].capture)
        self.assertEqual(m.time_in_state().seconds, (timezone.now() - ch2[0].capture).seconds)

    def test_monitor_grouping(self):
        m = models.Monitor(name='foo', url='http://example.org')
        m.save()
        ch1 = create_many_states(m, number=6, up=True)
        ch2 = create_many_states(m, number=5, up=False, starting_at=ch1[-1].capture)
        ch3 = create_many_states(m, number=4, up=True, starting_at=ch2[-1].capture)
        ch4 = create_many_states(m, number=3, up=False, starting_at=ch3[-1].capture)
        ch5 = create_many_states(m, number=2, up=True, starting_at=ch4[-1].capture)
        self.assertEqual(logic.chunked_history1(m), [ch1, ch2, ch3, ch4, ch5])

    def test_monitor_grouping_filtered(self):
        "test that the chunked_history1 function filters by it's arguments correctly"
        m = models.Monitor(name='foo', url='http://example.org')
        m.save()
        ch1 = create_many_states(m, number=6, up=True)
        ch2 = create_many_states(m, number=5, up=False, starting_at=ch1[-1].capture)
        ch3 = create_many_states(m, number=4, up=True, starting_at=ch2[-1].capture)
        ch4 = create_many_states(m, number=3, up=False, starting_at=ch3[-1].capture)
        ch5 = create_many_states(m, number=2, up=True, starting_at=ch4[-1].capture)
        self.assertEqual(logic.chunked_history1(m, capture__gte=ch3[-1].capture), [ch1, ch2, ch3])
