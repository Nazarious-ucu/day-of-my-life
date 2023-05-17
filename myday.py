"""
last lab of discret math
"""
import random
from time import sleep
def prime(fn):
    def wrapper(*args, **kwargs):
        v = fn(*args, **kwargs)
        v.send(None)
        return v
    return wrapper

class DaySimulator:
    """
    class for simulation of day by FSM
    """

    def __init__(self) -> None:
        self.current_state = self._create_sleep()
        self.num_lessons = 1
        self.num_hour_deadlines = 0
        self.__state_dict = {
            "sleep": self._create_sleep(),
            "wake up": self._create_eating(),
            "chill": self._create_chill(),
            "paru": self._create_paru(),
            "pivko": self._create_pivko(),
            "do deadlines": self._create_do_deadlines(),
            "colegium": self._create_colegium()
        }
        self.hour = 0
        self.stopped = False
        self.day_of_week = random.choice(['Monday',
                                          'Tuesday',
                                          'Wednesday',
                                          'Thursday',
                                          'Friday'])
        self.day_over = False
        print(f'So, today is {self.day_of_week}')

    def send(self, char):
        try:
            self.current_state.send(char)
        except StopIteration:
            self.stopped = True

    @prime
    def _create_sleep(self):
        """
        create sleep state
        """
        while True:
            chance = yield
            if self.hour == 7 and chance <= 0.5:
                print('Okeey, hello new day!')
                sleep(1)
                self.current_state = self.__state_dict['wake up']

            elif self.hour == 8:
                print("NOOOOO, I overslept, i haven't time!!!")
                sleep(1)
                self.current_state = self.__state_dict['wake up']
            else:
                print('zzzzz.....')
                self.hour += 1

    @prime
    def _create_eating(self):
        """
        create eating state
        """
        while True:
            yield
            if self.day_of_week == 'Monday' or \
                self.day_of_week == 'Thursday':
                print('Today, I do not have breakfast today, becose I have first lesson')
                sleep(1)
                self.current_state = self.__state_dict['paru']
            else:
                print('Today,There is very tasty breakfast in trapezna')
                sleep(1)
                print('I have not first lesson, so lets go chill')
                sleep(1)
                sleep(1)
                self.current_state = self.__state_dict['chill']
                self.hour += 1

    @prime
    def _create_chill(self):
        """
        create chill state
        """
        while True:
            chance = yield
            if chance >= 0.35:
                print('I have next lesson, nooooooo(')
                sleep(1)
                print('I have to go to lesson')
                sleep(1)
                self.current_state = self.__state_dict['paru']
            else:
                print('I can more chill')
                sleep(1)
                self.hour += 2


    @prime
    def _create_paru(self):
        """
        create paru state
        """
        while True:
            chance = yield
            end_of_big_deadline = chance <= 0.13
            if chance >= 0.25 and self.num_lessons <= 4:
                print('I have one more lesson')
                sleep(1)
                print('More pain')
                sleep(1)
                self.num_lessons += 1
                self.current_state = self.__state_dict['paru']
            elif self.day_of_week == 'Friday' or end_of_big_deadline :
                print('Cool, my pain it is over for today!!!!!')
                sleep(1)
                print('Let`s go `pyty pivo with kentamu`')
                sleep(1)
                self.current_state = self.__state_dict['pivko']
            else:
                print('Cool, my pain it is over for today!!!!!')
                sleep(1)
                print('Let`s go do my deadlines')
                sleep(1)
                self.current_state = self.__state_dict['do deadlines']
            self.hour += 2



    @prime
    def _create_pivko(self):
        """
        create pivko state
        """
        while True:
            yield
            print('Pivko is very great, veryyy delicious')
            sleep(1)
            print('After drinkng pivo, i have to make my deadlines')
            sleep(1)
            self.current_state = self.__state_dict['do deadlines']
            self.hour += 1

    @prime
    def _create_do_deadlines(self):
        """
        create do deadlines state
        """
        while True:
            chance = yield
            print('I am doing my deadlines')
            sleep(1)
            if self.hour <= 21 and chance <= 0.8:
                print('I have a lot of deadlines')
                sleep(1)
                print('brrrr.....')
                sleep(1)
                self.num_hour_deadlines += 1
                self.current_state = self.__state_dict['do deadlines']
            else:
                print('I do all my deadlines for todey')
                sleep(1)
                print('Let`s go to colegium and do somethings')
                self.current_state = self.__state_dict['colegium']
            self.hour += 1

    @prime
    def _create_colegium(self):
        """
        create colegium state
        """
        while True:
            chance = yield
            if chance <= 0.8 and self.hour < 24:
                print('I am doing something in colegium')
                self.current_state = self.__state_dict['colegium']
                self.hour += 1
            else:
                self.day_over = True
                print('It is end of my day, Bye')
                break


if __name__ == "__main__":
    day = DaySimulator()
    while not day.day_over:
        chance = random.random()
        day.send(chance)
        print(f'it is {day.hour} o`clock')
        sleep(1)
