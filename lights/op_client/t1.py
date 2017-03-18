import opc_imp as opc
from layout_handler import LayoutHandler
import random
import os
import re
from visual_algos.throbber import Throbber
from visual_algos.bar_graph import BarGrapher
import subprocess


def random_color(mv=255):
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
    return random_color(100)
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
s2_throb = Throbber(s2)
s1_bar = BarGrapher(s1, bar_cb)
c1_throb = Throbber(c1)
client = opc.Client('localhost:7890')
b1.set_char('C', 0, 0)
b1.set_scroll_text('abcdefghijklmnop hello Derrick')
bx = 0
by = 0
lx = 0
ly = 0
while True:
    rc = random_color()
    b1.tick(rc)
    s1_bar.tick()
    s2_throb.tick()
    c1_throb.tick()
    x1.render(client)
    time.sleep(1.0/100)
