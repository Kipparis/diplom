curl -s -i -X PUT -H  "Content-Type:application/json" \
    http://localhost:8083/connectors/sink-elastic-01/config \
    -d '{
            "connector.class": "io.confluent.connect.elasticsearch.ElasticsearchSinkConnector",
            "connection.url": "http://elasticsearch:9200",
            "type.name": "testtypename",
            "topics": "algorithms-events",
            "key.ignore": "true",
            "schema.ignore": "true"
            }'
