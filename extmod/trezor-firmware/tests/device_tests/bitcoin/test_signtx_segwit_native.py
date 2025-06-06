# This file is part of the Trezor project.
#
# Copyright (C) 2012-2019 SatoshiLabs and contributors
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the License along with this library.
# If not, see <https://www.gnu.org/licenses/lgpl-3.0.html>.

import pytest

from trezorlib import btc, messages
from trezorlib.tools import H_, parse_path

from ...bip32 import deserialize
from ...tx_cache import TxCache
from ..signtx import request_finished, request_input, request_meta, request_output

B = messages.ButtonRequestType
TX_API = TxCache("Testnet")

TXHASH_20912f = bytes.fromhex(
    "20912f98ea3ed849042efed0fdac8cb4fc301961c5988cba56902d8ffb61c337"
)
TXHASH_091446 = bytes.fromhex(
    "09144602765ce3dd8f4329445b20e3684e948709c5cdcaf12da3bb079c99448a"
)
TXHASH_65b811 = bytes.fromhex(
    "65b811d3eca0fe6915d9f2d77c86c5a7f19bf66b1b1253c2c51cb4ae5f0c017b"
)
TXHASH_e5040e = bytes.fromhex(
    "e5040e1bc1ae7667ffb9e5248e90b2fb93cd9150234151ce90e14ab2f5933bcd"
)
TXHASH_9c3192 = bytes.fromhex(
    "9c31922be756c06d02167656465c8dc83bb553bf386a3f478ae65b5c021002be"
)
TXHASH_f41cbe = bytes.fromhex(
    "f41cbedd8becee05a830f418d13aa665125464547db5c7a6cd28f21639fe1228"
)
TXHASH_c93480 = bytes.fromhex(
    "c9348040bbc2024e12dcb4a0b4806b0398646b91acf314da028c3f03dd0179fc"
)
TXHASH_31bc1c = bytes.fromhex(
    "31bc1c88ce6ae337a6b3057a16d5bad0b561ad1dfc047d0a7fbb8814668f91e5"
)
TXHASH_a345b8 = bytes.fromhex(
    "a345b85759b385c6446055e4c3baa77e8161a65009dc009489b48aa6587ce348"
)
TXHASH_ec16dc = bytes.fromhex(
    "ec16dc5a539c5d60001a7471c37dbb0b5294c289c77df8bd07870b30d73e2231"
)


def test_send_p2sh(client):
    inp1 = messages.TxInputType(
        address_n=parse_path("49'/1'/0'/1/0"),
        # 2N1LGaGg836mqSQqiuUBLfcyGBhyZbremDX
        amount=123456789,
        prev_hash=TXHASH_20912f,
        prev_index=0,
        script_type=messages.InputScriptType.SPENDP2SHWITNESS,
    )
    out1 = messages.TxOutputType(
        address="tb1qqzv60m9ajw8drqulta4ld4gfx0rdh82un5s65s",
        amount=12300000,
        script_type=messages.OutputScriptType.PAYTOADDRESS,
    )
    out2 = messages.TxOutputType(
        address="2N1LGaGg836mqSQqiuUBLfcyGBhyZbremDX",
        script_type=messages.OutputScriptType.PAYTOADDRESS,
        amount=123456789 - 11000 - 12300000,
    )
    with client:
        client.set_expected_responses(
            [
                request_input(0),
                request_output(0),
                messages.ButtonRequest(code=B.ConfirmOutput),
                request_output(1),
                messages.ButtonRequest(code=B.ConfirmOutput),
                messages.ButtonRequest(code=B.SignTx),
                request_input(0),
                request_meta(TXHASH_20912f),
                request_input(0, TXHASH_20912f),
                request_output(0, TXHASH_20912f),
                request_output(1, TXHASH_20912f),
                request_input(0),
                request_output(0),
                request_output(1),
                request_input(0),
                request_finished(),
            ]
        )
        _, serialized_tx = btc.sign_tx(
            client, "Testnet", [inp1], [out1, out2], prev_txes=TX_API
        )

    assert (
        serialized_tx.hex()
        == "0100000000010137c361fb8f2d9056ba8c98c5611930fcb48cacfdd0fe2e0449d83eea982f91200000000017160014d16b8c0680c61fc6ed2e407455715055e41052f5ffffffff02e0aebb00000000001600140099a7ecbd938ed1839f5f6bf6d50933c6db9d5c3df39f060000000017a91458b53ea7f832e8f096e896b8713a8c6df0e892ca8702483045022100bd3d8b8ad35c094e01f6282277300e575f1021678fc63ec3f9945d6e35670da3022052e26ef0dd5f3741c9d5939d1dec5464c15ab5f2c85245e70a622df250d4eb7c012103e7bfe10708f715e8538c92d46ca50db6f657bbc455b7494e6a0303ccdb868b7900000000"
    )


