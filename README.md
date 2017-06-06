Feedly
===================
Gets posts from the specified list of feedly `streams`. 

Properties
------------------
**authorization_token**: developer token from feedly account
**streams**: feedly streams to query
**lookback**: how far to lookback for posts 
**retry_interval**: how long to wait before attempting to try again when a url request fails
**retry_limit**: number of times to attempt a retry before giving up when a url request fails

Dependencies
------------------
* [RESTPolling Block](https://github.com/nio-blocks/http_blocks/blob/master/rest/rest_block.py)

Commands
------------------
None

Input 
------------------
None

Output
------------------
The returned posts from each specified feedly `stream`. For example:

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
