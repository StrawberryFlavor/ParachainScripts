# -*- coding: utf-8 -*-
# @Time : 2021/6/25 15:02
# @Author : Joey
import sys
import os
import json

from ..utils import command


def readJson():
    config_path = os.path.dirname(os.path.abspath('.')) + '/ParachainScripts/config.json'
    config = json.loads(open(config_path).read())
    return config


def readFile(path):
    with open("r", path) as reader:
        resp = reader.read()
        reader.close()
        return resp


def writeFile(path, content):
    with open("w", path) as writer:
        writer.write(content)
        writer.close()


def start():
    config = readJson()
    relayCli = config["relaychain"]['bin']
    relayChain = config["relaychain"]['chain']
    relayNodes = config['relaychain']['nodes']

    shell = "{relayCli} build-spec --chain {relayChain}  --disable-default-bootnode --raw > {relayChain}.json".format(relayCli=relayCli,
                                                                                                                      relayChain=relayChain)
    print(shell)
    command.sub_command(shell)

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
        command.sub_command(shell)

    parachains = config["parachains"]
    for parachain in parachains:
        parachainCli = parachain['bin']
        parachainChain = parachain['chain']
        parachainId = parachain['id']
        parachainRoot = parachain['root']
        parachainAura = parachain['aura']

        shell = "{relayCli} build-spec --disable-default-bootnode --chain {parachainChain} > {parachainChain}.json".format(relayCli=relayCli, parachainChain=parachainChain)
        print(shell)
        command.sub_command(shell)

        resp = readFile("{parachainChain}.json".format(parachainChain=parachainChain))
        resp = json.dumps(resp)
        resp.bootNodes = []
        runtime = resp['genesis']['runtime']
        runtime['parachainInfo']['parachainId'] = parachainId
        runtime['sudo']['key'] = parachainRoot
        runtime['collatorSelection']['invulnerables'] = parachainAura
        balancesList = runtime['palletBalances']['balances']
        balancesList.append([parachainRoot, 100000000000000000])

        keys = []
        for aura in parachainAura:
            data = [aura, aura, {"aura": aura}]
            keys.append(data)
            balancesList.append([aura, 100000000000000000])

        runtime['palletSession']['keys'] = keys

        writeFile("{parachainChain}.json".format(parachainChain=parachainChain), resp)

        shell = "{parachainCli} export-genesis-state --parachain-id {parachainId} --chain {parachainChain} > genesis-state".format(
            parachainCli=parachainCli, parachainId=parachainId, parachainChain=parachainChain)
        print(shell)
        command.sub_command(shell)

        shell = "{parachainCli} export-genesis-wasm --chain {parachainChain} > genesis-wasm".format(parachainCli=parachainCli,
                                                                                                    parachainChain=parachainChain)
        print(shell)
        command.sub_command(shell)

    return


if __name__ == '__main__':
    start()

