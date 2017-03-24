import opc_imp as opc
from layout_handler import LayoutHandler
import random
import time
from visual_algos.throbber import Throbber
# from visual_algos.bar_graph import BarGrapher
from slacker import SlackJenkinsWatcher
sleep_base_interval = 1.0 / 20


def random_color(mv=10):
    r = random.randint(0, mv)
    g = random.randint(0, mv)
    b = random.randint(0, mv)
    return (r, g, b)


x1 = LayoutHandler('../openpixelcontrol/layouts/concircs.json')

s1 = x1.get_strand_element('s1')
b1 = x1.get_banner_element('b1')
c1 = x1.get_conrings_element('c1')
s2 = x1.get_strand_element('s2')
# s2_throb = Throbber(s2)
# s1_bar = BarGrapher(s1, bar_cb)
c1_throb = Throbber(c1)

client = opc.Client('buildspy.local:7890')
b1.set_scroll_text('loading')

slack_client = SlackJenkinsWatcher()

cl = 10
unknown_color = (cl, cl, cl)
running_color = (0, 0, cl)
failed_color = (cl, 0, 0)
success_color = (0, cl, 0)
use_color = unknown_color


while True:
    current_status = slack_client.get_current_status()
    if current_status.was_updated:
        b1.set_scroll_text(current_status.panel_text)
        if current_status.is_unknown:
            use_color = unknown_color
        elif current_status.is_running:
            use_color = running_color
        elif current_status.is_failed:
            use_color = failed_color
        else:
            assert current_status.is_success, \
                'not unknown, not running, not failed. why was it not success!!!'
            use_color = success_color
    start_proc_time = time.time()
    b1.tick(use_color)
    c1_throb.tick()
    x1.render(client)
    end_proc_time = time.time()
    ran_time = end_proc_time - start_proc_time
    if ran_time > sleep_base_interval:
        # print "WARNING: proced for {} but sleep is only {}".format(ran_time, sleep_base_interval)
        pass
    else:
        # time.sleep(sleep_base_interval - ran_time)
        time.sleep(0.1)
        pass
