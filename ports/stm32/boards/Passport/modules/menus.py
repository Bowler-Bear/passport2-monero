# SPDX-FileCopyrightText: © 2022 Foundation Devices, Inc. <hello@foundationdevices.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# menus.py - Menu configuration

import lvgl as lv
from utils import has_seed
# from pages import ColorPickerPage

########################################################################################
# Menu Item Fields
########################################################################################
# field            # type          # description
########################################################################################
# icon             # lv.ICON*      # icon
# label            # string        # label
# submenu          # menu function # a function that returns a list of menu items
# page             # Page          # page to display
# flow             # Flow          # flow to run
# args             # dict          # list of args passed to the submenu, page, or flow
# context          # any           # a specific arg that persists into deeper menus
# card_header      # dict          # specification of the item's card header
# statusbar        # dict          # specification of the item's statusbar
# auto_card_header # boolean       # set False to manipulate card headers manually
# exit_on_success  # booolean      # exit menu if this item is selected and returns True
# initial_selected_index # int     # a submenu arg
# is_top_level     # boolean       # a submenu arg
########################################################################################


def manage_account_menu():
    from flows import RenameAccountFlow, DeleteAccountFlow, ConnectWalletFlow
    from pages import AccountDetailsPage

    return [
        {'icon': lv.ICON_FOLDER, 'label': 'Account Details', 'page': AccountDetailsPage},
        {'icon': lv.ICON_INFO, 'label': 'Rename Account', 'flow': RenameAccountFlow},
        {'icon': lv.ICON_CONNECT, 'label': 'Connect Wallet', 'flow': ConnectWalletFlow,
         'statusbar': {'title': 'CONNECT'}},
        {'icon': lv.ICON_CANCEL, 'label': 'Delete Account', 'flow': DeleteAccountFlow},
    ]


def account_menu():
    from flows import VerifyAddressFlow, SignPsbtQRFlow, SignPsbtMicroSDFlow

    return [
        {'icon': lv.ICON_SCAN_QR, 'label': 'Sign with QR Code', 'flow': SignPsbtQRFlow,
         'statusbar': {'title': 'SIGN'}},
        {'icon': lv.ICON_MICROSD, 'label': 'Sign with microSD', 'flow': SignPsbtMicroSDFlow,
         'statusbar': {'title': 'SIGN'}},
        {'icon': lv.ICON_VERIFY_ADDRESS, 'label': 'Verify Address', 'flow': VerifyAddressFlow},
        {'icon': lv.ICON_FOLDER, 'label': 'Manage Account', 'submenu': manage_account_menu},
    ]


def health_check_submenu():
    from flows import CasaHealthCheckQRFlow, CasaHealthCheckMicrosdFlow

    return [
        {'icon': lv.ICON_SCAN_QR, 'label': 'Check with QR Code', 'flow': CasaHealthCheckQRFlow,
         'statusbar': {'title': 'SIGN'}},
        {'icon': lv.ICON_MICROSD, 'label': 'Check with microSD', 'flow': CasaHealthCheckMicrosdFlow,
         'statusbar': {'title': 'SIGN'}},
    ]


def casa_menu():
    from flows import VerifyAddressFlow, SignPsbtQRFlow, SignPsbtMicroSDFlow, ConnectWalletFlow

    return [
        {'icon': lv.ICON_SCAN_QR, 'label': 'Sign with QR Code', 'flow': SignPsbtQRFlow,
         'statusbar': {'title': 'SIGN'}},
        {'icon': lv.ICON_MICROSD, 'label': 'Sign with microSD', 'flow': SignPsbtMicroSDFlow,
         'statusbar': {'title': 'SIGN'}},
        {'icon': lv.ICON_VERIFY_ADDRESS, 'label': 'Verify Address', 'flow': VerifyAddressFlow},
        {'icon': lv.ICON_HEALTH_CHECK, 'label': 'Health Check', 'submenu': health_check_submenu},
        {'icon': lv.ICON_CONNECT, 'label': 'Connect to Casa', 'flow': ConnectWalletFlow,
         'statusbar': {'title': 'CONNECT'}, 'args': {'sw_wallet': 'Casa'}},
    ]


