from typing import Optional
import logging
from fwsim.lexer.lexer import Lexer
from fwsim.ast.ast import Chain, ChainType, Config, Family, HookType, IpAddr, IpField, IpRule, Item, PolicyType, Ruleset, TableBlock
from fwsim.lexer.tokens import TokenType


class Parser:
    lexer: Lexer

    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer

    def parse(self) -> Optional[Ruleset]:
        ruleset = Ruleset()

        while True:
            peek = self.lexer.peek()

            if peek is None:
                return ruleset

            table_block = self._parse_table_block()
            ruleset.table_blocks.append(table_block)


    def _parse_table_block(self) -> TableBlock:
        # TABLE family IDENTIFIER L_CURLY chain* R_CURLY

        _ = self.lexer.chomp(TokenType.IDENTIFIER, 'table')
        family = self._parse_family()
        ident = self._parse_ident()
        _ = self.lexer.chomp(TokenType.L_CURLY)

        chains = self._parse_chains()

        _ = self.lexer.chomp(TokenType.R_CURLY)

        return TableBlock(family, ident, chains)

    def _parse_chains(self) -> list[Chain]:
        chains = []

        while True:
            peek = self.lexer.peek()
            if peek is None:
                raise RuntimeError("None peek when parsing chain")

            if peek.is_type(TokenType.R_CURLY):
                return chains

            chains.append(self._parse_chain())

    def _parse_chain(self) -> Chain:
        _ = self.lexer.chomp(TokenType.IDENTIFIER, 'chain')
        ident = self._parse_ident()
        _ = self.lexer.chomp(TokenType.L_CURLY)


        config = self._parse_config()
        items = self._parse_items()
        
        _ = self.lexer.chomp(TokenType.R_CURLY)

        ret = Chain(ident, config, items)
        logging.debug(f'parsed chain definition: {ret}')
        return ret

    def _parse_item(self) -> Item:
        policies = {"accept": PolicyType.ACCEPT, "drop": PolicyType.DROP}

        peek = self.lexer.peek()

        if peek is None:
            raise RuntimeError("expected policy or rule, got None")

        if peek.is_type(TokenType.IDENTIFIER) and peek.value in policies:
            _ = self.lexer.chomp(TokenType.IDENTIFIER, peek.value)
            return Item(None,policies[peek.value])

        rule_types = {"ip":self._parse_ip_rule}

        if peek.value in rule_types:
            rule = rule_types[peek.value]()
            
            policy = self.lexer.chomp(TokenType.IDENTIFIER).value
            if policy not in policies:
                raise RuntimeError(f"expected policy, got {policy}")

            ret = Item(rule, policies[policy])
            logging.debug(f'parsed item definition: {ret}')
            return ret

        raise RuntimeError(f"expected item, got {peek}")

    def _parse_ip_rule(self) -> IpRule:
        _ = self.lexer.chomp(TokenType.IDENTIFIER, 'ip')
        field = self._parse_ip_field()
        addr = self._parse_ipv4_addr()

        ret = IpRule(field, addr)
        logging.debug(f'parsed ipv4 rule: {ret}')
        return ret

    # TODO: rename type to Ipv4Addr
    def _parse_ipv4_addr(self) -> IpAddr:
        def byte_invalid(a: int) -> bool:
            return a < 0 or a > 255

        a = int(self.lexer.chomp(TokenType.INTEGER_LITERAL).value)
        _ = self.lexer.chomp(TokenType.DOT)
        b =int( self.lexer.chomp(TokenType.INTEGER_LITERAL).value)
        _ = self.lexer.chomp(TokenType.DOT)
        c =int( self.lexer.chomp(TokenType.INTEGER_LITERAL).value)
        _ = self.lexer.chomp(TokenType.DOT)
        d =int( self.lexer.chomp(TokenType.INTEGER_LITERAL).value)

        if any(byte_invalid(byte) for byte in [a,b,c,d]):
            raise RuntimeError(f"expected IPv4 address, got {a}.{b}.{c}.{d}")

        peek = self.lexer.peek()
        if peek is None:
            raise RuntimeError("unexpected None when lexing")

        if peek.is_type(TokenType.FORWARD_SLASH):
            _ = self.lexer.chomp(TokenType.FORWARD_SLASH)
            subnet_mask = int(self.lexer.chomp(TokenType.INTEGER_LITERAL).value)

            ret = IpAddr((a,b,c,d), subnet_mask)
            logging.debug(f'parsed ipv4 address: {ret}')
            return ret

        ret = IpAddr((a,b,c,d),None)
        logging.debug(f'parsed ipv4 address: {ret}')
        return ret

    def _parse_ip_field(self) -> IpField:
        peek = self.lexer.next()
        if peek is None:
            raise RuntimeError("expected IP field, got None")

        fields = {"saddr": IpField.SADDR, "daddr": IpField.DADDR}

        if peek.value in fields:
            ret = fields[peek.value]
            logging.debug(f'parsed IP field: {ret}')
            return ret

        raise RuntimeError(f"expected IP field, got {peek}")


    def _parse_items(self) -> list[Item]:
        items = []

        while True:
            peek = self.lexer.peek()
            if peek is None:
                raise RuntimeError("None peek when parsing item")

            if peek.is_type(TokenType.R_CURLY):
                return items

            items.append(self._parse_item())


    def _parse_config(self) -> Config:
        _ = self.lexer.chomp(TokenType.IDENTIFIER, 'type')
        chain_type = self._parse_chain_type()

        _ = self.lexer.chomp(TokenType.IDENTIFIER, 'hook')
        hook_type = self._parse_hook_type()

        _ = self.lexer.chomp(TokenType.IDENTIFIER, 'priority')
        priority = int(self.lexer.chomp(TokenType.INTEGER_LITERAL).value)

        _ = self.lexer.chomp(TokenType.SEMI_COLON)
        
        ret = Config(chain_type, hook_type, priority,None)
        logging.debug(f'parsed chain config: {ret}')
        return ret
        
    def _parse_chain_type(self) -> ChainType:
        peek = self.lexer.chomp(TokenType.IDENTIFIER)
        if peek is None:
            raise RuntimeError("expected chain type, got None")

        if peek.value == "filter":
            ret = ChainType.FILTER
            logging.debug(f'parsed chain type: {ret}')
            return ret

        raise RuntimeError(f"expected family, got {peek}")

    def _parse_hook_type(self) -> HookType:
        peek = self.lexer.chomp(TokenType.IDENTIFIER)
        if peek is None:
            raise RuntimeError("expected hook type, got None")

        hooks = {"input":HookType.INPUT,"output":HookType.OUTPUT,"forward":HookType.FORWARD,"prerouting":HookType.PRE_ROUTING,"postrouting":HookType.POST_ROUTING} 

        if peek.value in hooks:
            ret = hooks[peek.value]
            logging.debug(f'parsed chain hook type: {ret}')
            return ret

        raise RuntimeError("expected hook type, got {peek}")


    def _parse_ident(self) -> str:
        got = self.lexer.chomp(TokenType.IDENTIFIER)

        ret = got.value
        logging.debug(f'parsing identifier: {ret}')
        return ret

    def _parse_family(self) -> Family:
        peek = self.lexer.next()
        if peek is None:
            raise RuntimeError("expected family, got None")

        families = {"ip":Family.IP,"inet":Family.INET,"ip6":Family.IP6}

        if peek.value in families:
            ret = families[peek.value]
            logging.debug(f'parsing table family: {ret}')
            return ret

        raise RuntimeError(f"expected family, got {peek}")


