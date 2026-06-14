import requests

class Money:
    money_list = [0, 0, 0]


    def __init__(self):
        pass


    def date_input(self, date):
        url = f'https://www.nbrb.by/api/exrates/rates?ondate={date}&periodicity=0'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            for currency in data:
                if currency['Cur_Name'] == "Российских рублей":
                    self.money_list[0] = currency['Cur_Scale']
                    self.money_list[1] = currency['Cur_OfficialRate']
                elif currency['Cur_Name'] == "Евро":
                    self.money_list[2] = currency['Cur_OfficialRate']
            print(self.money_list)
        else:
            pass


    def money_input(self, input):
        try:
            value = float(input) / self.money_list[0] * self.money_list[1] / self.money_list[2]

            value = round(value, 2)

            if str(value).endswith(".00") or str(value).endswith(".0"):
                value = int(value)

            return value
        except:
            return ""


if __name__ == "__main__":
    while True:
        try:
            Money().date_input(input("date: "))
            print(Money().money_input(input("money RUB: ")))
        except:
            print("Error!")
            