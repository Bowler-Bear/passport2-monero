# SPDX-FileCopyrightText: © 2022 Foundation Devices, Inc. <hello@foundationdevices.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2018 Coinkite, Inc. <coldcardwallet.com>
# SPDX-License-Identifier: GPL-3.0-only
#
# (c) Copyright 2018 by Coinkite Inc. This file is part of Coldcard <coldcardwallet.com>
# and is covered by GPLv3 license found in COPYING.
#
# search_for_address_task.py - Task to search a given range of addresses to see if we find a match


async def search_for_address_task(
        on_done,
        account_number,
        address,
        address_type,
        network_type,
        lower,
        upper):

    import stash
    from errors import Error
    from uasyncio import sleep_ms
    from xmr.monero import generate_monero_keys, generate_sub_address_keys
    from xmr.addresses import AddressTypes, encode_addr
    from xmr.networks import NetworkTypes, net_version
    from xmr import crypto

    try:
        with stash.SensitiveValues() as sv:
            _, spend_pub, view_priv, _ = generate_monero_keys(sv.raw)
            r = range(lower, upper)

            #TODO: check integerated address
            if address_type == AddressTypes.PRIMARY:
                major_index = 0
            else:
                major_index = account_number
            for i in r:
                minor_index = i
                current_spend_pub, current_view_pub = generate_sub_address_keys(view_priv, spend_pub, major_index, minor_index)
                public_address = encode_addr(net_version(network_type, address_type == AddressTypes.SUB, address_type == AddressTypes.INTEGRATED), crypto.encodepoint(current_spend_pub), crypto.encodepoint(current_view_pub)).decode('ascii')
                # print('i={}: indices=({}, {}) address_type={} public_address={} address={}\n'.format(i, major_index, minor_index, address_type, public_address, address))
                if public_address == address:
                    await on_done(i, None)
                    return
                await sleep_ms(1)

        await on_done(-1, Error.ADDRESS_NOT_FOUND)
    except Exception as e:
        # print('EXCEPTION: e={}'.format(e))
        # Any address handling exceptions result in no address found
        await on_done(-1, Error.ADDRESS_NOT_FOUND)