def test_send_p2sh_change(client):
    inp1 = messages.TxInputType(
        address_n=parse_path("49'/1'/0'/1/0"),
        # 2N1LGaGg836mqSQqiuUBLfcyGBhyZbremDX
        amount=123456789,
        prev_hash=TXHASH_20912f,
        prev_index=0,
        script_type=messages.InputScriptType.SPENDP2SHWITNESS,
    )
    out1 = messages.TxOutputType(
        address="tb1qqzv60m9ajw8drqulta4ld4gfx0rdh82un5s65s",
        amount=12300000,
        script_type=messages.OutputScriptType.PAYTOADDRESS,
    )
    out2 = messages.TxOutputType(
        address_n=parse_path("49'/1'/0'/1/0"),
        script_type=messages.OutputScriptType.PAYTOP2SHWITNESS,
        amount=123456789 - 11000 - 12300000,
    )
    with client:
        client.set_expected_responses(
            [
                request_input(0),
                request_output(0),
                messages.ButtonRequest(code=B.ConfirmOutput),
                request_output(1),
                messages.ButtonRequest(code=B.SignTx),
                request_input(0),
                request_meta(TXHASH_20912f),
                request_input(0, TXHASH_20912f),
                request_output(0, TXHASH_20912f),
                request_output(1, TXHASH_20912f),
                request_input(0),
                request_output(0),
                request_output(1),
                request_input(0),
                request_finished(),
            ]
        )
        _, serialized_tx = btc.sign_tx(
            client, "Testnet", [inp1], [out1, out2], prev_txes=TX_API
        )

    assert (
        serialized_tx.hex()
        == "0100000000010137c361fb8f2d9056ba8c98c5611930fcb48cacfdd0fe2e0449d83eea982f91200000000017160014d16b8c0680c61fc6ed2e407455715055e41052f5ffffffff02e0aebb00000000001600140099a7ecbd938ed1839f5f6bf6d50933c6db9d5c3df39f060000000017a91458b53ea7f832e8f096e896b8713a8c6df0e892ca8702483045022100bd3d8b8ad35c094e01f6282277300e575f1021678fc63ec3f9945d6e35670da3022052e26ef0dd5f3741c9d5939d1dec5464c15ab5f2c85245e70a622df250d4eb7c012103e7bfe10708f715e8538c92d46ca50db6f657bbc455b7494e6a0303ccdb868b7900000000"
    )


def test_send_native(client):
    inp1 = messages.TxInputType(
        address_n=parse_path("84'/1'/0'/0/0"),
        amount=12300000,
        prev_hash=TXHASH_091446,
        prev_index=0,
        script_type=messages.InputScriptType.SPENDWITNESS,
    )
    out1 = messages.TxOutputType(
        address="2N4Q5FhU2497BryFfUgbqkAJE87aKHUhXMp",
        amount=5000000,
        script_type=messages.OutputScriptType.PAYTOADDRESS,
    )
    out2 = messages.TxOutputType(
        address="tb1q694ccp5qcc0udmfwgp692u2s2hjpq5h407urtu",
        script_type=messages.OutputScriptType.PAYTOADDRESS,
        amount=12300000 - 11000 - 5000000,
    )
    with client:
        client.set_expected_responses(
            [
                request_input(0),
                request_output(0),
                messages.ButtonRequest(code=B.ConfirmOutput),
                request_output(1),
                messages.ButtonRequest(code=B.ConfirmOutput),
                messages.ButtonRequest(code=B.SignTx),
                request_input(0),
                request_meta(TXHASH_091446),
                request_input(0, TXHASH_091446),
                request_output(0, TXHASH_091446),
                request_output(1, TXHASH_091446),
                request_input(0),
                request_output(0),
                request_output(1),
                request_input(0),
                request_finished(),
            ]
        )
        _, serialized_tx = btc.sign_tx(
            client, "Testnet", [inp1], [out1, out2], prev_txes=TX_API
        )

    assert (
        serialized_tx.hex()
        == "010000000001018a44999c07bba32df1cacdc50987944e68e3205b4429438fdde35c76024614090000000000ffffffff02404b4c000000000017a9147a55d61848e77ca266e79a39bfc85c580a6426c987a8386f0000000000160014d16b8c0680c61fc6ed2e407455715055e41052f502473044022073ce72dcf2f6e42eeb44adbe7d5038cf3763f168d1c04bd8b873a19b53331f51022016b051725731e7f53a567021bcd9c370727f551c81e857ebae7c128472119652012103adc58245cf28406af0ef5cc24b8afba7f1be6c72f279b642d85c48798685f86200000000"
    )


