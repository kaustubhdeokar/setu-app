API calls:

pan card call:
- ```curl -X POST "http://localhost:8000/api/verify/pan" -H "Content-Type: application/json" -d '{"pan": "ABCDE1234A", "consent": "Y", reason": "Reason for verifying PAN set by the developer"}'```
rpd call
- ```curl -X POST "http://localhost:8000/api/verify/ban/reverse" -H "Content-Type: application/json"```
simulate web hook
- ```curl -X POST "http://localhost:8000/api/verify/ban/reverse/webhook" -H "Content-Type: application/json"```
get details call
- ```curl -X GET "http://localhost:8000/api/verify/ban/reverse/1234"```

