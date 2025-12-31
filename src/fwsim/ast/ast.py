from abc import ABC
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, Tuple


class Node(ABC):
    ...

class Family(Enum):
    IP = auto()
    INET = auto()
    IP6 = auto()

class ChainType(Enum):
    FILTER = auto()

class HookType(Enum):
    INPUT = auto()
    OUTPUT = auto()
    FORWARD = auto()
    PRE_ROUTING = auto()
    POST_ROUTING = auto()

class PolicyType(Enum):
    ACCEPT = auto()
    DROP = auto()

@dataclass
class Config(Node):
    chain_type: ChainType
    hook_type: HookType
    priority: int
    policy: Optional[PolicyType]

class Rule(Node):
    ...

class IpField(Enum):
    SADDR = auto()
    DADDR = auto()

@dataclass
class IpAddr(Node):
    value: Tuple[int,int,int,int]
    mask: Optional[int]

@dataclass
class IpRule(Rule):
    field: IpField
    addr: IpAddr
    
class Protocol(Enum):
    TCP = auto()
    UDP = auto()

class PortField(Enum):
    SPORT = auto()
    DPORT = auto()

@dataclass
class ProtoRule(Rule):
    protocol: Protocol
    field: PortField
    port: int

@dataclass
class Item(Node):
    rule: Optional[Rule]
    policy: PolicyType

@dataclass
class Chain(Node):
    ident: str
    config: Config
    rules: list[Item]

@dataclass
class TableBlock(Node):
    family: Family
    ident: str
    chains: list[Chain]

@dataclass
class Ruleset(Node):
    table_blocks: list[TableBlock] = field(default_factory=list)
