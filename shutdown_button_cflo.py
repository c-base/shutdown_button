#!/usr/bin/env python3

import os.path
from time import sleep

import msgflo
import gevent
from takaratomy.Takaratomy import Takaratomy


# when executing locally, do not forget to set MSGFLO_BROKER env variable:
# bash: export MSGFLO_BROKER=mqtt://c-beam/
# fish: set -x MSGFLO_BROKER mqtt://c-beam/


class ShutdownButton(msgflo.Participant):
    def __init__(self, role):
        self.button = Takaratomy()
        self.button.open(0)

        d = {
            'component': 'c-base/shutdown-button',
            'label': 'Shuts down the space station and initiates an evacuation',
            'icon': 'power-off',
            'inports': [
              { 'id': 'do_not_use', 'type': 'boolean' },
            ],
            'outports': [
                { 'id': 'pressed', 'type': 'boolean' },
            ],
        }

        msgflo.Participant.__init__(self, d, role)
        gevent.Greenlet.spawn(self.loop)

    def process(self, inport, msg):
        self.ack(msg)

    def onButtonPress(self):
        self.send('press', True)

    def loop(self):
        while True:
            gevent.sleep(0.1)
            state = self.button.get_state()

            if state == 1: # OPEN_BUTTON_PRESSED
              self.onButtonPress()

if __name__ == '__main__':
    print('Shutdown Button')

    msgflo.main(ShutdownButton)