def postmix_menu():
    from flows import VerifyAddressFlow, SignPsbtQRFlow, SignPsbtMicroSDFlow, ConnectWalletFlow

    return [
        {'icon': lv.ICON_SCAN_QR, 'label': 'Sign with QR Code', 'flow': SignPsbtQRFlow,
         'statusbar': {'title': 'SIGN'}},
        {'icon': lv.ICON_MICROSD, 'label': 'Sign with microSD', 'flow': SignPsbtMicroSDFlow,
         'statusbar': {'title': 'SIGN'}},
        {'icon': lv.ICON_VERIFY_ADDRESS, 'label': 'Verify Address', 'flow': VerifyAddressFlow},
        {'icon': lv.ICON_CONNECT, 'label': 'Connect Wallet', 'flow': ConnectWalletFlow,
         'statusbar': {'title': 'CONNECT'}},
    ]


def plus_menu():
    from flows import NewAccountFlow

    return [
        {'icon': lv.ICON_ADD_ACCOUNT, 'label': 'New Account', 'flow': NewAccountFlow}
    ]


def device_menu():
    from flows import AboutFlow, ChangePINFlow
    from pages import AutoShutdownSettingPage, BrightnessSettingPage
    from utils import is_logged_in

    return [
        {'icon': lv.ICON_BRIGHTNESS, 'label': 'Screen Brightness', 'page': BrightnessSettingPage},
        {'icon': lv.ICON_COUNTDOWN, 'label': 'Auto-Shutdown', 'page': AutoShutdownSettingPage},
        {'icon': lv.ICON_PIN, 'label': 'Change PIN', 'flow': ChangePINFlow, 'is_visible': is_logged_in},
        {'icon': lv.ICON_INFO, 'label': 'About', 'flow': AboutFlow},
    ]


def backup_menu():
    from flows import BackupFlow, RestoreBackupFlow, VerifyBackupFlow, ViewBackupCodeFlow

    return [
        {'icon': lv.ICON_BACKUP, 'label': 'Backup Now', 'flow': BackupFlow, 'is_visible': has_seed},
        {'icon': lv.ICON_RETRY, 'label': 'Restore', 'flow': RestoreBackupFlow,
         'args': {'refresh_cards_when_done': True}},
        {'icon': lv.ICON_CIRCLE_CHECK, 'label': 'Verify Backup', 'flow': VerifyBackupFlow},
        {'icon': lv.ICON_PIN, 'label': 'View Backup Code', 'flow': ViewBackupCodeFlow,
            'statusbar': {'title': 'BACKUP', 'icon': lv.ICON_PIN}, 'is_visible': has_seed}
    ]


def key_item_menu():
    from flows import (
        ViewDerivedKeyDetailsFlow,
        RenameDerivedKeyFlow,
        ExportDerivedKeyFlow,
        HideDerivedKeyFlow)
    return [
        {'icon': lv.ICON_ONE_KEY, 'label': 'View Details', 'flow': ViewDerivedKeyDetailsFlow},
        {'icon': lv.ICON_SIGN, 'label': 'Rename', 'flow': RenameDerivedKeyFlow, 'auto_card_header': False},
        {'icon': lv.ICON_SCAN_QR, 'label': 'Export', 'flow': ExportDerivedKeyFlow},
        {'icon': lv.ICON_ERASE, 'label': 'Toggle Hidden', 'flow': HideDerivedKeyFlow},
    ]


def new_key_menu():
    from flows import NewDerivedKeyFlow
    from derived_key import key_types

    result = []
    for key_type in key_types:
        title = key_type['title']
        icon = key_type['icon']
        result.append({'icon': icon,
                       'label': title,
                       'flow': NewDerivedKeyFlow,
                       'statusbar': {'title': title.upper(),
                                     'icon': icon},
                       'args': {'context': key_type},
                       'exit_on_success': True})
    return result


def manage_keys():
    from utils import toggle_showing_hidden_keys, are_hidden_keys_showing
    return [
        {'icon': lv.ICON_TWO_KEYS,
         'label': 'Show Hidden',
         'action': lambda item: toggle_showing_hidden_keys(),
         'is_toggle': True,
         'value': lambda: are_hidden_keys_showing()},
    ]


