from typing import List, Dict
from dataclasses import dataclass
from copy import deepcopy
from zetsubou.project.model.config_string import EDefaultConfigSlots

from zetsubou.utils import logger


@dataclass
class ConfigVariant:
    config_string: str
    slots: Dict[str, str]

    def get_slot(self, slot):
        if isinstance(slot, EDefaultConfigSlots):
            return self.slots[slot.name]
        return self.slots[slot]


def get_config_matrix_os_name(config_string: str):
    return config_string.replace('-', '_')


@dataclass
class ConfigMatrix:
    variants: List[ConfigVariant]
    slots: List[str]

    def find_variants(self, data: dict):
        results = []

        for variant in self.variants:
            is_variant_ok = True

            for filter_name, filter_value in data.items():
                if filter_name not in self.slots:
                    raise ValueError(f"Unknown slot '{filter_name}'")

                val = variant.get_slot(filter_name)
                if val != filter_value:
                    is_variant_ok = False

            if is_variant_ok:
                results.append(variant)

        return results


    def get_config_name(self, pattern : str, variant : str):
        if isinstance(pattern, EDefaultConfigSlots):
            pattern = pattern.name

        pattern_slots = pattern.split('-')
        variant_slots = variant.split('-')
        out_values = []

        for slot in pattern_slots:
            if slot not in self.slots:
                raise ValueError(f"No slot '{slot}' in config matrix! Available slots: {self.slots}")
            slot_index = self.slots.index(slot)
            out_values.append(variant_slots[slot_index])

        return '-'.join(out_values)


def parse_config_string(conf: str):
    slot_defs = conf.split('-')
    result = []

    if len(slot_defs) == 0:
        return None

    for slot in slot_defs:
        if slot[0] != '{' or slot[len(slot) - 1] != '}':
            continue
        result.append(slot[1:len(slot)-1])

    return result

def create_config_matrix(config_string:str, domain:list) -> ConfigMatrix:
    slots = parse_config_string(config_string)
    config_variants = []

    # domain = [
    #     ['pc', 'xbox', 'orbis'],
    #     ['Debug', 'Release' , 'Hybrid', 'ReleaseWithProfiler'],
    #     ['clang', 'msvc'],
    #     ['x86', 'x64'],
    #     ['none', 'memdump', 'asan']
    # ]

    template = config_string

    for slot_name, values in domain.items():
        if len(values) == 0:
            logger.CriticalError(f'Unable to build list of values for slot \'{slot_name}\'')
            return None

    for slot_name, _ in domain.items():
        if slot_name not in slots:
            domain.pop(slot_name)

    def RecurseBuildVariants(slot_itr:int=0, field_values={}):
        if slot_itr >= len(domain):
            config_variants.append(ConfigVariant(
                config_string=template.format(**field_values),
                slots=deepcopy(field_values)
            ))
        else:
            key, values = list(domain.items())[slot_itr]
            for val in values:
                field_values[key] = val
                RecurseBuildVariants(slot_itr+1, field_values)

    RecurseBuildVariants()

    # for variant in config_variants:
    #     logger.Info(variant.config_string)

    return ConfigMatrix(variants=config_variants, slots=slots)

    # val = []
    # for f in range(len(domain[0])):
    #     val[0] = domain[0][f]
    #     for v in range(len(domain[1])):
    #         val[1] = domain[1][v]
    #         for x in range(len(domain[2])):
    #             print(f'[{f}]-[{v}]-[{x}]')


    # for slot in slots:
    #     slot_matrix[slot] = get_slot_values(proj, slot)

    # for slot in slots:
    #     for value in slot:

    