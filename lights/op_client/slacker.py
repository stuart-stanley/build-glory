import os
import time
import logging
from slackclient import SlackClient


FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logs = logging.getLogger(__name__)
logs.setLevel(logging.INFO)
_fm = logging.Formatter(FORMAT)
_ch = logging.StreamHandler()
_ch.setLevel(logging.DEBUG)
_ch.setFormatter(_fm)
logs.addHandler(_ch)


class _AStatus(object):
    def __init__(self, event):
        self.was_updated = True
        base_info = {
            'name': None,
            'phase': None,
            'status': None,
            'queue_id': 'UNKNOWN'
        }
        if event is None:
            base_info['name'] = 'MasterCI'
            base_info['phase'] = 'UNKNOWN'
            base_info['status'] = 'UNKNOWN'
        else:
            if 'text' in event:
                lines = event['text'].split('\n')
            else:
                lines = []

            for line in lines:
                line_key, line_data = line.split(':', 1)
                line_data = line_data.strip()
                if line_key == 'Name':
                    base_info['name'] = line_data
                elif line_key == 'Phase':
                    base_info['phase'] = line_data
                elif line_key == 'Status':
                    base_info['status'] = line_data
                elif line_key == 'Build Queue ID':
                    base_info['queue_id'] = line_data
                else:
                    logs.debug('...ignoring {}'.format(line))

        for k, val in base_info.items():
            if val is None:
                val = "UNKNOWN"
            setattr(self, k, val)

    @property
    def is_unknown(self):
        if self.phase == 'UNKNOWN' or self.status == 'UNKNOWN':
            return True
        return False

    @property
    def is_running(self):
        if self.phase == 'STARTED':
            return True
        return False

    @property
    def is_completed(self):
        if self.phase == 'COMPLETED':
            return True
        return False

    @property
    def is_totally_done(self):
        if self.phase == 'FINALIZED':
            return True
        return False

    @property
    def is_success(self):
        if self.is_totally_done and self.status == 'SUCCESS':
            return True
        return False

    @property
    def is_failed(self):
        if self.is_totally_done and self.status != 'SUCCESS':
            return True
        return False

    @property
    def panel_text(self):
        if self.is_unknown:
            what = 'UNKNOWN'
        elif self.is_running:
            what = 'running'
        elif self.is_success:
            what = 'YAY!'
        else:
            what = self.status

        rs = '{} {} {}'.format(self.name, self.queue_id, what)
        return rs

    def __str__(self):
        return self.panel_text

    def __repr__(self):
        return str(self)


class SlackJenkinsWatcher(object):
    def __init__(self):
        self.__slack_client = SlackClient(os.environ.get('SLACK_TOKEN'))
        self.__connected = False
        self.__try_connect()
        self.__chanid = self.__determine_channel_id()
        self.__last_status = None

    def __try_connect(self):
        tries = 0
        while not self.__connected:
            tries += 1
            cr = self.__slack_client.rtm_connect()
            self.__connected = cr
            if not cr:
                logs.warn("failed to connect, try {}".format(tries))
                time.sleep(5)
            else:
                logs.info("Connected on try {}".format(tries))

    def __determine_channel_id(self):
        response = self.__slack_client.api_call("channels.list")
        channels = response['channels']
        rackhd_ci_channel = None
        for chan in channels:
            if chan['name'] == 'rackhd-ci':
                rackhd_ci_channel = chan
                break

        assert rackhd_ci_channel is not None, \
            "could not find channel 'rackhd-ci' in channel list"
        logs.info('Found channel info {}'.format(rackhd_ci_channel))
        return rackhd_ci_channel['id']

    def get_current_status(self):
        read_data = self.__slack_client.rtm_read()
        ns = None
        for event in read_data:
            if event['type'] == 'message' and event['channel'] == self.__chanid:
                print(event, self.__chanid)
                try_ns = _AStatus(event)
                print(" aaanddd try_ns name is '{}'".format(try_ns.name))
                if try_ns.name == 'MasterCI':
                    ns = try_ns
        if ns is None:
            if self.__last_status is None:
                self.__last_status = _AStatus(None)
            else:
                self.__last_status.was_updated = False
            ns = self.__last_status
        else:
            logs.info('Status has changed! {}'.format(ns))
        self.__last_status = ns
        return ns


if __name__ == "__main__":
    sjw = SlackJenkinsWatcher()