def test_send_to_taproot(client):
    inp1 = messages.TxInputType(
        address_n=parse_path("84'/1'/0'/0/0"),
        amount=10000,
        prev_hash=TXHASH_ec16dc,
        prev_index=0,
        script_type=messages.InputScriptType.SPENDWITNESS,
    )
    out1 = messages.TxOutputType(
        address="tb1pdvdljpj774356dpk32c2ks0yqv7q7c4f98px2d9e76s73vpudpxs7tl6vp",
        amount=7000,
        script_type=messages.OutputScriptType.PAYTOADDRESS,
    )
    out2 = messages.TxOutputType(
        address="tb1qcc4ext5rsa8pzqa2m030jk670wmn5f649pu7sr",
        script_type=messages.OutputScriptType.PAYTOADDRESS,
        amount=10000 - 7000 - 200,
    )
    with client:
        _, serialized_tx = btc.sign_tx(
            client, "Testnet", [inp1], [out1, out2], prev_txes=TX_API
        )

    assert (
        serialized_tx.hex()
        == "0100000000010131223ed7300b8707bdf87dc789c294520bbb7dc371741a00605d9c535adc16ec0000000000ffffffff02581b0000000000002251206b1bf9065ef5634d34368ab0ab41e4033c0f62a929c26534b9f6a1e8b03c684df00a000000000000160014c62b932e83874e1103aadbe2f95b5e7bb73a275502473044022008ce0e893e91935ada9a31fe6b2f6228070dd2a5bdebc413429e658be761901502207086e0d3aa6abbad29c966444d3b791e43c174f88154381d07c92a84fec7c527012103adc58245cf28406af0ef5cc24b8afba7f1be6c72f279b642d85c48798685f86200000000"
    )


def test_send_native_change(client):
    inp1 = messages.TxInputType(
        address_n=parse_path("84'/1'/0'/0/0"),
        amount=12300000,
        prev_hash=TXHASH_091446,
        prev_index=0,
        script_type=messages.InputScriptType.SPENDWITNESS,
    )
    out1 = messages.TxOutputType(
        address="2N4Q5FhU2497BryFfUgbqkAJE87aKHUhXMp",
        amount=5000000,
        script_type=messages.OutputScriptType.PAYTOADDRESS,
    )
    out2 = messages.TxOutputType(
        address_n=parse_path("84'/1'/0'/1/0"),
        script_type=messages.OutputScriptType.PAYTOWITNESS,
        amount=12300000 - 11000 - 5000000,
    )
    with client:
        client.set_expected_responses(
            [
                request_input(0),
                request_output(0),
                messages.ButtonRequest(code=B.ConfirmOutput),
                request_output(1),
                messages.ButtonRequest(code=B.SignTx),
                request_input(0),
                request_meta(TXHASH_091446),
                request_input(0, TXHASH_091446),
                request_output(0, TXHASH_091446),
                request_output(1, TXHASH_091446),
                request_input(0),
                request_output(0),
                request_output(1),
                request_input(0),
                request_finished(),
            ]
        )
        _, serialized_tx = btc.sign_tx(
            client, "Testnet", [inp1], [out1, out2], prev_txes=TX_API
        )

    assert (
        serialized_tx.hex()
        == "010000000001018a44999c07bba32df1cacdc50987944e68e3205b4429438fdde35c76024614090000000000ffffffff02404b4c000000000017a9147a55d61848e77ca266e79a39bfc85c580a6426c987a8386f0000000000160014cc8067093f6f843d6d3e22004a4290cd0c0f336b024730440220067675423ca6a0be3ddd5e13da00a9433775041e5cebc838873d2686f1d2840102201a5819e0312e6451d6b6180689101bce995685a51524cc4c3a5383f7bdab979a012103adc58245cf28406af0ef5cc24b8afba7f1be6c72f279b642d85c48798685f86200000000"
    )


