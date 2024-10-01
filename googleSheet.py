import gspread

class GoogleSheet:
    def __init__(self, url) -> None:
        self.gc = gspread.service_account(filename='googleAPI.json')
        self.sheet = self.gc.open_by_url(url).sheet1

    def get_records(self):
        return self.sheet.get_all_records()
    
    def get_row(self, num):
        return self.sheet.row_values(num)
    
    def get_row_count(self):
        return self.sheet.row_count
