

class TrafficSwitcher:

    _signal_on: bool
    _id: int


    def __init__(self, traffic_light):
        self._signal_on = False
        self._id = traffic_light.get_id()

    def set_signal_status(self, value):
        self._signal_on = value