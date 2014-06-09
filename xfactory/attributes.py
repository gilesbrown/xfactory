from types import GeneratorType


OMITTED = object()


class Attributes(object):
    """ Extractor functions for attributes of the same entity.
    """

    def __init__(self, **kw):
        self.extractors = {}
        for k, v in kw.items():
            self.add(k, v)

    def __len__(self):
        return len(self.extractors)

    def __call__(self, *args, **kwargs):
        # Add exception as 3rd field...

        for name, extractor in sorted(self.extractors.items()):

            try:
                value_or_generator = extractor(*args)
            except Exception as exc:
                yield name, exc
                continue

            # Wrapper generator, is there a more generic check?
            if not isinstance(value_or_generator, GeneratorType):
                yield name, value_or_generator
            else:
                try:
                    for value in value_or_generator:
                        yield name, value
                # Catch programming errors: NameError...
                except Exception as exc:
                    yield name, exc

    def add(self, extractor_or_name, extractor=OMITTED):
        '''
        An attribute function decorator/add method.
        '''
        if extractor is OMITTED:
            # Look at me, I'm a decorator
            name = extractor_or_name.__name__
            extractor = extractor_or_name
        else:
            # Hi, I'm an add() method
            name = extractor_or_name

        self.extractors[name] = extractor

        # Return the extractor so we can act as a decorator
        return extractor_or_name
