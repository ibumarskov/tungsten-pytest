class AnalyticData(object):
    def __init__(self, obj):
        self.obj = obj

    @property
    def state_info(self):
        return self.state(self.obj['state_info'][0][0]['PeerStateInfo'])

    @staticmethod
    def state(obj):
        return obj['state']['#text']


class BgpPeerInfoData(AnalyticData):
    def __init__(self, obj):
        super(BgpPeerInfoData, self).__init__(obj['BgpPeerInfoData'])


class XmppPeerInfoData(AnalyticData):
    def __init__(self, obj):
        super(XmppPeerInfoData, self).__init__(obj['XmppPeerInfoData'])


class NodeStatus(AnalyticData):
    def __init__(self, obj):
        super(NodeStatus, self).__init__(obj['NodeStatus'])

    @property
    def get_process_status(self):
        # Returns list
        return self.obj['process_status']['list']['ProcessStatus']

    @staticmethod
    def module_id(obj):
        return obj['module_id']['#text']