def key_manager_menu():
    from utils import get_derived_keys, are_hidden_keys_showing
    from derived_key import get_key_type_from_tn
    from common import settings

    result = []

    keys = get_derived_keys()
    xfp = settings.get('xfp')
    showing_hidden = are_hidden_keys_showing()

    for key in keys:
        if key['xfp'] == xfp and (not key['hidden'] or showing_hidden):
            key_type = get_key_type_from_tn(key.get('tn', None))

            if not key_type:
                continue

            title = "{} ({})".format(key['name'], key['index'])

            result.append({'icon': key_type['icon'],
                           'label': title,
                           'submenu': key_item_menu,
                           'card_header': {'title': title,
                                           'right_icon': key_type['icon']},
                           'statusbar': {'title': 'KEY MANAGER'},
                           'args': {'context': key},
                           'auto_card_header': False})

    result.append({'icon': lv.ICON_ONE_KEY, 'label': 'New Key', 'submenu': new_key_menu})
    result.append({'icon': lv.ICON_SETTINGS, 'label': 'Manage', 'submenu': manage_keys})

    return result


def bitcoin_menu():
    from flows import SetChainFlow
    from pages import UnitsSettingPage
    from utils import is_logged_in

    return [
        {'icon': lv.ICON_MONERO, 'label': 'Units', 'page': UnitsSettingPage, 'is_visible': is_logged_in},
        {'icon': lv.ICON_TWO_KEYS, 'label': 'Multisig', 'submenu': multisig_menu, 'is_visible': has_seed},
        {'icon': lv.ICON_NETWORK, 'label': 'Network', 'flow': SetChainFlow, 'statusbar': {},
         'is_visible': is_logged_in},
    ]


def security_menu():
    from flows import ChangePINFlow, SignTextFileFlow, ViewSeedWordsFlow, NewSeedFlow, RestoreSeedFlow

    return [
        {'icon': lv.ICON_SEED, 'label': 'Restore Seed', 'flow': RestoreSeedFlow, 'is_visible': lambda: not has_seed(),
         'args': {'refresh_cards_when_done': True}},
        {'icon': lv.ICON_SEED, 'label': 'New Seed', 'flow': NewSeedFlow, 'is_visible': lambda: not has_seed(),
         'args': {'refresh_cards_when_done': True}},
        {'icon': lv.ICON_SIGN, 'label': 'Sign Text File', 'flow': SignTextFileFlow, 'is_visible': has_seed},
    ]


def update_menu():
    from flows import UpdateFirmwareFlow, ViewCurrentFirmwareFlow
    from utils import is_logged_in

    return [
        {'icon': lv.ICON_FIRMWARE, 'label': 'Update Firmware', 'flow': UpdateFirmwareFlow, 'is_visible': is_logged_in},
        {'icon': lv.ICON_INFO, 'label': 'Current Version', 'flow': ViewCurrentFirmwareFlow, 'statusbar': {}},
    ]


def microsd_menu():
    from flows import FormatMicroSDFlow, ListFilesFlow, ExportSummaryFlow

    return [
        {'icon': lv.ICON_MICROSD, 'label': 'Format Card', 'flow': FormatMicroSDFlow},
        {'icon': lv.ICON_FILE, 'label': 'List Files', 'flow': ListFilesFlow},
        {'icon': lv.ICON_INFO, 'label': 'Export Summary', 'flow': ExportSummaryFlow, 'is_visible': has_seed},
    ]


def multisig_item_menu():
    from flows import (RenameMultisigFlow, DeleteMultisigFlow, ViewMultisigDetailsFlow,
                       ExportMultisigQRFlow, ExportMultisigMicrosdFlow)

    return [
        {'icon': lv.ICON_TWO_KEYS, 'label': 'View Details', 'flow': ViewMultisigDetailsFlow},
        {'icon': lv.ICON_SCAN_QR, 'label': 'Export via QR', 'flow': ExportMultisigQRFlow,
         'statusbar': {'title': 'EXPORT'}},
        {'icon': lv.ICON_MICROSD, 'label': 'Export via microSD', 'flow': ExportMultisigMicrosdFlow,
         'statusbar': {'title': 'EXPORT'}},
        {'icon': lv.ICON_TWO_KEYS, 'label': 'Rename', 'flow': RenameMultisigFlow, 'exit_on_success': True},
        {'icon': lv.ICON_TWO_KEYS, 'label': 'Delete', 'flow': DeleteMultisigFlow, 'exit_on_success': True},
    ]


