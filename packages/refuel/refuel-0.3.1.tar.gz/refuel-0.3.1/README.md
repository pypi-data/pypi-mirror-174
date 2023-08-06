# Refuel Python API

<p align="center"><img height="250" src="https://user-images.githubusercontent.com/1568137/172486199-f4eddb09-7c58-4841-8f3c-60f647079073.png"></p>

This is the [Refuel.ai](https://www.refuel.ai/) Python client library. The primary use for this library is to log your machine learning datasets to the Refuel platform. More features coming soon!

# Installation
You can install this library using `pip`:

```bash
pip install refuel
```

# Usage

Make sure you have a valid API key from Refuel (shared with your team during onboarding). Contact us at support@refuel.ai if you need help. 

## Initialization:

Initialize the Refuel client with your API key. This can be done in one of two ways:

```python
import refuel

# Assuming you've set `REFUEL_API_KEY` in your env,
# init() will pick it up automatically
refuel_client = refuel.init()
```

Alternatively, specify it as an explicit option:
```python
import refuel

options = {
    "api_key": "<YOUR_API_KEY>"
}

refuel_client = refuel.init(**options)
```

## Logging data

### Log a single prediction event (no ground truth)

```python
refuel_client.log(
    model_name='my-model-name',
    dataset_name='my-dataset-name',
    x={'id': 'id1', 'image_url': 's3://<bucket>/<path>', 'embedding': [0.42, -0.13, ...]},
    y_pred={'scores': {'cat': 0.92, 'dog': 0.08}, 'label': 'cat'},
    metadata={'camera_id': 'camera1'}
)
```

### Log a single prediction event (with ground truth)

```python
refuel_client.log(
    model_name='my-model-name',
    dataset_name='my-dataset-name',
    x={'id': 'id2', 'image_url': 's3://<bucket>/<path>', 'embedding': [0.35, -0.27, ...]},
    y_pred={'scores': {'cat': 0.12, 'dog': 0.88}, 'label': 'dog'},
    y_true={'label': 'cat'},
    metadata={'camera_id': 'camera1'}
)
```

### Log a single prediction event (ground truth becomes available at a later point)

```python
# This will be joined with the rest of the event logged previously
refuel_client.log(
    model_name='my-model-name',
    dataset_name='my-dataset-name',
    x={'id': 'id1'},
    y_true={'label': 'cat'},
    metadata={'camera_id': 'camera1'}
)
```

### Log a batch of prediction events

```python
# List of events to be logged. 
events = [{'x': ..., 'y_pred': ..., 'y_true': ..., 'metadata': ...}]

refuel_client.log_batch(
    model_name='my-model-name',
    dataset_name='my-dataset-name',
    events=events
)
```

### Log a dataset stored in S3 with the s3 path

```python
refuel_client.log_dataset(
    model_name='my-model-name',
    dataset_name='my-dataset-name',
    s3_uri='s3://bucket/path/to/object.type',
    dataset_config={'type': 'CSV', 'delimiter': '\t'}
)
```

### Log a dataset stored in S3 with a presigned url

```python
refuel_client.log_dataset(
    model_name='my-model-name',
    dataset_name='my-dataset-name',
    s3_uri='https://bucket.s3.amazonaws.com/path/to/object.type?AWSAccessKeyId=1234&Signature=1234',
    dataset_config={'type': 'CSV', 'delimiter': '\t'}
)
```

## Querying data

### Query events table

```python
# Query events directly from a dataset
refuel_client.query_events(
    model_name='my-model-name',
    dataset_name='my-dataset-name',
    time_start='2022-07-01',
    time_end='2022-08-02.',
    filters=[{"field": "column-name", "operator": "=", "value": "1"}],
    order_by="ordering-column",
    offset=1234,
    max_events=1234
)
```

### Query annotation queue

```python
# Query events from the annotation queue
refuel_client.query_annotation_queue(
    model_name='my-model-name',
    queue_name='my-queue-name',
    time_start='2022-07-01',
    time_end='2022-08-02.',
    filters=[{"field": "column-name", "operator": "=", "value": "1"}],
    order_by="ordering-column",
    offset=1234,
    max_events=1234
)
```

### Query similar events

```python
# Query events similar to passed event
refuel_client.query_similar_events(
    model_name='my-model-name',
    refuel_uuid='refuel-uuid',
    embedding_column='embedding-column',
    dataset_name='my-dataset-name',
    time_start='2022-07-01',
    time_end='2022-08-02.',
    filters=[{"field": "column-name", "operator": "=", "value": "1"}],
    max_events=1234
)
```

# Questions?

Reach out to us at support@refuel.ai with any questions!