def test_send_both(client):
    inp1 = messages.TxInputType(
        address_n=parse_path("49'/1'/0'/1/0"),
        # 2N1LGaGg836mqSQqiuUBLfcyGBhyZbremDX
        amount=111145789,
        prev_hash=TXHASH_091446,
        prev_index=1,
        script_type=messages.InputScriptType.SPENDP2SHWITNESS,
    )
    inp2 = messages.TxInputType(
        address_n=parse_path("84'/1'/0'/1/0"),
        amount=7289000,
        prev_hash=TXHASH_65b811,
        prev_index=1,
        script_type=messages.InputScriptType.SPENDWITNESS,
    )
    out1 = messages.TxOutputType(
        address="tb1q54un3q39sf7e7tlfq99d6ezys7qgc62a6rxllc",
        amount=12300000,
        script_type=messages.OutputScriptType.PAYTOADDRESS,
    )
    out2 = messages.TxOutputType(
        # address_n=parse_path("44'/1'/0'/0/0"),
        # script_type=messages.OutputScriptType.PAYTOP2SHWITNESS,
        address="2N6UeBoqYEEnybg4cReFYDammpsyDw8R2Mc",
        script_type=messages.OutputScriptType.PAYTOADDRESS,
        amount=45600000,
    )
    out3 = messages.TxOutputType(
        address="mvbu1Gdy8SUjTenqerxUaZyYjmveZvt33q",
        amount=111145789 + 7289000 - 11000 - 12300000 - 45600000,
        script_type=messages.OutputScriptType.PAYTOADDRESS,
    )

    with client:
        client.set_expected_responses(
            [
                request_input(0),
                request_input(1),
                request_output(0),
                messages.ButtonRequest(code=B.ConfirmOutput),
                request_output(1),
                messages.ButtonRequest(code=B.ConfirmOutput),
                request_output(2),
                messages.ButtonRequest(code=B.ConfirmOutput),
                messages.ButtonRequest(code=B.SignTx),
                request_input(0),
                request_meta(TXHASH_091446),
                request_input(0, TXHASH_091446),
                request_output(0, TXHASH_091446),
                request_output(1, TXHASH_091446),
                request_input(1),
                request_meta(TXHASH_65b811),
                request_input(0, TXHASH_65b811),
                request_output(0, TXHASH_65b811),
                request_output(1, TXHASH_65b811),
                request_input(0),
                request_input(1),
                request_output(0),
                request_output(1),
                request_output(2),
                request_input(0),
                request_input(1),
                request_finished(),
            ]
        )
        _, serialized_tx = btc.sign_tx(
            client, "Testnet", [inp1, inp2], [out1, out2, out3], prev_txes=TX_API
        )

    assert (
        serialized_tx.hex()
        == "010000000001028a44999c07bba32df1cacdc50987944e68e3205b4429438fdde35c76024614090100000017160014d16b8c0680c61fc6ed2e407455715055e41052f5ffffffff7b010c5faeb41cc5c253121b6bf69bf1a7c5867cd7f2d91569fea0ecd311b8650100000000ffffffff03e0aebb0000000000160014a579388225827d9f2fe9014add644487808c695d00cdb7020000000017a91491233e24a9bf8dbb19c1187ad876a9380c12e787870d859b03000000001976a914a579388225827d9f2fe9014add644487808c695d88ac02483045022100ead79ee134f25bb585b48aee6284a4bb14e07f03cc130253e83450d095515e5202201e161e9402c8b26b666f2b67e5b668a404ef7e57858ae9a6a68c3837e65fdc69012103e7bfe10708f715e8538c92d46ca50db6f657bbc455b7494e6a0303ccdb868b7902463043021f585c54a84dc7326fa60e22729accd41153c7dd4725bd4c8f751aa3a8cd8d6a0220631bfd83fc312cc6d5d129572a25178696d81eaf50c8c3f16c6121be4f4c029d012103505647c017ff2156eb6da20fae72173d3b681a1d0a629f95f49e884db300689f00000000"
    )


