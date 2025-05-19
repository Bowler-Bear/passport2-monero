# SPDX-FileCopyrightText: © 2021 Foundation Devices, Inc. <hello@foundationdevices.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# monero_cli.py - Monero CLI Wallet
#

import ujson
import stash
from data_codecs.qr_type import QRType

def view_wallet_export(sw_wallet=None, addr_type=None, acct_num=0, multisig=False, legacy=False, export_mode='qr', qr_type=None):
    with stash.SensitiveValues() as sv:
        #TODO: Generate private view key and public address
        private_view_key = "view_key"
        public_address = "public_address"

    rv = dict(PrivateViewKey=private_view_key, PublicAddress=public_address)

    accts = [{'fmt': addr_type, 'deriv': None, 'acct': acct_num}]
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
