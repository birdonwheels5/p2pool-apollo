import os
import platform

from twisted.internet import defer

from . import data
from p2pool.util import math, pack, jsonrpc

@defer.inlineCallbacks
def check_genesis_block(bitcoind, genesis_block_hash):
    try:
        yield bitcoind.rpc_getblock(genesis_block_hash)
    except jsonrpc.Error_for_code(-5):
        defer.returnValue(False)
    else:
        defer.returnValue(True)

nets = dict(
    apollocoin=math.Object(
        P2P_PREFIX='fcc1b7dc'.decode('hex'),
        P2P_PORT=55888,
        ADDRESS_VERSION=50,
        RPC_PORT=31914,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'apollocoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 100*100000000 >> (height + 1)//100000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=30, # s
        SYMBOL='APOLLO',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'Apollocoin') if platform.system() == 'Windows' else os.path.expanuser('~/Library/Application Support/Apollocoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.apollocoin'), 'apollocoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='',
        ADDRESS_EXPLORER_URL_PREFIX='',
        TX_EXPLORER_URL_PREFIX='',
        SANE_TARGET_RANGE=(2**256//2**32//1000 - 1, 2**256//2**20 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=0.001e8,
    ),


)
for net_name, net in nets.iteritems():
    net.NAME = net_name
