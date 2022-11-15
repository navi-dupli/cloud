from google.cloud import pubsub_v1


def publish_messages(project_id: str, topic_id: str, message: str):
    """Publishes multiple messages to a Pub/Sub topic."""
    # [START pubsub_quickstart_publisher]
    # [START pubsub_publish]
    publisher = pubsub_v1.PublisherClient()
    # The `topic_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/topics/{topic_id}`
    topic_path = publisher.topic_path(project_id, topic_id)

    data_str = f'{message}'
        # Data must be a bytestring
    data = data_str.encode("utf-8")
        # When you publish a message, the client returns a future.
    future = publisher.publish(topic_path, data)
    print(future.result())

    print(f"Published messages to topic {topic_path}.")
    # [END pubsub_quickstart_publisher]
    # [END pubsub_publish]