@pytest.mark.multisig
def test_send_multisig_1(client):
    nodes = [
        btc.get_public_node(client, parse_path(f"49'/1'/{index}'"), coin_name="Testnet")
        for index in range(1, 4)
    ]
    multisig = messages.MultisigRedeemScriptType(
        nodes=[deserialize(n.xpub) for n in nodes],
        address_n=[0, 0],
        signatures=[b"", b"", b""],
        m=2,
    )

    inp1 = messages.TxInputType(
        address_n=parse_path("49'/1'/1'/0/0"),
        prev_hash=TXHASH_9c3192,
        prev_index=1,
        script_type=messages.InputScriptType.SPENDP2SHWITNESS,
        multisig=multisig,
        amount=1610436,
    )

    out1 = messages.TxOutputType(
        address="tb1qch62pf820spe9mlq49ns5uexfnl6jzcezp7d328fw58lj0rhlhasge9hzy",
        amount=1605000,
        script_type=messages.OutputScriptType.PAYTOADDRESS,
    )

    with client:
        client.set_expected_responses(
            [
                request_input(0),
                request_output(0),
                messages.ButtonRequest(code=B.ConfirmOutput),
                messages.ButtonRequest(code=B.SignTx),
                request_input(0),
                request_meta(TXHASH_9c3192),
                request_input(0, TXHASH_9c3192),
                request_output(0, TXHASH_9c3192),
                request_output(1, TXHASH_9c3192),
                request_input(0),
                request_output(0),
                request_input(0),
                request_finished(),
            ]
        )
        signatures, _ = btc.sign_tx(client, "Testnet", [inp1], [out1], prev_txes=TX_API)
        # store signature
        inp1.multisig.signatures[0] = signatures[0]
        # sign with third key
        inp1.address_n[2] = H_(3)
        client.set_expected_responses(
            [
                request_input(0),
                request_output(0),
                messages.ButtonRequest(code=B.ConfirmOutput),
                messages.ButtonRequest(code=B.SignTx),
                request_input(0),
                request_meta(TXHASH_9c3192),
                request_input(0, TXHASH_9c3192),
                request_output(0, TXHASH_9c3192),
                request_output(1, TXHASH_9c3192),
                request_input(0),
                request_output(0),
                request_input(0),
                request_finished(),
            ]
        )
        _, serialized_tx = btc.sign_tx(
            client, "Testnet", [inp1], [out1], prev_txes=TX_API
        )

    assert (
        serialized_tx.hex()
        == "01000000000101be0210025c5be68a473f6a38bf53b53bc88d5c46567616026dc056e72b92319c01000000232200208d398cfb58a1d9cdb59ccbce81559c095e8c6f4a3e64966ca385078d9879f95effffffff01887d180000000000220020c5f4a0a4ea7c0392efe0a9670a73264cffa90b19107cd8a8e9750ff93c77fdfb0400483045022100dd6342c65197af27d7894d8b8b88b16b568ee3b5ebfdc55fdfb7caa9650e3b4c02200c7074a5bcb0068f63d9014c7cd2b0490aba75822d315d41aad444e9b86adf5201483045022100e7e6c2d21109512ba0609e93903e84bfb7731ac3962ee2c1cad54a7a30ff99a20220421497930226c39fc3834e8d6da3fc876516239518b0e82e2dc1e3c46271a17c01695221021630971f20fa349ba940a6ba3706884c41579cd760c89901374358db5dd545b92102f2ff4b353702d2bb03d4c494be19d77d0ab53d16161b53fbcaf1afeef4ad0cb52103e9b6b1c691a12ce448f1aedbbd588e064869c79fbd760eae3b8cd8a5f1a224db53ae00000000"
    )


@pytest.mark.multisig
def test_send_multisig_2(client):
    nodes = [
        btc.get_public_node(client, parse_path(f"84'/1'/{index}'"), coin_name="Testnet")
        for index in range(1, 4)
    ]
    multisig = messages.MultisigRedeemScriptType(
        nodes=[deserialize(n.xpub) for n in nodes],
        address_n=[0, 1],
        signatures=[b"", b"", b""],
        m=2,
    )

    inp1 = messages.TxInputType(
        address_n=parse_path("84'/1'/2'/0/1"),
        prev_hash=TXHASH_f41cbe,
        prev_index=0,
        script_type=messages.InputScriptType.SPENDWITNESS,
        multisig=multisig,
        amount=1605000,
    )

    out1 = messages.TxOutputType(
        address="tb1qr6xa5v60zyt3ry9nmfew2fk5g9y3gerkjeu6xxdz7qga5kknz2ssld9z2z",
        amount=1604000,
        script_type=messages.OutputScriptType.PAYTOADDRESS,
    )

    with client:
        client.set_expected_responses(
            [
                request_input(0),
                request_output(0),
                messages.ButtonRequest(code=B.ConfirmOutput),
                messages.ButtonRequest(code=B.SignTx),
                request_input(0),
                request_meta(TXHASH_f41cbe),
                request_input(0, TXHASH_f41cbe),
                request_output(0, TXHASH_f41cbe),
                request_input(0),
                request_output(0),
                request_input(0),
                request_finished(),
            ]
        )
        signatures, _ = btc.sign_tx(client, "Testnet", [inp1], [out1], prev_txes=TX_API)
        # store signature
        inp1.multisig.signatures[1] = signatures[0]
        # sign with first key
        inp1.address_n[2] = H_(1)
        client.set_expected_responses(
            [
                request_input(0),
                request_output(0),
                messages.ButtonRequest(code=B.ConfirmOutput),
                messages.ButtonRequest(code=B.SignTx),
                request_input(0),
                request_meta(TXHASH_f41cbe),
                request_input(0, TXHASH_f41cbe),
                request_output(0, TXHASH_f41cbe),
                request_input(0),
                request_output(0),
                request_input(0),
                request_finished(),
            ]
        )
        _, serialized_tx = btc.sign_tx(
            client, "Testnet", [inp1], [out1], prev_txes=TX_API
        )

    assert (
        serialized_tx.hex()
        == "010000000001012812fe3916f228cda6c7b57d5464541265a63ad118f430a805eeec8bddbe1cf40000000000ffffffff01a0791800000000002200201e8dda334f11171190b3da72e526d441491464769679a319a2f011da5ad312a10400473044022001b7f4f21a8ddcd5e0faaaee3b95515bf8b84f2a7cbfdf66996c64123617a5cf02202fc6a776a7225420dbca759ad4ac83a61d15bf8d2883b6bf1aa31de7437f9b6e0147304402206c4125c1189a3b3e93a77cdf54c60c0538b80e5a03ec74e6ac776dfa77706ee4022035be14de76259b9d8a24863131a06a65b95df02f7d3ace90d52b37e8d94b167f0169522103bab8ecdd9ae2c51a0dc858f4c751b27533143bf6013ba1725ba8a4ecebe7de8c21027d5e55696c875308b03f2ca3d8637f51d3e35da9456a5187aa14b3de8a89534f2103b78eabaea8b3a4868be4f4bb96d6f66973f7081faa7f1cafba321444611c241e53ae00000000"
    )


