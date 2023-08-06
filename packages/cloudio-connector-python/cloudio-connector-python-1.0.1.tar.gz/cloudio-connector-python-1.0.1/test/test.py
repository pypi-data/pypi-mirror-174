import time
import datetime
from datetime import datetime
from threading import Thread

from src.cloudio_connector import AttributeListener, CloudioConnector, AttributeId, TimeSeries


class Tester(AttributeListener):
    def __init__(self):
        cc = CloudioConnector("http://192.168.37.130:8080", "admin", "0yveCJ1SZRvOFS24")
        cc.add_attribute_listener(self)

        # while True:
        attr = [
            AttributeId(uuid=cc.get_uuid('demo'), node='myNode', objects=['myObject'], attribute='mySetPoint'),
            AttributeId(uuid=cc.get_uuid('demo'), node='myNode', objects=['myObject'], attribute='myInt')]
        cc.subscribe_to_attribute(attr[0])
        tm = TimeSeries(attr[0], start=datetime.now() - datetime.timedelta(hours=2), stop=datetime.now(), resample='15m')
        data = cc.get_time_series(tm)


    def attribute_has_changed(self, attribute: AttributeId, value):
        print(str(attribute) + ' ' + str(value))


if __name__ == '__main__':
    for i in range(0, 1):
        Thread(target=Tester).start()
        time.sleep(0.1)
    while True:
        time.sleep(0.01)