def multisig_menu():
    from multisig_wallet import MultisigWallet
    from pages import MultisigPolicySettingPage, ErrorPage
    from flows import ImportMultisigWalletFromMicroSDFlow, ImportMultisigWalletFromQRFlow

    if not MultisigWallet.exists():
        items = [{'icon': lv.ICON_TWO_KEYS, 'label': '(None setup yet)', 'page': ErrorPage,
                  'args': {'text': "You haven't imported any multisig wallets yet."}}]
    else:
        items = []
        for ms in MultisigWallet.get_all():
            nice_name = '%d/%d: %s' % (ms.M, ms.N, ms.name)
            items.append({
                'icon': lv.ICON_TWO_KEYS,
                'label': nice_name,
                'submenu': multisig_item_menu,
                # Adding this below causes the header to stick around after it shoudl be gone
                # Probably need MenuFlow() to pop it off after
                # 'args': {'card_header': {'title': nice_name}, 'context': ms.storage_idx}
                'args': {'context': ms.storage_idx}
            })

    items.append({'icon': lv.ICON_SCAN_QR, 'label': 'Import from QR', 'flow': ImportMultisigWalletFromQRFlow,
                 'statusbar': {'title': 'IMPORT'}})
    items.append({'icon': lv.ICON_MICROSD, 'label': 'Import from microSD',
                  'flow': ImportMultisigWalletFromMicroSDFlow, 'statusbar': {'title': 'IMPORT'}})
    items.append({'icon': lv.ICON_SETTINGS, 'label': 'Multisig Policy', 'page': MultisigPolicySettingPage})

    return items


def developer_pubkey_menu():
    from utils import has_dev_pubkey
    from flows import InstallDevPubkeyFlow, ViewDevPubkeyFlow, RemoveDevPubkeyFlow

    return [
        {'icon': lv.ICON_ONE_KEY, 'label': 'Install PubKey', 'flow': InstallDevPubkeyFlow,
         'is_visible': lambda: not has_dev_pubkey()},
        {'icon': lv.ICON_ONE_KEY, 'label': 'View PubKey', 'flow': ViewDevPubkeyFlow,
         'is_visible': has_dev_pubkey},
        {'icon': lv.ICON_CANCEL, 'label': 'Remove Pubkey', 'flow': RemoveDevPubkeyFlow,
         'is_visible': has_dev_pubkey}
    ]


def advanced_menu():
    from flows import ViewSeedWordsFlow, ErasePassportFlow, ScvFlow, ShowSecurityWordsSettingFlow

    return [
        {'icon': lv.ICON_SETTINGS, 'label': 'Security Words', 'flow': ShowSecurityWordsSettingFlow},
        {'icon': lv.ICON_SEED, 'label': 'View Seed Words', 'flow': ViewSeedWordsFlow, 'is_visible': has_seed,
         'statusbar': {'title': 'SEED WORDS', 'icon': lv.ICON_SEED}},
        {'icon': lv.ICON_ONE_KEY, 'label': 'Developer Pubkey', 'submenu': developer_pubkey_menu,
         'statusbar': {'title': 'DEV. PUBKEY'}},
        {'icon': lv.ICON_MICROSD, 'label': 'microSD', 'submenu': microsd_menu},
        {'icon': lv.ICON_ERASE, 'label': 'Erase Passport', 'flow': ErasePassportFlow},
        {'icon': lv.ICON_SHIELD, 'label': 'Security Check', 'flow': ScvFlow,
         'args': {'envoy': False, 'ask_to_skip': False}},
    ]


