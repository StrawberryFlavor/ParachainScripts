# -*- coding: utf-8 -*-
# @Time : 2021/6/25 15:02
# @Author : Joey
from src.utils import command

import os
import json


def environmental(ip_info=None):
    print()


def readJson():
    config_path = os.path.dirname(os.path.abspath('..')) + '/config.json'
    config = json.loads(open(config_path).read())
    return config


def start(ip_info=None):
    config = readJson()
    relayCli = config["relaychain"]['bin']
    relayChain = config["relaychain"]['chain']
    relayNodes = config['relaychain']['nodes']

    shell = "{relayCli} build-spec --chain {relayChain}  --disable-default-bootnode --raw > {relayChain}.json".format(relayCli=relayCli,
                                                                                                                      relayChain=relayChain)
    print(shell)

    for relayNode in relayNodes:
        relayNodeName = relayNode['name']
        relayNodeWsPort = relayNode['wsPort']
        relayNodePort = relayNode['port']

        relayNodeFlags = ''
        for flag in relayNode['flags']:
            relayNodeFlags = relayNodeFlags + flag

        shell = "{relayCli} --chain {relayChain} --{relayNodeName} --ws-port {relayNodeWsPort} {relayNodeFlags}".format(relayCli=relayCli,
                                                                                                                        relayChain=relayChain,
                                                                                                                        relayNodeName=relayNodeName,
                                                                                                                        relayNodeWsPort=relayNodeWsPort,
                                                                                                                        relayNodeFlags=relayNodeFlags)
        print(shell)

    parachains = config["parachains"]
    for parachain in parachains:
        parachainCli = parachain['bin']
        parachainChain = parachain['chain']
        parachainId = parachain['id']
        parachainRoot = parachain['root']
        parachainAura = parachain['aura']

        shell = "{parachainCli} export-genesis-state --parachain-id {parachainId} --chain {parachainChain} > genesis-state".format(
            parachainCli=parachainCli, parachainId=parachainId, parachainChain=parachainChain)
        print(shell)

        shell = "{parachainCli} export-genesis-wasm --chain {parachainChain} > genesis-wasm".format(parachainCli=parachainCli,
                                                                                                    parachainChain=parachainChain)
        print(shell)

    return


if __name__ == '__main__':
    start()
    print()
