import opc_imp as opc
from layout_handler import LayoutHandler
import random
import os
import re
from visual_algos.throbber import Throbber
from visual_algos.bar_graph import BarGrapher
import subprocess


def random_color(mv=10):
    r = random.randint(0,mv)
    g = random.randint(0,mv)
    b = random.randint(0,mv)
    return (r, g, b)

x1 = LayoutHandler('../openpixelcontrol/layouts/concircs.json')
import time

def bar_cb():
    """
    on os-x: CPU usage: 10.93% user, 23.43% sys, 65.62% idle

    """
    return random_color(120)
    top_data = subprocess.check_output(['top', '-n', '0', '-l', '1'])
    retx = r'''(?P<user>\d+.\d+)%\s+user,\s+
               (?P<sys>\d+.\d+)%\s+sys,\s+
               (?P<idle>\d+.\d+)%\s+idle'''
    m = re.search(retx, top_data, re.VERBOSE)
    assert m is not None, 'failed on {}'.top_data
    u = float(m.group("user"))
    s = float(m.group("sys"))
    i = float(m.group("idle"))
    return (u, s, i)

s1 = x1.get_strand_element('s1')
b1 = x1.get_banner_element('b1')
c1 = x1.get_conrings_element('c1')
s2 = x1.get_strand_element('s2')
r1 = x1.get_raw_space()
s2_throb = Throbber(s2)
s1_bar = BarGrapher(s1, bar_cb)
c1_throb = Throbber(c1)
client = opc.Client('localhost:7890')
#b1.set_char('C', 0, 0)
b1.set_scroll_text('IloveDELL')
bx = 0
by = 0
lx = 0
ly = 0
what = 'all'
sleep_base_interval = 1.0 / 20

while True:
    if what == 'all':
        start_proc_time = time.time()
        rc = random_color()
        b1.tick(rc)
        s1_bar.tick()
        s2_throb.tick()
        c1_throb.tick()
        x1.render(client)
        end_proc_time = time.time()
        ran_time = end_proc_time - start_proc_time
        if ran_time > sleep_base_interval:
            print "WARNING: proced for {} but sleep is only {}".format(ran_time, sleep_base_interval)
        else:
            #time.sleep(sleep_base_interval - ran_time)
            time.sleep(0.1)
            pass
    elif what == 'tick':
        w = (64,64,64)
        b = (0,0,0)
        x = 0
        run_list = [b1, s1, s2, c1]
        ts = 0.2
        for r in run_list:
            x = 0
            print r.name, r.length
            while x < r.length:
                r.set_pixel(x, w)
                if x > 0:
                    r.set_pixel(x-1, b)
                x1.render(client)
                x += 1
                if ts > 0:
                    #print "now on {}".format(x)
                    time.sleep(ts)
                else:
                    raw_input(" return to move to {}".format(x))
    elif what == 'banner':
        rc = random_color()
        b1.set_pixel(0, (255, 255, 255))
        x1.render(client)
        print b1.start
        raw_input("return to scroll a line")
        for col in range(0, 32):
            b1.set_char('!', col)
            x1.render(client)
            raw_input("return to scroll a line")
        