def developer_menu():
    import passport

    if passport.IS_DEV:
        from flows import (
            ScvFlow,
            LoginFlow,
            NewSeedFlow,
            SetInitialPINFlow,
        )
        from developer import (
            BatteryPage,
            DeleteDerivedKeysFlow,
            DeveloperFunctionsFlow,
            SpinDelayFlow,
        )
        from pages import StatusPage, ShowQRPage
        from data_codecs.qr_type import QRType
        from foundation import ur

        return [
            {'icon': lv.ICON_BATTERY, 'label': 'Battery', 'page': BatteryPage},
            {'icon': lv.ICON_ERASE, 'label': 'Factory Reset',
                'flow': DeveloperFunctionsFlow, 'args': {'fn_name': 'factory_reset'}},
            {'icon': lv.ICON_RETRY, 'label': 'Spin!!!', 'flow': SpinDelayFlow, 'args': {'delay_ms': 10000}},
            {'icon': lv.ICON_SETTINGS, 'label': 'Dump Settings',
                'flow': DeveloperFunctionsFlow, 'args': {'fn_name': 'dump_settings'}},
            {'icon': lv.ICON_SCAN_QR, 'label': 'Show Setup QR', 'page': StatusPage, 'args': {
                'text': 'Scan the QR code above with Envoy.', 'icon': lv.LARGE_ICON_SETUP_QR}, 'card_header': {}},
            {'icon': lv.ICON_SCAN_QR, 'label': 'Show Test UR', 'page': ShowQRPage, 'args': {
                'qr_type': QRType.UR2, 'qr_data': ur.new_bytes('test data' * 10)}},
            {'icon': lv.ICON_SHIELD, 'label': 'Supply Chain', 'flow': ScvFlow},
            {'icon': lv.ICON_ONE_KEY, 'label': 'Login', 'flow': LoginFlow},
            {'icon': lv.ICON_SEED, 'label': 'New Seed', 'flow': NewSeedFlow, 'args': {'refresh_cards_when_done': True}},
            {'icon': lv.ICON_ONE_KEY, 'label': 'Set PIN', 'flow': SetInitialPINFlow},
            {'icon': lv.ICON_ERASE, 'label': 'Erase Child Keys', 'flow': DeleteDerivedKeysFlow},
            # {'icon': lv.ICON_SETTINGS, 'label': 'I\'m Busy!', 'page': LongTextPage,
            #     'args': {'show_busy': True, 'message': 'Signing Transaction...'}},
            # {'icon': lv.ICON_SETTINGS, 'label': 'FCC Test', 'flow': FCCTestFlow},
            # {'icon': lv.ICON_ABOUT, 'label': 'Color Picker', 'page': ColorPickerPage},
            # {'icon': lv.ICON_CHANGE_PIN, 'label': 'Enter PIN', 'page': PINEntryPage,
            #  'args': {'title': 'Enter Initial PIN'}},
            # {'icon': lv.ICON_FOLDER, 'label': 'Rename Account', 'page': TextInputPage,
            #     'args': {'card_header': {'title': 'Rename Account', 'icon': lv.ICON_ABOUT, 'right_text': '!!',
            #              'bg_color': RED, 'fg_color': FD_BLUE}}},
            # {'icon': lv.ICON_SEED, 'label': 'Enter Seed', 'page': PredictiveTextInputPage},
            # {'icon': lv.ICON_CHANGE_PIN, 'label': 'Enter Backup Code', 'page': BackupCodePage},
        ]
    else:
        return []


def extensions_menu():
    from extensions.extensions import supported_extensions_menu
    return supported_extensions_menu


def settings_menu():
    from utils import is_logged_in, is_dev_build

    return [
        {'icon': lv.ICON_DEVICE, 'label': 'Device', 'submenu': device_menu},
        {'icon': lv.ICON_BACKUP, 'label': 'Backup', 'submenu': backup_menu, 'is_visible': is_logged_in},
        {'icon': lv.ICON_FIRMWARE, 'label': 'Firmware', 'submenu': update_menu},
        {'icon': lv.ICON_MONERO, 'label': 'Monero', 'submenu': bitcoin_menu, 'is_visible': is_logged_in},
        {'icon': lv.ICON_ADVANCED, 'label': 'Advanced', 'submenu': advanced_menu, 'is_visible': is_logged_in},
        {'icon': lv.ICON_EXTENSIONS, 'label': 'Extensions', 'submenu': extensions_menu},
        {'icon': lv.ICON_ADVANCED, 'label': 'Developer', 'submenu': developer_menu, 'is_visible': is_dev_build}
    ]
