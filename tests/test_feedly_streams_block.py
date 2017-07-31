from nio.testing.block_test_case import NIOBlockTestCase
from ..feedly_streams_block import FeedlyStreams


class TestFeedlyStreams(NIOBlockTestCase):

    def test_process_signals(self):
        blk = FeedlyStreams()
        self.configure_block(blk, {
            "queries": [],
        })
        blk.start()
        blk.stop()
