import time
import calendar
from enum import Enum
from urllib.request import quote

from nio.util.discovery import discoverable
from nio.signal.base import Signal
from nio.properties import (StringProperty, SelectProperty, TimeDeltaProperty,
                            ListProperty, PropertyHolder, VersionProperty)

from .rest_polling.rest_block import RESTPolling


class FeedlyStreamType(Enum):
    FEED = 0
    CATEGORY = 1
    TAG = 2


class FeedlyStream(PropertyHolder):
    stream_name = StringProperty(title='Stream', default='')
    stream_type = SelectProperty(
        FeedlyStreamType,
        default=FeedlyStreamType.FEED,
        title='Stream Type'
    )


@discoverable
class FeedlyStreams(RESTPolling):
    """ A block that gets entries from a feedly stream.

    Attributes:
        queries (List(str)): Feedly streams to query.
        lookback (timedelta): Initial amount of time to lookback
            for old feed entries.
        get_updates (bool): Notify a signal when a feed entry is updated.

    """
    URL_FORMAT = ("http://www.feedly.com/v3/streams/contents"
                  "?streamId={}&newerThan={}&continuation={}")

    auth_token = StringProperty(title='Authorization Token',
                                default='[[FEEDLY_AUTHORIZATION_TOKEN]]')
    user_id = StringProperty(title='User ID',
                             default='[[FEEDLY_USER_ID]]')
    queries = ListProperty(FeedlyStream, title='Streams')
    lookback = TimeDeltaProperty(title='Lookback Period',
                                 default={'seconds': 300})
    version = VersionProperty("1.0.0")

    def __init__(self):
        super().__init__()
        self._newer_than_timestamp = [None]
        self._next_newer_than_timestamp = [None]
        self._continuation = None

    def configure(self, context):
        super().configure(context)
        self._init_newer_than_timestamp()

    def _init_newer_than_timestamp(self):
        lookback_seconds = self.lookback().total_seconds()
        now_minus_lookback = calendar.timegm(time.gmtime()) - lookback_seconds
        self._newer_than_timestamp = [int(now_minus_lookback * 1000)]
        self._next_newer_than_timestamp = [int(now_minus_lookback * 1000)]
        self.logger.debug(
            'Initializing newerThan timestamp to {}'
            .format(int(now_minus_lookback * 1000))
        )
        self._newer_than_timestamp *= self._n_queries
        self._next_newer_than_timestamp *= self._n_queries

    def _needs_auth(self):
        # Authorization is only needed for category and feeds streams.
        if self.stream_type() == FeedlyStreamType.FEED:
            return False
        else:
            return True

    def _prepare_url(self, paging):
        if self._needs_auth():
            headers = {"Content-Type": "application/json",
                       "Authorization": "OAuth {}".format(self.auth_token())}
        else:
            headers = {"Content-Type": "application/json"}
        self.url = self.URL_FORMAT.format(self.stream_id,
                                          self.newer_than_timestamp,
                                          self._continuation)
        return headers

    def _process_response(self, resp):
        resp = resp.json()
        self._update_newer_than_timestamp(resp)
        entries = resp.get('items', [])
        self.logger.debug(
            'Feedly response contains {} items'.format(len(entries))
        )
        signals = [Signal(e) for e in entries]
        paging = self._check_if_paging(resp)
        return signals, paging

    def _update_newer_than_timestamp(self, resp):
        updated = resp.get('updated')
        if updated and updated >= self.newer_than_timestamp:
            self.next_newer_than_timestamp = updated + 1
            self.logger.debug(
                'Updating next newerThan timestamp to {} for {}'
                .format(self.next_newer_than_timestamp, self.current_query)
            )

    def _check_if_paging(self, resp):
        continuation = resp.get('continuation')
        if continuation:
            self._continuation = continuation
            return True
        else:
            # when paging is done, update newer than timestamp.
            self.newer_than_timestamp = self.next_newer_than_timestamp
            self._continuation = None
            return False

    @property
    def stream_id(self):
        if self.stream_type() == FeedlyStreamType.FEED:
            return quote('feed/{}'.format(self.stream_name()),
                         safe='')
        if self.stream_type() == FeedlyStreamType.TAG:
            return quote('user/{}/tag/{}'.format(self.user_id(),
                                                 self.stream_name()),
                         safe='')
        else:  # FeedlyStreamType.CATEGORY
            return quote('user/{}/category/{}'.format(self.user_id(),
                                                      self.stream_name()),
                         safe='')

    @property
    def stream_type(self):
        return self.queries[self._idx].stream_type

    @property
    def stream_name(self):
        return self.queries[self._idx].stream_name

    @property
    def current_query(self):
        return quote(self.stream_name)

    @property
    def next_newer_than_timestamp(self):
        return self._next_newer_than_timestamp[self._idx]

    @next_newer_than_timestamp.setter
    def next_newer_than_timestamp(self, timestamp):
        self._next_newer_than_timestamp[self._idx] = timestamp

    @property
    def newer_than_timestamp(self):
        return self._newer_than_timestamp[self._idx]

    @newer_than_timestamp.setter
    def newer_than_timestamp(self, timestamp):
        self._newer_than_timestamp[self._idx] = timestamp
