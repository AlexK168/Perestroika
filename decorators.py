from glob import GlobalState


def decorator(function_to_decorate):
    def wrapper_func(bracing, blocks, tower, builder, block):
        function_to_decorate(bracing, blocks, tower, builder, block)
        if GlobalState().over and not GlobalState().falling and GlobalState().score > GlobalState().record.score:
            GlobalState().record.score = GlobalState().score
            GlobalState().record.save()
            GlobalState().score = 0
    return wrapper_func

