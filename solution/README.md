# kafka

+ `docker exec -it kafka /bin/bash`: логинимся в систему с kafka

+ `kafka-topics --create --topic algorithms-events --bootstrap-server localhost:9092`: создаем topic
+ `kafka-topics --describe --topic algorithms-events --bootstrap-server localhost:9092`: выводим инфу о топике

+ `kafka-console-consumer --topic algorithms-events --from-beginning --bootstrap-server localhost:9092`: показывает какие сообщения поступают
