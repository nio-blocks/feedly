FeedlyStreams
=============

Gets posts from the specified list of feedly `streams`.

Properties
----------
- **auth_token**: developer token from feedly account
- **include_query**: whether to include queries on requests to feedly
- **lookback**: how far to lookback for posts
- **polling_interval**: interval to poll
- **queries**: feedly streams to query
- **retry_interval**: interval to retry
- **retry_limit**: number of times max to retry on a request
- **user_id**: feedly user id

Inputs
------
- **default**: Any list of signals.

Outputs
-------
- **default**: The returned posts from each specified feedly `stream`. For example:

```
{
  continuation: string,
  id: string,
  items: [
    {
      actionTimestamp: datetime,
      alternate: [
        {
          href: string
        }
      ],
      author: string,
      canonical: [
        {
          href: string
        }
      ],
      categories: [
        {
          id: string,
          label: string
        }
      ],
      crawled: datetime,
      id: string,
      origin: {
        htmlUrl: string,
        streamId: string,
        title: string
      },
      originId: string,
      published: datetime,
      summary: {
        content: string,
        direction: string
      },
      title: string,
      tags: [
        {
          id: string,
          label: string
        }
      ],
      unread: boolean
    }
  ]
}
```

Commands
--------
None

Dependencies
------------
None
