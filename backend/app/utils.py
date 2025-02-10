SANDBOX_API_URL = "https://dg.setu.co"
POSTMAN_LOCAL_SERVER_URL = 'https://25722b22-725b-47cc-9584-5f068802cce2.mock.pstmn.io'
BASE_URI = POSTMAN_LOCAL_SERVER_URL


def get_headers(product_id):
    headers = {
            "Content-Type": "application/json",
            "x-client-id":"b79b7d73-1c17-43f5-8c4c-8c185765c1c1",
            "x-client-secret":"jHlqATEpLKo4OXgF28gjFOdOT4Nk06Vo",
            "x-product-instance-id":product_id
        }
    return headers
