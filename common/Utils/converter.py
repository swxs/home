from api.consts.const import undefined


def optional(converter):
    """
    A converter that allows an attribute to be optional. An optional attribute
    is one which can be set to ``None``.

    :param callable converter: the converter that is used for non-``None``
        values.
    """

    def optional_converter(val):
        if val is None:
            return None
        if val == undefined:
            raise ApiValidateException(val)
        return converter(val)

    return optional_converter
