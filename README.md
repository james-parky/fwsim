# `fwsim`

A command line tool for simulating a packet passing through a firewall.

---




## TODO

- [ ] Parse NFT rules.
- [ ] Collect packets from `tshark` output in JSON.
- [ ] Take command line arguments for NFT ruleset file and packet file.

### Further Work

- [ ] Take packets from a JSON stream.
- [ ] Handle `tcpdump`, non-JSON `tshark`, and `pcap` outputs.
- [ ] Handle parsing FaC file formats other than NFT.


### Links

- [NFT](https://wiki.nftables.org/wiki-nftables/index.php/Main_Page)
- [Tshark Packet Format](https://tshark.dev/formats/)
- [`argparse`](https://docs.python.org/3/library/argparse.html)
- [`json`](https://docs.python.org/3/library/json.html)
- [`black`](https://pypi.org/project/black/)
- [`abc`](https://docs.python.org/3/library/abc.html)
