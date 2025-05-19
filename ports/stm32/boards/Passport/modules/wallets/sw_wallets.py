# SPDX-FileCopyrightText: © 2021 Foundation Devices, Inc. <hello@foundationdevices.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# sw_wallets.py - Software wallet config data for all supported wallets
#
#TODO: Add Cake Wallet, Feather Wallet, Guarda Wallet, Anonero

from .monero_cli import MoneroCLI

# Array of all supported software wallets and their attributes.
# Used to build wallet menus and drive their behavior.
supported_software_wallets = [
    MoneroCLI
]
