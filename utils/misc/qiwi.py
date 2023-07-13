# import pyqiwi
# from uuid import uuid4
# from dataclasses import dataclass
# import datetime


# from data.config import qiwi_key, qiwi_token, qiwi_number

# wallet = pyqiwi.Wallet(number=qiwi_number, token=qiwi_token)


# class NotEnoughMoney(Exception):
#     pass


# class NotPaymentFound(Exception):
#     pass


# @dataclass()
# class Payment:                      # класс куда попадают стоимость оплаты и персональный id
#     amount: int
#     id: str = None

#     def create(self):               # здесь генерируется id(рандомно)
#         self.id = str(uuid4())

#     def check_payment(self):  # здесь мы проверяем наличие оплаты по транзакциям за 2 дня
#         transactions = wallet.history(start_date=datetime.datetime.now() - datetime.timedelta(days=2)).get('transactions')
#         for transaction in transactions:  # итерируем занчаение
#             if transaction.comment:       # если транзакция найдена
#                 if str(self.id) in transaction.comment:  # правильный ли id
#                     if float(transaction.total.amount) >= self.amount: # если отправленная сумма денег больше или ровна
#                         return True                                    # тогда True
#                     else:                                              # в другом случае сообщить что средств недостаточно
#                         raise NotEnoughMoney
#         else:                                                          # ессли транзакция не найдена
#             raise NotPaymentFound

#     @property  # независммая функция но она в классе
#     def invoice(self):  # здесь формируется ссылка со всеми данными
#         link = "https://oplata.qiwi.com/create?publicKey={publickey}&amount={amount}&comment={comment}"
#         return link.format(publickey=qiwi_key, amount=self.amount, comment=self.id)  # она придёт как ссылка на оплату