"""
Utilities for with-statement contexts
"""
# pylint: disable=invalid-name
#
import contextlib


class suppress(contextlib.suppress, contextlib.ContextDecorator):
    """
    A version of contextlib.suppress with decorator support.

    Example
    -------

    .. code-block::

        @contextlib.suppress(ValueError)
        def foobar():
            ...
    """


class reraise_from_none(contextlib.suppress, contextlib.ContextDecorator):
    """
    Similar to contextlib.suppress, but with decorator support, and that
    re-raises exception from None instead of hiding it.

    Example
    -------

    .. code-block::

        @contextlib.reraise_from_none(ValueError)
        def foobar():
            ...
    """

    def __exit__(self, exctype, excinst, _exctb):
        if exctype is None:
            return
        if issubclass(exctype, self._exceptions):
            raise excinst from None
