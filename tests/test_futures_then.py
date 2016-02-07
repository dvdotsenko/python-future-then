from unittest import TestCase

from futures_then import ThenableFuture, CircularFuturesChainException


class ThenMethodTests(TestCase):

    def test_no_callbacks_and_success(self):

        base_f = ThenableFuture()
        new_f = base_f.then()

        assert base_f is not new_f

        assert not base_f.done()
        assert not new_f.done()

        base_f.set_result('done')

        assert base_f.done()
        assert new_f.done()

        assert not new_f.exception()
        assert new_f.result() == 'done'

    def test_no_callbacks_and_failure(self):

        base_f = ThenableFuture()
        new_f = base_f.then()

        assert base_f is not new_f

        assert not base_f.done()
        assert not new_f.done()

        class _MyException(Exception):
            pass

        base_f.set_exception(_MyException('sad'))

        assert base_f.done()
        assert new_f.done()

        assert new_f.exception()
        with self.assertRaises(_MyException) as catcher:
            new_f.result()
        assert catcher.exception.message == 'sad'

    def test_success_callback_and_success(self):

        base_f = ThenableFuture()
        new_f = base_f.then(
            lambda result: result + ' manipulated'
        )

        assert base_f is not new_f

        assert not base_f.done()
        assert not new_f.done()

        base_f.set_result('done')

        assert base_f.done()
        assert new_f.done()

        assert not new_f.exception()
        assert new_f.result() == 'done manipulated'

    def test_err_callback_and_failure_repackage(self):

        class _MyException(Exception):
            pass

        class _MyRepackagedException(Exception):
            pass

        class _NotMatched(Exception):
            pass

        base_f = ThenableFuture()
        new_f = base_f.then(
            None,
            lambda ex: _MyRepackagedException(ex.message + ' repackaged') if isinstance(ex, _MyException) else _NotMatched('WTF?')
        )

        assert base_f is not new_f

        assert not base_f.done()
        assert not new_f.done()

        base_f.set_exception(_MyException('sad'))

        assert base_f.done()
        assert new_f.done()

        assert new_f.exception()
        with self.assertRaises(_MyRepackagedException) as catcher:
            new_f.result()
        assert catcher.exception.message == 'sad repackaged'

    def test_err_callback_and_failure_raised(self):

        class _MyException(Exception):
            pass

        class _MyRepackagedException(Exception):
            pass

        def raise_something_else(ex):
            raise _MyRepackagedException(
                ex.message + ' repackaged'
            )

        base_f = ThenableFuture()
        new_f = base_f.then(
            None,
            raise_something_else
        )

        assert base_f is not new_f

        assert not base_f.done()
        assert not new_f.done()

        base_f.set_exception(_MyException('sad'))

        assert base_f.done()
        assert new_f.done()

        assert new_f.exception()
        with self.assertRaises(_MyRepackagedException) as catcher:
            new_f.result()
        assert catcher.exception.message == 'sad repackaged'

    def test_err_callback_convert_to_success(self):

        class _MyException(Exception):
            pass

        class _NotMatched(Exception):
            pass

        base_f = ThenableFuture()
        new_f = base_f.then(
            None,
            lambda ex: ex.message + ' repackaged' if isinstance(ex, _MyException) else _NotMatched('WTF?')
        )

        assert base_f is not new_f

        assert not base_f.done()
        assert not new_f.done()

        base_f.set_exception(_MyException('sad'))

        assert base_f.done()
        assert new_f.done()

        assert not new_f.exception()
        assert new_f.result() == 'sad repackaged'

    def test_success_callback_and_failure_raised(self):

        class _MyException(Exception):
            pass

        def raise_something_else(value):
            raise _MyException(
                value + ' repackaged'
            )

        base_f = ThenableFuture()
        new_f = base_f.then(
            raise_something_else
        )

        assert base_f is not new_f

        assert not base_f.done()
        assert not new_f.done()

        base_f.set_result('sad')

        assert base_f.done()
        assert new_f.done()

        assert new_f.exception()
        with self.assertRaises(_MyException) as catcher:
            new_f.result()
        assert catcher.exception.message == 'sad repackaged'

    def test_chained_success_callback_and_success(self):

        base_f = ThenableFuture()

        def _transform(value):
            """
            :param int value:
            :rtype: int
            """
            f = ThenableFuture()
            if value < 5:
                f.set_result(_transform(value+1))
            else:
                f.set_result(value)
            return f

        new_f = base_f.then(_transform)

        assert base_f is not new_f

        assert not base_f.done()
        assert not new_f.done()

        base_f.set_result(1)

        assert base_f.done()
        assert new_f.done()

        assert not new_f.exception()
        assert new_f.result() == 5

    def test_detect_circular_chains(self):

        base_f = ThenableFuture()

        f1 = ThenableFuture()
        f2 = ThenableFuture()

        chain = [f1, f2, f1]

        def _transform(a):
            """
            :param int value:
            :rtype: int
            """
            try:
                f = chain.pop(0)
                f.set_result(_transform(a))
                return f
            except IndexError:
                return 5

        new_f = base_f.then(_transform)

        assert base_f is not new_f

        assert not base_f.done()
        assert not new_f.done()

        base_f.set_result(1)

        assert base_f.done()
        assert new_f.done()

        assert new_f.exception()
        with self.assertRaises(CircularFuturesChainException) as catcher:
            new_f.result()

        assert 'Circular Futures chain detected' in catcher.exception.message
