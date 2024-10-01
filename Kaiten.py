import requests
import asyncio

class Kaiten:

    def __init__(self, token, domain) -> None:
        self.token = token
        self.domain = domain
        self.url = f"https://{self.domain}.kaiten.ru/api/latest/" 
        self.headers = {
            'Accept':'application/json',
            'Content-Type':'application/json',
            'Authorization':f'Bearer {self.token}'
            }

    def get_cur_user(self):
        response = requests.get(url=self.url+"users/current", headers=self.headers)
        if response.status_code == 200:
            return {"id": response.json()["id"], 
                    "full_name": response.json()["full_name"], 
                    "email": response.json()["email"],
                    "username": response.json()["username"]}
        else : return f"response error {response.status_code}"

    def get_users(self):
        response = requests.get(url=self.url+"users", headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else : return f"response error {response.status_code}"

    def get_spaces(self):
        response = requests.get(url=self.url+"spaces", headers=self.headers)
        if response.status_code == 200:
            return list(map(lambda x:(x["id"], x["title"]), response.json()))
        else : return f"response error {response.status_code}"

    def get_boards(self, space_id):
        response = requests.get(url=self.url+f"spaces/{space_id}/boards", headers=self.headers)
        if response.status_code == 200:
            return list(map(lambda x:(x["id"], x["title"], list(map(lambda c: (c["id"], c["title"]), x["columns"]))), response.json()))
        else : return f"response error {response.status_code}"

    def create_card(self, board_id, column_id, title, description, due_date):
        data = {
            'title': title,
            'board_id': board_id,
            "asap": 0,
            'column_id': column_id,
            'due_date': due_date,
            'due_date_time_present': 0,
            'description':description
        }
        response = requests.post(url=self.url+"cards", headers=self.headers, json=data)
        return response.status_code
    
    async def get_all_boards(self):
        return list(map(lambda x:( x, self.get_boards(x[0])), self.get_spaces()))
    
    async def check_conntection(self):
        return True if requests.get(url=self.url+"users", headers=self.headers).status_code == 200 else False
