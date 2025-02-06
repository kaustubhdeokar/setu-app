APIs:
- register
  - ```curl -X POST "http://127.0.0.1:8000/register" \
     -H "Content-Type: application/json" \
     -d '{
           "username": "user4",
           "password": "user4",
           "pan_number": "ABABA1212C"
         }'
- login
  - curl -X POST "http://127.0.0.1:8000/login" \
     -H "Content-Type: application/json" \
     -u user4:user4

- pan card validation
  - curl -X POST "http://127.0.0.1:8000/api/verify/pan" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyNCIsImV4cCI6MTczODg2NDEwNX0.frmwNKXd-2lXajPiAZOrMUskKTVwgVr8QoOq9e35kF8" \
    -H "x-client-id: b79b7d73-1c17-43f5-8c4c-8c185765c1c1" \
    -H "x-client-secret: jHlqATEpLKo4OXgF28gjFOdOT4Nk06Vo" \
    -H "x-product-instance-id: 289ca52c-361a-48d7-9090-de8ab8bd3c52" \
    -d '{
          "pan": "ABCDE1234A",
          "consent": "Y",
          "reason": "Reason for verifying PAN set by the developer"
        }'