# SPDX-FileCopyrightText: © 2021 Foundation Devices, Inc. <hello@foundationdevices.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# monero_cli.py - Monero CLI Wallet
#

import ujson
import stash
from data_codecs.qr_type import QRType
from xmr.monero import generate_monero_keys

def view_wallet_export(sw_wallet=None, addr_type=None, acct_num=0, multisig=False, legacy=False, export_mode='qr', qr_type=None):
    accts = [{'fmt': addr_type, 'deriv': None, 'acct': acct_num}]
    with stash.SensitiveValues() as sv:
        _, spend_pub, private_view_key, view_pub = generate_monero_keys(sv.raw)
        #TODO: Generate Testnet addresses too
        try:
            from xmr.addresses import encode_addr
            from xmr.networks import NetworkTypes, net_version
            from xmr import crypto
            public_address = encode_addr(net_version(NetworkTypes.MAINNET), crypto.encodepoint(spend_pub), crypto.encodepoint(view_pub))
        except Exception as e:
            return (dict(error=e), accts)

    rv = dict(PrivateViewKey=''.join('{:02x}'.format(x) for x in crypto.encodeint(private_view_key)), PublicAddress=public_address)

    msg = ujson.dumps(rv)
    return (msg, accts)


MoneroCLI = {
    'label': 'Monero CLI',
    'sig_types': [
        {'id': 'single-sig', 'label': 'Single-sig', 'addr_type': None, 'create_wallet': view_wallet_export},
    ],
    'export_modes': [
        {'id': 'qr', 'label': 'QR Code', 'qr_type': QRType.UR2},
        {'id': 'microsd', 'label': 'microSD', 'filename_pattern': 'MoneroCLI-View-Wallet.json'}
    ]
}