@pytest.mark.multisig
def test_send_multisig_3_change(client):
    nodes = [
        btc.get_public_node(client, parse_path(f"84'/1'/{index}'"), coin_name="Testnet")
        for index in range(1, 4)
    ]
    multisig = messages.MultisigRedeemScriptType(
        nodes=[deserialize(n.xpub) for n in nodes],
        address_n=[1, 0],
        signatures=[b"", b"", b""],
        m=2,
    )
    multisig2 = messages.MultisigRedeemScriptType(
        nodes=[deserialize(n.xpub) for n in nodes],
        address_n=[1, 1],
        signatures=[b"", b"", b""],
        m=2,
    )

    inp1 = messages.TxInputType(
        address_n=parse_path("84'/1'/1'/1/0"),
        prev_hash=TXHASH_c93480,
        prev_index=0,
        script_type=messages.InputScriptType.SPENDWITNESS,
        multisig=multisig,
        amount=1604000,
    )

    out1 = messages.TxOutputType(
        address_n=parse_path("84'/1'/1'/1/1"),
        amount=1603000,
        multisig=multisig2,
        script_type=messages.OutputScriptType.PAYTOP2SHWITNESS,
    )

    with client:
        client.set_expected_responses(
            [
                request_input(0),
                request_output(0),
                messages.ButtonRequest(code=B.SignTx),
                request_input(0),
                request_meta(TXHASH_c93480),
                request_input(0, TXHASH_c93480),
                request_output(0, TXHASH_c93480),
                request_input(0),
                request_output(0),
                request_input(0),
                request_finished(),
            ]
        )
        signatures, _ = btc.sign_tx(client, "Testnet", [inp1], [out1], prev_txes=TX_API)
        # store signature
        inp1.multisig.signatures[0] = signatures[0]
        # sign with third key
        inp1.address_n[2] = H_(3)
        out1.address_n[2] = H_(3)
        client.set_expected_responses(
            [
                request_input(0),
                request_output(0),
                messages.ButtonRequest(code=B.SignTx),
                request_input(0),
                request_meta(TXHASH_c93480),
                request_input(0, TXHASH_c93480),
                request_output(0, TXHASH_c93480),
                request_input(0),
                request_output(0),
                request_input(0),
                request_finished(),
            ]
        )
        _, serialized_tx = btc.sign_tx(
            client, "Testnet", [inp1], [out1], prev_txes=TX_API
        )

    assert (
        serialized_tx.hex()
        == "01000000000101fc7901dd033f8c02da14f3ac916b6498036b80b4a0b4dc124e02c2bb408034c90000000000ffffffff01b87518000000000017a914536250d41937e5b641082447580ff6a8e46c122a870400473044022003c26107a5a47f1f900ef8aa758977530cd13ea37a33971abae8d75cac2f9f34022039e2b8c2c1d0c24ff4fc026652e1f27ad8e3ed6c9bf485f61d9aa691cb57830801483045022100963b0dc0ab46e963a66ab6e69e5e41bac6c4fedc127cac12c560b029d54fe87402205b3bcdcf313dccd78e5dce0540e7d3c8cc1bf83f13c1f9f01811eb791fd35c8101695221039dba3a72f5dc3cad17aa924b5a03c34561465f997d0cb15993f2ca2c0be771c42103cd39f3f08bbd508dce4d307d57d0c70c258c285878bfda579fa260acc738c25d2102cd631ba95beca1d64766f5540885092d0bb384a3c13b6c3a5334d0ebacf51b9553ae00000000"
    )


