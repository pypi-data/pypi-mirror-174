# DJ StreamIO

Framework for making it easy to post stream updates to (stream.io)[https://getstream.io]

## Installation

[![PyPI version](https://badge.fury.io/py/dj-streamio.svg)](https://badge.fury.io/py/dj-streamio)

```
pip install dj-streamio
```

## Configuration

### 1. Add `streamio` to `INSTALLED_APPS`

### 2. Configure your models for tracking:

e.g.:

```python
from streamio.mixins import StreamModelMixin

class Todo(models.Model, StreamModelMixin):

    collection = 'todos'
    feed_name = 'todo'
    feed_actor_field = 'owner_id'
    feed_once_off_actions = ["create"]
    feed_related_mapping = [
        # feed_slug, model_field
        ('user', 'owner_id'),
        ('todo', 'id'),
    ]
    # a list of object_id prefixes to look for in the `object_ids` field
    # e.g.: todo.object_ids = ["foo:1", "bar:2"]
    feed_object_ids_mapping = ["foo", "bar"]
    enrichment_serializer = 'example_app.models.TodoSerializer'

```

**Notes:**

1. We add `StreamModelMixin` to our model
2. Add the various meta fields
3. Profit

#### Track actions:

```python
todo = Todo.objects.first()
todo.track_action('create')
todo.track_action('start')
todo.track_action('complete')
```

#### Add reaction:

You can add a reaction (e.g.: like, comment, upvote etc) to an activity

**Example**

```python
todo.add_reaction(
    activity_kind, # e.g.: like, comment, status
    activity_id,
    data,
    by=user_id,
    target_feeds=["notification:thierry"]
)
```

**notes:**

* `data` is the reaction data. e.g.: `{"text": "@thierry great post!"}`
* `by` (optional) will default to the models `actor_id` if none is provided.
*  `target_feeds` (optional) will default to the models `feed_related_mapping`.

**Stream docs on Reactions:** https://getstream.io/docs/python/#reactions_introduction

#### Add notifications:

```python
todo = Todo.objects.first()

# note: you'll need to setup a webhook to actually handle forwarding!
# https://getstream.io/docs/#realtime-webhooks

# a combination of ways to propagate this notification (all are optional)
forward = {
    "sms": ['+27...', '+27...'],
    "inapp": ['user:1', 'user:2'], # inapp notification channels
    "email: ['jane@soap.com', 'joe@soap.com']
}

todo.add_notification(
    verb="..",
    notify=[user1.id, user2.id],
    message='hello!',
    forward = forward
)
```

### Get Feed

```python
todo = Todo.objects.first()
# get feed with all the defaults
todo.get_feed()

# you can set any extra args with kwargs:
# available parameters: https://getstream.io/docs/python/#retrieve
todo.get_feed({"limit": 5, "offset": 5, "enrich": False})
```

### Feed mixin

> `dj-streamio` provides a mixin that can be used to expose a `/stream/` endpoint on a DjangoRestFramework `ModelViewSet`. This endpoint proxiess the group feed for the underlying model. It also provides an analytics endpoint which gives a breakdown of the last 100 activities at `/streamactivity/`

**Example:**

```python
from streamio.viewsets import StreamViewSetMixin

# for older versions of DRF (prior to the @action update) use this mixin
# from streamio.viewsets_legacy import StreamViewSetMixin

...

# then simply mix it into your ViewSet:

class TodoViewSet(StreamViewSetMixin, viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

# /todos/:pk/stream/
# /todos/:pk/streamactivity/
```

## Low level usage

```python
from streamio.streamio import get_client
stream = get_client() # returns a standard logged-in stream.io client
...
```
**Note:**

* See also: `StreamObject` and `StreamUser`

### TODOS:

* Provide alternative backends (later)



