from typing import Dict, List, Set
from parsers.accounts.jetton_wallets_recover import JettonWalletsRecover
from parsers.accounts.nfts_recover import NFTsRecover
from parsers.message_contents.decode_comment import CommentsDecoder
from parsers.accounts.core_prices import CorePricesLSDstTON, CorePricesLSDtsTON, CorePricesUSDT
from parsers.message.dedust_swap import DedustSwap
from parsers.message.stonfi_swap import StonfiSwap
from parsers.nft_transfer.nft_history import NftHistoryParser
from model.parser import Parser
from loguru import logger
import os

EMULATOR_PATH = os.environ.get("EMULATOR_LIBRARY")

_parsers = [
    DedustSwap(),
    NftHistoryParser(),
    StonfiSwap(),

    CorePricesUSDT(),
    CorePricesLSDstTON(),
    CorePricesLSDtsTON(),

    NFTsRecover(EMULATOR_PATH),
    JettonWalletsRecover(EMULATOR_PATH),
    
    CommentsDecoder()
]

"""
dict of parsers, where key is the topic name
"""
def generate_parsers(names: Set)-> Dict[str, List[Parser]]: 
    out: Dict[str, List[Parser]] = {}

    for parser in _parsers:
        if names is not None:
            if type(parser).__name__ not in names:
                logger.info(f"Skipping parser {parser}, it is not in supported parsers list")
                continue
            else:
                logger.info(f"Adding parser {parser}: {type(parser).__name__}, {names}")
        for topic in parser.topics():
            if topic not in out:
                out[topic] = []
            out[topic].append(parser)
    return out