@pytest.mark.multisig
def test_send_multisig_4_change(client):
    nodes = [
        btc.get_public_node(client, parse_path(f"49'/1'/{index}'"), coin_name="Testnet")
        for index in range(1, 4)
    ]
    multisig = messages.MultisigRedeemScriptType(
        nodes=[deserialize(n.xpub) for n in nodes],
        address_n=[1, 1],
        signatures=[b"", b"", b""],
        m=2,
    )
    multisig2 = messages.MultisigRedeemScriptType(
        nodes=[deserialize(n.xpub) for n in nodes],
        address_n=[1, 2],
        signatures=[b"", b"", b""],
        m=2,
    )

    inp1 = messages.TxInputType(
        address_n=parse_path("49'/1'/1'/1/1"),
        prev_hash=TXHASH_31bc1c,
        prev_index=0,
        script_type=messages.InputScriptType.SPENDP2SHWITNESS,
        multisig=multisig,
        amount=1603000,
    )

    out1 = messages.TxOutputType(
        address_n=parse_path("49'/1'/1'/1/2"),
        amount=1602000,
        multisig=multisig2,
        script_type=messages.OutputScriptType.PAYTOWITNESS,
    )

    with client:
        client.set_expected_responses(
            [
                request_input(0),
                request_output(0),
                messages.ButtonRequest(code=B.SignTx),
                request_input(0),
                request_meta(TXHASH_31bc1c),
                request_input(0, TXHASH_31bc1c),
                request_output(0, TXHASH_31bc1c),
                request_input(0),
                request_output(0),
                request_input(0),
                request_finished(),
            ]
        )
        signatures, _ = btc.sign_tx(client, "Testnet", [inp1], [out1], prev_txes=TX_API)
        # store signature
        inp1.multisig.signatures[0] = signatures[0]
        # sign with third key
        inp1.address_n[2] = H_(3)
        out1.address_n[2] = H_(3)
        client.set_expected_responses(
            [
                request_input(0),
                request_output(0),
                messages.ButtonRequest(code=B.SignTx),
                request_input(0),
                request_meta(TXHASH_31bc1c),
                request_input(0, TXHASH_31bc1c),
                request_output(0, TXHASH_31bc1c),
                request_input(0),
                request_output(0),
                request_input(0),
                request_finished(),
            ]
        )
        _, serialized_tx = btc.sign_tx(
            client, "Testnet", [inp1], [out1], prev_txes=TX_API
        )

    assert (
        serialized_tx.hex()
        == "01000000000101e5918f661488bb7f0a7d04fc1dad61b5d0bad5167a05b3a637e36ace881cbc310000000023220020fa6c73de618ec134eeec0c16f6dd04d46d4347e9a4fd0a95fd7938403a4949f9ffffffff01d071180000000000220020bcea2324dacbcde5a9db90cc26b8df9cbc72010e05cb68cf034df6f0e05239a2040047304402206bbddb45f12e31e77610fd85b50a83bad4426433b1c4860b1c5ddc0a69f803720220087b0607daab14830f4b4941f16b953b38e606ad70029bac24af7267f93c4242014730440220551a0cb6b0d5b3fa0cfd0b07bb5d751494b827b1c6a08702186696cfbc18278302204f37c382876c4117cca656654599b508f2d55fc3b083dc938e3cd8491b29719601695221036a5ec3abd10501409092246fe59c6d7a15fff1a933479483c3ba98b866c5b9742103559be875179d44e438db2c74de26e0bc9842cbdefd16018eae8a2ed989e474722103067b56aad037cd8b5f569b21f9025b76470a72dc69457813d2b76e98dc0cd01a53ae00000000"
    )


