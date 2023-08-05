#!/usr/bin/python3
# -*- coding: utf-8 -*-


from dataclasses import dataclass

from slpkg.queries import SBoQueries
from slpkg.configs import Configs


@dataclass
class SearchPackage:
    colors: dict = Configs.colour

    def package(self, packages):
        color = self.colors()
        CYAN = color['CYAN']
        ENDC = color['ENDC']

        names = SBoQueries('').names()

        print(f'The list below shows the packages '
              f'that contains \'{", ".join([p for p in packages])}\' files:\n')

        for name in names:
            for package in packages:
                if package in name:
                    desc = SBoQueries(name).description().replace(name, '')
                    print(f'{name}-{SBoQueries(name).version()}'
                          f'{CYAN}{desc}{ENDC}')
