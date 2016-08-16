# Feedly
Gets posts from the specified list of feedly `streams`. 

## Properties
* **Authorization Token**: developer token from feedly account
* **Streams**: feedly streams to query
* **Lookback Period**: how far to lookback 
* **Retry Interval**: how long to wait before attempting to try again when a url request fails
* **Retry Limit**: number of times to attempt a retry before giving up when a url request fails

## Dependencies
* [RESTPolling Block](https://github.com/nio-blocks/http_blocks/blob/master/rest/rest_block.py)

## Commands
None

## Input 
None

## Output
The returned posts from each specified feedly `stream`. For example:

```
{
  "continuation": ":continuation_key",
  "id": ":category_id",
  "items": [
    {
      "actionTimestamp": ":action_timestamp",
      "alternate": [
        {
          "href": ":alternate_uri",
          "type": ":mimetype"
        }
      ],
      "author": ":author",
      "canonical": [
        {
          "href": ":canonical_uri",
          "type": ":mimetype"
        }
      ],
      "categories": [
        {
          "id": ":item_category_id",
          "label": ":item_category_name"
        }
      ],
      "crawled": ":crawled_timestamp",
      "fingerprint": ":fingerprint",
      "id": ":item_id",
      "keywords": [
        ":keyword"
      ],
      "origin": {
        "htmlUrl": ":site_uri",
        "streamId": ":feed_id",
        "title": ":feed_title"
      },
      "originId": ":item_uri",
      "published": "item_pub_timestamp",
      "summary": {
        "content": ":item_desc",
        "direction": ":text_direction"
      },
      "title": ":item_title",
      "tags": [
        {
          "id": ":tag_id",
          "label": ":tag_name"
        },
        ...
      ],
      "unread": true
    }
  ],
  ...
}
```