# Ensure that if there is a non-multisig input, then a multisig output
# will not be identified as a change output.
def test_multisig_mismatch_inputs_single(client):
    # m/84'/1'/0' for "alcohol woman abuse ..." seed.
    node_int = deserialize(
        "Vpub5kFDCYhiYuAzjk7TBQPNFffbexHF7iAd8AVVgHQKUany7e6NQvthgk86d7DfH57DY2dwBK4PyVTDDaS1r2gjkdyJyUYGoV9qNujGSrW9Dpe"
    )

    # m/84'/1'/0' for "all all ... all" seed.
    node_ext = deserialize(
        "Vpub5jR76XyyhBaQXPSRf3PBeY3gF914d9sf7DWFVhMESEQMCdNv35XiVvp8gZsFXAv222VPHLNnAEXxMPG8DPiSuhAXfEydBf55LTLBGHCDzH2"
    )

    # tb1qpzmgzpcumztvmpu3q27wwdggqav26j9dgks92pvnne2lz9ferxgssmhzlq
    multisig_in = messages.MultisigRedeemScriptType(
        nodes=[node_int, node_ext], address_n=[0, 0], signatures=[b"", b""], m=1
    )

    multisig_out = messages.MultisigRedeemScriptType(
        nodes=[node_int, node_ext], address_n=[1, 0], signatures=[b"", b""], m=1
    )

    inp1 = messages.TxInputType(
        address_n=parse_path("84'/1'/0'/0/0"),
        amount=12300000,
        prev_hash=TXHASH_091446,
        prev_index=0,
        script_type=messages.InputScriptType.SPENDWITNESS,
    )

    inp2 = messages.TxInputType(
        address_n=parse_path("84'/1'/0'/0/0"),
        prev_hash=TXHASH_a345b8,
        prev_index=0,
        script_type=messages.InputScriptType.SPENDWITNESS,
        multisig=multisig_in,
        amount=100,
    )

    out1 = messages.TxOutputType(
        address="2N4Q5FhU2497BryFfUgbqkAJE87aKHUhXMp",
        amount=5000000,
        script_type=messages.OutputScriptType.PAYTOADDRESS,
    )

    out2 = messages.TxOutputType(
        address_n=parse_path("84'/1'/0'/1/0"),
        script_type=messages.OutputScriptType.PAYTOWITNESS,
        multisig=multisig_out,
        amount=12300000 + 100 - 5000000 - 10000,
    )

    with client:
        client.set_expected_responses(
            [
                request_input(0),
                request_input(1),
                request_output(0),
                messages.ButtonRequest(code=B.ConfirmOutput),
                request_output(1),
                # Ensure that the multisig output is not identified as a change output.
                messages.ButtonRequest(code=B.ConfirmOutput),
                messages.ButtonRequest(code=B.SignTx),
                request_input(0),
                request_meta(TXHASH_091446),
                request_input(0, TXHASH_091446),
                request_output(0, TXHASH_091446),
                request_output(1, TXHASH_091446),
                request_input(1),
                request_meta(TXHASH_a345b8),
                request_input(0, TXHASH_a345b8),
                request_output(0, TXHASH_a345b8),
                request_input(0),
                request_input(1),
                request_output(0),
                request_output(1),
                request_input(0),
                request_input(1),
                request_finished(),
            ]
        )

        _, serialized_tx = btc.sign_tx(
            client, "Testnet", [inp1, inp2], [out1, out2], prev_txes=TX_API
        )

    assert (
        serialized_tx.hex()
        == "010000000001028a44999c07bba32df1cacdc50987944e68e3205b4429438fdde35c76024614090000000000ffffffff48e37c58a68ab4899400dc0950a661817ea7bac3e4556044c685b35957b845a30000000000ffffffff02404b4c000000000017a9147a55d61848e77ca266e79a39bfc85c580a6426c987f43c6f0000000000220020733ecfbbe7e47a74dde6c7645b60cdf627e90a585cde7733bc7fdaf9fe30b37402473044022037dc98b16be542a6e3e1ab32007a74192c43f2498170cc5e1dffb6847e3663e402206715102d0eb59e6461a97c78eb40a8679a04a8921fdafef25f0d3d16cc65de39012103adc58245cf28406af0ef5cc24b8afba7f1be6c72f279b642d85c48798685f8620300473044022070a24bcb00041cbed465f1f546bc59e1e353a6e182393932d5ba96e20bc32ef702202ddc76a97c01465692d5b0a0a61d653f64b9ea833af1810022110fd4d505ff950147512103505f0d82bbdd251511591b34f36ad5eea37d3220c2b81a1189084431ddb3aa3d2103adc58245cf28406af0ef5cc24b8afba7f1be6c72f279b642d85c48798685f86252ae00000000"
    )
