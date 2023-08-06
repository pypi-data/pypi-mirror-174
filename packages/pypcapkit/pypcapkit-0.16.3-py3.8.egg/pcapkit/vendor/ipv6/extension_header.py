# -*- coding: utf-8 -*-
"""IPv6 Extension Header Types
=================================

This module contains the vendor crawler for **IPv6 Extension Header Types**,
which is automatically generating :class:`pcapkit.const.ipv6.extension_header.ExtensionHeader`.

"""

import collections
import csv
import re
import sys
from typing import TYPE_CHECKING

from pcapkit.vendor.default import Vendor

if TYPE_CHECKING:
    from collections import Counter
    from typing import Callable

__all__ = ['ExtensionHeader']



def _walrus_wrapper_lambda_f19bc391a72f4f87a8668d906db61d52( NAME, DOCS, ENUM, MODL):
    """Wrapper function for lambda definitions."""
    if False:
        name = NotImplemented

    def _walrus_wrapper_name_d0d68e970cbf4f51b6b5c6f2681dde13(expr):
        """Wrapper function for assignment expression."""
        nonlocal name
        name = expr
        return name

    return f'''\
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long,consider-using-f-string
"""{(_walrus_wrapper_name_d0d68e970cbf4f51b6b5c6f2681dde13(DOCS.split(' [', maxsplit=1)[0]))}
{'=' * (len(name) + 6)}

This module contains the constant enumeration for **{name}**,
which is automatically generated from :class:`{MODL}.{NAME}`.

"""

from aenum import IntEnum, extend_enum

__all__ = ['{NAME}']


class {NAME}(IntEnum):
    """[{NAME}] {DOCS}"""

    {ENUM}

    @staticmethod
    def get(key: 'int | str', default: 'int' = -1) -> '{NAME}':
        """Backport support for original codes."""
        if isinstance(key, int):
            return {NAME}(key)
        return {NAME}[key]  # type: ignore[misc]
'''

LINE =_walrus_wrapper_lambda_f19bc391a72f4f87a8668d906db61d52  # type: Callable[[str, str, str, str], str]


class ExtensionHeader(Vendor):
    """IPv6 Extension Header Types"""

    #: Link to registry.
    LINK = 'https://www.iana.org/assignments/protocol-numbers/protocol-numbers-1.csv'

    def count(self, data: 'list[str]') -> 'Counter[str]':
        """Count field records.

        Args:
            data: CSV data.

        Returns:
            Field recordings.

        """
        reader = csv.reader(data)
        next(reader)  # header
        return collections.Counter(map(lambda item: self.safe_name(item[1] or item[2]),
                                       filter(lambda item: len(item[0].split('-')) != 2, reader)))

    def process(self, data: 'list[str]') -> 'tuple[list[str], list[str]]':
        """Process CSV data.

        Args:
            data: CSV data.

        Returns:
            Enumeration fields and missing fields.

        """
        reader = csv.reader(data)
        next(reader)  # header

        enum = []  # type: list[str]
        miss = []  # type: list[str]
        for item in reader:
            flag = item[3]
            if flag != 'Y':
                continue

            name = item[1]
            rfcs = item[4]

            temp = []  # type: list[str]
            for rfc in filter(None, re.split(r'\[|\]', rfcs)):
                if 'RFC' in rfc and re.match(r'\d+', rfc[3:]):
                    #temp.append(f'[{rfc[:3]} {rfc[3:]}]')
                    temp.append(f'[:rfc:`{rfc[3:]}`]')
                else:
                    temp.append(f'[{rfc}]'.replace('_', ' '))
            lrfc = re.sub(r'( )( )*', ' ', f" {''.join(temp)}".replace('\n', ' ')) if rfcs else ''

            subd = re.sub(r'( )( )*', ' ', item[2].replace('\n', ' '))
            tmp1 = f' {subd}' if item[2] else ''

            split = name.split(' (', 1)
            if len(split) == 2:
                name, cmmt = split[0], f" ({split[1]}"
            else:
                name, cmmt = name, ''  # pylint: disable=self-assigning-variable

            if name:
                tmp1 = f',{tmp1}' if tmp1 else ''
            else:
                name, tmp1 = item[2], ''
            desc = self.wrap_comment(f'{name}{tmp1}{lrfc}{cmmt}')

            try:
                code, _ = item[0], int(item[0])
                if not name:
                    name, desc = item[2], ''
                renm = self.rename(name, code, original=item[1])

                pres = f"{renm} = {code}"
                sufs = f"#: {desc}"

                #if len(pres) > 74:
                #    sufs = f"\n{' '*80}{sufs}"

                #enum.append(f'{pres.ljust(76)}{sufs}')
                enum.append(f'{sufs}\n    {pres}')
            except ValueError:
                start, stop = item[0].split('-')

                miss.append(f'if {start} <= value <= {stop}:')
                miss.append(f'    #: {desc}')
                miss.append(f"    extend_enum(cls, '{self.safe_name(name)}_%d' % value, value)")
                miss.append('    return cls(value)')
        return enum, miss

    def context(self, data: 'list[str]') -> 'str':
        """Generate constant context.

        Args:
            data: CSV data.

        Returns:
            Constant context.

        """
        enum, _ = self.process(data)
        ENUM = '\n\n    '.join(map(lambda s: s.rstrip(), enum))
        return LINE(self.NAME, self.DOCS, ENUM, self.__module__)


if __name__ == '__main__':
    sys.exit(ExtensionHeader())
