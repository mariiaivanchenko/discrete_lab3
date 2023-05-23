"""Day simulation using FSM"""

import random

class Student:
    """describes student."""

    def __init__(self, name: str, age: int, hours: int, deadlines: int) -> None:
        self.name = name
        self.age = age
        self.energy = self.calculate_energy(hours)
        self.stress = 10 * deadlines
        self.deadlines = deadlines
        self.hunger = None
        self.mood = None

    def calculate_energy(self, hours: int) -> int:
        """calculate amount of student energy according to sleeping hours."""
        if hours >= 8:
            return 100
        else:
            return round(hours * (100 / 8))

    def __str__(self) -> str:
        return f"{self.name} is {self.age}-years-old student at UCU.\n\
According to number of sleep hours student has {self.energy}% of energy today. \n\
Stress level according to deadlines number, which is {self.deadlines}, is {self.stress}."


class State:
    """respresents students state"""
    def __init__(self, name, finite=False) -> None:
        self.name = name
        self.finite = finite


class DaySimulation:
    """implements FSM according to one day of students life."""
    sleep_m = State("Good morning")
    sleep_n = State("Good night", True)
    eat  = State("Eat")
    workout = State("Work Out")
    walk = State("Walk with friends")
    study = State("Study")
    family = State("Family time")
    rest = State("Relax")
    anime = State("Watch anime")
    lessons = State("Lessons")
    time = 0 # end when time is 24
    def __init__(self, student:Student) -> None:
        self.state = self.sleep_m #default
        self.student = student
        self.time = 7 if self.student.energy >= 80 else 8

    def start_simulation(self):
        """i believe this should be smt like controller
        that connects all the parts together or only starts simulation,
        dont know"""
        # set moood
        if self.student.energy >= 70 and self.student.stress <= 10:
            self.student.mood = "great"
        elif self.student.energy >= 50 or 10 < self.student.stress <= 30:
            self.student.mood = "okay"
        elif self.student.energy == 0:
            print(f'{self.student.name} does not have ehough energy to start the day.')
            exit()
        else:
            self.student.mood = "bad"

        self.student.hunger = 50
        print("Good morning, day is started.")
        self.choice()

    def choice(self):
        """create choices"""
        if self.time < 24 and self.student.energy > 0:
            if self.state == self.sleep_m:
                if random.randint(0, 100) <= 50:
                    print(f"{self.student.name} is working out now.")
                    self.change_to_workout()
                else:
                    print(f"{self.student.name} just waked up and heading to eat deliciuos breakfast.")
                    self.change_to_eat()

            elif self.state == self.eat:
                num = random.randint(0, 32)
                if num <= 10:
                    print("Lessons and studies is not today`s goal, we are meeting friends.")
                    self.change_to_walk()
                elif 10 < num <= 12:
                    print("Something really unexpected happened, anime time <3")
                    self.change_to_anime()
                elif 12 < num <= 15:
                    print("Now it is time to enjoy the company of the family.")
                    self.change_to_family()
                elif 15 < num <= 31:
                    print(f"Today {self.student.name} need to submit some deadlines to sleep at night.")
                    self.change_to_study()
                else:
                    print(f"Today {self.student.name} has some lessons to attend.")
                    self.change_to_lessons()

            elif self.state == self.lessons:
                print(f"{self.student.name} need to restore resources, food resources.")
                self.change_to_eat()

            elif self.state == self.walk:
                print("Walking with friends is nice, but food is better.")
                self.change_to_eat()

            elif self.state == self.workout:
                print("After work out body needs resources, heading to kitchen.")
                self.change_to_eat()

            elif self.state == self.anime:
                if self.time >= 21:
                    print(f"{self.student.name} is tired of watching and going to sleep.")
                    self.change_to_night()
                else:
                    self.change_to_anime()

            elif self.state == self.family:
                if self.time >= 21:
                    print(f"{self.student.name} satysfied social needs with family and would like to sleep.")
                    self.change_to_night()
                else:
                    self.change_to_family()

            elif self.state == self.study:
                if random.randint(0, 100) <= 15:
                    print(f"To continue {self.student.name} need to rest a liitle.")
                    self.change_to_rest()
                elif self.time < 21:
                    self.change_to_study()
                else:
                    print(f"{self.student.name} is exhausted with studing and ready to sleep.")
                    self.change_to_night()

            elif self.state == self.rest:
                if self.time >= 21:
                    print(f"There is no reason to stay awake, so {self.student.name} is going to bed.")
                    self.change_to_night()
                else:
                    print("There is still some studies to complete.")
                    self.change_to_study()
        else:
            self.current()
            print(f'{self.student.name} is ran out of resources, so day is over)')

    def change_to_eat(self):
        """changes state to eating"""
        self.state = self.eat
        self.student.mood = "great"
        self.student.hunger = 0
        self.time += 1
        self.current()
        self.choice()

    def change_to_workout(self):
        """change state to work out"""
        self.state = self.workout
        self.student.mood = "great"
        self.student.hunger = 100
        self.student.energy -= 10
        self.time += 1
        self.current()
        self.choice()

    def change_to_walk(self):
        """change state to walk"""
        self.state = self.walk
        self.student.mood = "great"
        self.student.hunger = 50
        self.student.energy -= 20
        self.time += 2
        self.current()
        self.choice()

    def change_to_lessons(self):
        """change state to lessons"""
        self.state = self.lessons
        self.student.mood = "good"
        self.student.hunger = 100
        self.student.energy -= 20
        self.time += 4
        self.current()
        self.choice()

    def change_to_study(self):
        """change state to study"""
        self.state = self.study
        self.student.mood = "bad"
        self.student.hunger = 100
        self.student.energy -= 20
        self.time += 4
        self.current()
        self.choice()

    def change_to_family(self):
        """change state to family"""
        self.state = self.family
        self.student.mood = "good"
        self.student.hunger = 10
        self.student.energy -= 10
        self.time += 2
        self.current()
        self.choice()

    def change_to_rest(self):
        """change state to rest"""
        self.state = self.rest
        self.student.mood = "good"
        self.student.hunger = 0
        self.student.stress = 0
        self.time += 1
        self.current()
        self.choice()

    def change_to_anime(self):
        """change state to watch anime"""
        self.state = self.anime
        self.student.mood = "great"
        self.student.hunger = 0
        self.student.energy += 10
        self.time += 2
        self.current()
        self.choice()

    def change_to_night(self):
        """change state to sleep at night"""
        self.state = self.sleep_n
        self.student.mood = "good"
        self.student.hunger = 0
        self.student.energy = 0
        self.time = 24
        self.current()
        self.choice()

    def current(self) -> str:
        """that shows current situation, mood, state, energy etc"""
        print(f"Current situation is: \nTime: {self.time} \n\
State: {self.state.name} \nMood: {self.student.mood} \n\
Energy: {self.student.energy} \nHunger: {self.student.hunger} \nStress: {self.student.stress}\n")



# mariia = Student("Mariia", 18, 7, 1)
# day_sim = DaySimulation(mariia)
# day_sim.start_simulation()
