# docker.api
This is just a simple demo how to develop a webservice using python, flask and mysql

```
How to run
調整 docker-compose.yml
將HOST_IP 調整為你的機器ip
docker-compose -f docker-compose.yml up -d
```
## Insert User
```
curl -H "Content-Type:application/json" -X POST -d '{"name":"Jessica","job_title":"RD","email":"jessica@gmail.com","mobile":"0988-323-312"}' 127.0.0.1:80/user
```

## Get all User
```
curl 127.0.0.1:80/user
```

## Delete User
```
curl -X DELETE 127.0.0.1:80/user/<id>
```

## Update User
```
curl -H "Content-Type:application/json" -X PUT -d '{"id": "1","email":"test@gmail.com"}' 127.0.0.1:80/user
curl -H "Content-Type:application/json" -X PUT -d '{"id": "1","job_title":"CTO"}' 127.0.0.1:80/user
```
