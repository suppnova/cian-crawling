import re

regs = [r"м\.[^,]*,", r"мкр\.[^,]*,", r"р-н", r"пос.", r"улица"]


def process_address(raw_address):
    address = raw_address
    for reg in regs:
        address = re.sub(reg, "", address)
    return address
