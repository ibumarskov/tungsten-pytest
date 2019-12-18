class IntrospectData(object):
    def __init__(self, obj):
        self.obj = obj

    @staticmethod
    def _wrap_in_list(class_type, obj):
        if isinstance(obj, list):
            return [class_type(o) for o in obj]
        else:
            return [class_type(obj)]


class NodeStatus(IntrospectData):
    def __init__(self, obj):
        super(NodeStatus, self).__init__(obj)
        self.ProcessStatus = self._wrap_in_list(
            ProcessStatus, self.obj['process_status']['list']['ProcessStatus'])

    @property
    def name(self):
        return self.obj.get('name').get('#text')


class ProcessStatus(IntrospectData):
    def __init__(self, obj):
        super(ProcessStatus, self).__init__(obj)
        self.ConnectionInfo = self._wrap_in_list(ConnectionInfo,
                                                 self.connection_infos)

    @property
    def module_id(self):
        return self.obj.get('module_id').get('#text')

    @property
    def instance_id(self):
        return self.obj.get('instance_id').get('#text')

    @property
    def state(self):
        return self.obj.get('state').get('#text')

    @property
    def description(self):
        return self.obj.get('description').get('#text')

    @property
    def connection_infos(self):
        res = self.obj.get('connection_infos')
        if res:
            return res.get('list').get('ConnectionInfo')
        else:
            return res


class ConnectionInfo(IntrospectData):
    def __init__(self, obj):
        super(ConnectionInfo, self).__init__(obj)

    @property
    def type(self):
        return self.obj.get('type').get('#text')

    @property
    def name(self):
        return self.obj.get('name').get('#text')

    @property
    def status(self):
        return self.obj.get('status').get('#text')

    @property
    def description(self):
        return self.obj.get('description').get('#text')

    @property
    def server_addrs(self):
        addr = self.obj['server_addrs']['list'].get('element')
        if isinstance(addr, list):
            return [srv for srv in addr]
        else:
            return [addr]


class BgpPeerInfoData(IntrospectData):
    def __init__(self, obj):
        super(BgpPeerInfoData, self).__init__(obj)
        self.PeerStateInfo = PeerStateInfo(
            self.obj['state_info'][0][0]['PeerStateInfo'])


class XmppPeerInfoData(IntrospectData):
    def __init__(self, obj):
        super(XmppPeerInfoData, self).__init__(obj)
        self.PeerStateInfo = PeerStateInfo(
            self.obj['state_info'][0][0]['PeerStateInfo'])


class PeerStateInfo(IntrospectData):
    def __init__(self, obj):
        super(PeerStateInfo, self).__init__(obj)

    @property
    def module_id(self):
        return self.obj.get('module_id').get('#text')

    @property
    def state(self):
        return self.obj.get('state').get('#text')
