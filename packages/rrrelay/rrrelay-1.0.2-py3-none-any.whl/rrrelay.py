# SPDX-License-Identifier: MIT
"""rrrelay

 Read HTTP POST messages from Race Result Decoder or Track Box and 
 relay as telegraph timing messages in the following format:

	INDEX;SOURCE;CHANNEL;REFID;TOD;DATE

   - INDEX : passing sequence number (set by the relay)
   - SOURCE : decoder ID or nickname
   - CHANNEL : loop id or timing channel
   - REFID : transponder unique ID
   - TOD : local time of day string eg 13h27:52.4321
   - DATE : date of passing  eg 2023-02-27

 HTTP Endpoints:

	POST /rrs	Race Result Decoder Passings
	POST /tbp	Track Box 'Ping'	[TODO]
	GET /tbs	Track Box 'Status'	[TODO]

"""

import asyncio
import sys
import tornado.web
import logging
import signal
import metarace
import json
from metarace.strops import confopt_posint
from metarace.telegraph import telegraph
from metarace import tod

_LOGLEVEL = logging.DEBUG
_log = logging.getLogger('rrrelay')
_log.setLevel(_LOGLEVEL)

_QOS = 2
_PORT = 53037
_PASSTOPIC = 'timing/data'
_STATUSTOPIC = 'timing/status'
_SAVEFILE = 'passings.json'
_SAVEINTERVAL = 30
_USERID = ''
_TBPLEN = 11
_RRSLEN = 19
_RRSLOWBATT = 2.0
_RRSMARKER = '99999'


def fixdate(rrdate):
    """Repair RR datetime string"""
    return '20' + rrdate


class TbsHandler(tornado.web.RequestHandler):
    """HTTP request handler for Track Box status messages"""

    def initialize(self, app):
        self.app = app

    async def get(self):
        user = self.get_argument('custId', '-')
        if not self.app.userid or user == self.app.userid:
            _log.debug('Status: %r', self.request)
            deviceid = self.get_argument('boxId')
            channel = self.app.channel(deviceid, 'C1')
            datestr = fixdate(self.get_argument('boxTime'))
            date, boxtime = tod.fromiso(datestr)
            temp = self.get_argument('boxTemp', '-')
            stat = self.get_argument('readerStatus', 'NONE')
            noise = self.get_argument('boxNoise', 'NONE')
            accel = self.get_argument('boxAccel', '-')
            batt = self.get_argument('boxBatt', '-')
            srec = [
                deviceid, channel,
                boxtime.rawtime(3), date, stat, temp, noise, accel, batt
            ]
            _log.info('TBS: %r', srec)
            await self.app.status(srec)
        self.write('OK')


class TbpHandler(tornado.web.RequestHandler):
    """HTTP request handler for Track Box ping messages"""

    def initialize(self, app):
        self.app = app

    async def post(self):
        user = self.get_argument('custId', '-')
        if not self.app.userid or user == self.app.userid:
            _log.debug('Ping: %r', self.request)
            deviceid = self.get_argument('boxId')
            posinfo = self.get_argument('boxPos', 'U')
            channel = self.app.channel(deviceid, 'C1')
            fileindex = self.get_argument('index', '0')
            count = self.get_argument('count', '0')
            datestr = fixdate(self.get_argument('boxTime'))
            date, boxtime = tod.fromiso(datestr)
            passings = []
            for l in self.request.body.decode('ascii', 'ignore').split('\r'):
                passingstr = l.strip()
                if passingstr:
                    pv = passingstr.split(';')
                    if len(pv) == _TBPLEN:
                        tagid = pv[0]
                        eventid = pv[10]
                        if eventid and eventid != '0':
                            tagid = '-'.join((eventid, tagid))
                        tagtime = boxtime - tod.tod(pv[1])
                        rssi = int(pv[2])
                        hitcount = int(pv[3])
                        if hitcount < 4 or rssi < -82:
                            _log.warning('Poor read %s: Hits:%d RSSI:%ddBm',
                                         tagid, hitcount, rssi)
                        prec = [
                            None, deviceid, channel, tagid,
                            tagtime.rawtime(3), date
                        ]
                        passings.append(prec)
                        _log.info('TBP: %r', prec)
                    else:
                        _log.error('Invalid passing ignored: %r', l)
            if passings:
                await self.app.passing(passings)
        self.write('OK')


