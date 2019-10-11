from configparser import ConfigParser
from typing import Union, Optional


def parse(filename: str, section: str = None, entry: str = None, unwanted_fields=tuple()) -> Union[dict, Optional[str]]:
    """read config with the given sector

    :param filename: path to ini config file
    :param section: section name, if provided, will return a dictionary of the section's entries
                                  if not provided, will return the dictionary contain all sections
    :param entry: entry name, if provided, will return the value of that entry in the section
    :param unwanted_fields: remove the unwanted fields from the returned dict
    :return dictionary of a section if specified, or
            entry of a section if specified (in type str), or
            dictionary of the whole parser if neither section and entry are provided

    :raise KeyError if section is not found in the parser
           KeyError if the entry is not found in the section
    """
    config = ConfigParser()
    config.read(filename)
    if entry and not section:
        raise ValueError(f'Entry {entry} fail to lookup since Section {section} is not found in the {filename} file')

    if section and config.has_section(section):
        if entry:
            result = dict(config.items(section))[entry]
        else:
            result = dict(config.items(section))
    elif not section:
        result = {s: dict(config.items(s)) for s in config.sections()}
    else:
        raise KeyError(f'Section {section} not found in the {filename} file')
    for field in unwanted_fields:
        del result[field]
    return result


if __name__ == '__main__':
    # without a specific section name or entry name
    entry = parse('some-dir/some.ini')['section_name']['entry_name']
    print(entry)

    # with a specific section name but no entry name
    entry = parse('some-dir/some.ini', 'section_name')['entry_name']
    print(entry)

    # with a specific section name and entry name
    entry = parse('some-dir/some.ini', 'section_name', 'entry_name')
    print(entry)
