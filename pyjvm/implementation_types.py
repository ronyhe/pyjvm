from collections import namedtuple

_names_to_letters = {
    'Integer': 'I',
    'Float': 'F',
    'Double': 'D',
    'Long': 'J',
    'Reference': 'L'
}

_Kind = namedtuple('_Kind', 'name, letter')


class Kind(_Kind):
    @classmethod
    def from_letter(cls, letter):
        pass