class RrsHandler(tornado.web.RequestHandler):
    """HTTP request handler for Race Result System decoders"""

    def initialize(self, app):
        self.app = app

    async def post(self):
        user = self.get_argument('user', '-')
        if not self.app.userid or user == self.app.userid:
            _log.debug('Passing: %r', self.request)
            deviceid = self.get_argument('device')
            passings = []
            for l in self.request.body.decode('ascii', 'ignore').split('\n'):
                passingstr = l.strip()
                if passingstr:
                    pv = passingstr.split(';')
                    if len(pv) == _RRSLEN:
                        tagid = ''
                        channel = self.app.channel(deviceid, 'C1')
                        date = pv[2]
                        time = tod.tod(pv[3])
                        hitcount = int(pv[5])
                        rssi = int(pv[6])
                        isactive = bool(int(pv[10]))
                        if isactive:
                            tagid = pv[8]
                            channel = 'C' + str(int(pv[12]))
                            rssi = -90 + ((rssi & 0x70) >> 2)
                            battery = float(pv[15])
                            if battery < _RRSLOWBATT:
                                _log.warning('Low battery %s: %0.1fV', tagid,
                                             bv)
                            activestore = False
                            if pv[17]:
                                activestore = (int(pv[17]) & 0x40) == 0x40
                        else:
                            tagid = pv[1]
                            eventid = pv[4]
                            if eventid and eventid != '0':
                                tagid = '-'.join((eventid, tagid))
                        if tagid == _RRSMARKER:
                            tagid = ''
                        else:
                            if hitcount < 4 or rssi < -82:
                                _log.warning(
                                    'Poor read %s: Hits:%d RSSI:%ddBm', tagid,
                                    hitcount, rssi)
                        prec = [
                            None, deviceid, channel, tagid,
                            time.rawtime(3), date
                        ]
                        passings.append(prec)
                        astr = 'passive'
                        if isactive:
                            astr = 'active'
                        _log.info('RRS %s: %r', astr, prec)
                    else:
                        _log.error('Invalid passing ignored: %r', l)
            if passings:
                await self.app.passing(passings)

        else:
            _log.error('Invalid user ignored: %r', user)
        self.write('OK')


