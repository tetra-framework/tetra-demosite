from time import sleep

from tetra import Component, public


class DisableButton(Component):
    @public()
    def submit(self):
        sleep(3)
