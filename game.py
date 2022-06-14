from random import randint

class Game:
    games = {

    }

    @classmethod
    def startGame(self, chat_id):
        number = self.generateRandomNumber()

        self.games[chat_id] = number

        return number

    @classmethod
    def ifWin(self, chat_id, choice):
        # number2 - второй бросок кости
        # number1 - первый бросок кости
        number2 = self.generateRandomNumber()

        number1 = self.games[chat_id]

        print("Первая кость", number1)
        print("Вторая кость", number2)
        print("Выбор", choice)

        # choice - то что, выбрал игрок.
        # если он выбрал выше и вторая кость больше первой, то он победил. иначе проиграл

        if choice == "Выше":
            if number2 >= number1:
                return {
                    "isWin": True,
                    "number2": number2
                }
            else:
                return {
                    "isWin": False,
                    "number2": number2
                }

        if choice == "Ниже":
            if number2 >= number1:
                return {
                    "isWin": False,
                    "number2": number2
                }
            else:
                return {
                    "isWin": True,
                    "number2": number2
                }

    @classmethod
    def generateRandomNumber(self):
        return randint(1,6)