class app:

    def __init__(self):
        self._t = telegraph()
        self._port = _PORT
        self._passtopic = _PASSTOPIC
        self._statustopic = _STATUSTOPIC
        self._passingLock = None
        self._passings = []
        self._qos = _QOS
        self._shutdown = None
        self._loopids = {}
        self._dirty = True
        self._savetasks = set()
        self.userid = _USERID

    def _loadconfig(self):
        """Load configuration from sysconf"""
        if metarace.sysconf.has_option('rrrelay', 'port'):
            self._port = metarace.sysconf.get_posint('rrrelay', 'port', _PORT)
        if metarace.sysconf.has_option('rrrelay', 'passtopic'):
            self._passtopic = metarace.sysconf.get_str('rrrelay', 'passtopic',
                                                       _PASSTOPIC)
        if metarace.sysconf.has_option('rrrelay', 'statustopic'):
            self._statustopic = metarace.sysconf.get_str(
                'rrrelay', 'statustopic', _STATUSTOPIC)
        if metarace.sysconf.has_option('rrrelay', 'qos'):
            self._qos = metarace.sysconf.get_posint('rrrelay', 'qos', _QOS)
        if metarace.sysconf.has_option('rrrelay', 'userid'):
            self.userid = metarace.sysconf.get_str('rrrelay', 'userid',
                                                   _USERID)
        if metarace.sysconf.has_option('rrrelay', 'passiveloop'):
            try:
                loopids = metarace.sysconf.get('rrrelay', 'passiveloop')
                if isinstance(loopids, dict):
                    for deviceid in loopids:
                        if isinstance(loopids[deviceid], str):
                            self._loopids[deviceid] = loopids[deviceid]
                else:
                    _log.info('Ignored invalid loopids entry')
            except Exception as e:
                _log.warning('%s reading loopids: %s', e.__class__.__name__, e)
            _log.info('Set loop ID overrides to: %r', self._loopids)

        _log.debug(
            'Config: port=%r, statustopic=%r, passtopic=%r, qos=%r, userid=%r',
            self._port, self._statustopic, self._passtopic, self._qos,
            self.userid)

    def _loadpassings(self):
        """Read in saved passings from file"""
        try:
            with open(_SAVEFILE) as f:
                self._passings = json.load(f)
        except Exception as e:
            _log.error('%s reading stored passings: %s', e.__class__.__name__,
                       e)

    def channel(self, device, channel='C1'):
        """Return a channel id for the provided device"""
        try:
            if device in self._loopids:
                channel = self._loopids[device]
        except Exception as e:
            _log.info('%s reading %r channel id: %s', e.__class__.__name__,
                      device, e)
        return channel

    async def status(self, s):
        """Publish the track box status"""
        self._t.publish(topic=self._statustopic, message=u';'.join(s))

    async def passing(self, passings):
        """Relay and store provided passings"""
        async with self._passingLock:
            for p in passings:
                index = len(self._passings)
                p[0] = str(index)
                self._passings.append(p)
                self._t.publish(topic=self._passtopic,
                                message=u';'.join(p),
                                qos=self._qos)
                self._dirty = True

    def _savepassings(self):
        """Dump passings to the savefile"""
        try:
            with metarace.savefile(_SAVEFILE) as f:
                json.dump(self._passings, f)
            self._dirty = False
        except Exception as e:
            _log.error('%s writing passings: %s', e.__class__.__name__, e)

    def _sigterm(self):
        """Handle the TERM signal"""
        _log.info('Terminated by SIGTERM')
        self._shutdown.set()

    def _queue_save(self):
        """Create a task to save the passings, later"""
        nextSave = asyncio.create_task(self._delayed_save())
        self._savetasks.add(nextSave)
        nextSave.add_done_callback(self._savetasks.discard)

    async def _delayed_save(self):
        """Write out the passings if required then re-schedule"""
        await asyncio.sleep(_SAVEINTERVAL)
        if self._dirty:
            self._savepassings()
            _log.debug('Save %d passings', len(self._passings))
        self._queue_save()

    async def run(self):
        _log.info('Starting')
        self._loadconfig()
        self._loadpassings()

        # start telegraph
        self._t.start()

        # add passing lock
        self._passingLock = asyncio.Lock()

        # catch TERM signal
        self._shutdown = asyncio.Event()
        asyncio.get_running_loop().add_signal_handler(signal.SIGTERM,
                                                      self._sigterm)

        try:
            # setup tornado async server
            _log.info('Starting http listener on port %r', self._port)
            web = tornado.web.Application([
                (r"/rrs", RrsHandler, dict(app=self)),
                (r"/tbp", TbpHandler, dict(app=self)),
                (r"/tbs", TbsHandler, dict(app=self)),
            ])
            web.listen(self._port)
            self._queue_save()
            await self._shutdown.wait()
        except Exception as e:
            _log.error('%s: %s', e.__class__.__name__, e)
        finally:
            self._t.wait()
            self._t.exit()
            self._t.join()
            self._savepassings()
        return 0


def main():
    ch = logging.StreamHandler()
    ch.setLevel(_LOGLEVEL)
    fh = logging.Formatter(metarace.LOGFORMAT)
    ch.setFormatter(fh)
    logging.getLogger().addHandler(ch)

    # initialise the base library
    metarace.init()

    # Create and start relay app
    a = app()
    asyncio.run(a.run())


if __name__ == '__main__':
    sys.exit(main())
