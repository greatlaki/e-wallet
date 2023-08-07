from kafka import KafkaProducer


class ProducerServer(KafkaProducer):
    def publish_message(self, topic_name, key, value):
        try:
            key_bytes = bytes(key, encoding="utf-8") if key else None
            value_bytes = bytes(value, encoding="utf-8")
            self.send(topic_name, key=key_bytes, value=value_bytes)
            self.flush()
            return "Message published successfully."
        except Exception as excp:
            return f"Exception in publishing message: {excp}"
