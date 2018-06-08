from collections import namedtuple

_WITH_ = 'with_'

_WITHOUT_ = 'without_'

_WITHOUT_FLAG = _WITHOUT_ + 'flag'

_WITH_FLAG = _WITH_ + 'flag'

_TO_MASK = 'to_mask'

_FROM_MASK = 'from_mask'


def bit_mask_class(name, fields):
    try:
        fields = fields.replace(',', ' ').split()
    except AttributeError:
        pass

    fields = tuple(fields)

    _validate_fields(fields)

    base = namedtuple(name, fields)
    base.FIELDS = fields

    def from_mask(cls, mask):
        values = []
        for index in range(1, len(fields) + 1):
            value = (index & mask) > 0
            values.append(value)

        return cls(*values)

    def to_mask(self):
        number = 0
        for index, value in enumerate(self, start=1):
            if value:
                number = number | index

        return number

    def with_flag(self, _name):
        return self._replace(**{_name: True})

    def without_flag(self, _name):
        return self._replace(**{_name: False})

    methods = {
        _FROM_MASK: classmethod(from_mask),
        _TO_MASK: to_mask,
        _WITH_FLAG: with_flag,
        _WITHOUT_FLAG: without_flag
    }

    for field in fields:
        def with_method(self):
            return self.with_flag(field)

        def without_method(self):
            return self.without_flag(field)

        with_name = _WITH_ + field
        without_name = _WITHOUT_ + field
        methods.update({
            with_name: with_method,
            without_name: without_method
        })

    # noinspection PyTypeChecker
    return type(name, (base, ), methods)


def _value_error(text):
    raise ValueError(f'Cannot create bit_mask_class: {text}')


def _value_assertion(condition, text):
    if not condition:
        _value_error(text)


def _validate_fields(fields):
    for field in fields:
        _value_assertion(field.isidentifier(), f'{field} is not a valid python identifier')
        _value_assertion(not field == 'to_mask', f'{field} is a reserved name')
        _value_assertion(not field.startswith('with_'), f'{field} starts with "with_" which is reserved')
        _value_assertion(not field.startswith('without_'), f'{field} starts with "without" which is reserved')
