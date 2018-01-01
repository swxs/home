

def single_or_muliteple(function):
    def helper(*args, **kwargs):
        ret_obj = function(*args, **kwargs)
        return ret_obj
    return helper
