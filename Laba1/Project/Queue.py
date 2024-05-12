import random
import time
class Queue:
    def __init__(self):
        self.count_visitors_attract = random.randint(0, 60)
        self.count_visitors_ticket = random.randint(0, 20)

    def join_queue_attraction(self, attraction_capacity):
        while self.count_visitors_attract >= 0:
            print(f"Number of visitors in queue: {self.count_visitors_attract}")
            if self.count_visitors_attract >= attraction_capacity:
                print("The attraction is full. Waiting in the queue...")
                time.sleep(5)
                self.count_visitors_attract -= attraction_capacity
            else:
                self.count_visitors_attract = 0
                break

    def join_queue_ticket(self):
        while self.count_visitors_ticket > 0:
            print(f"Number of visitors in ticket queue: {self.count_visitors_ticket}")
            print("Waiting in the queue...")
            time.sleep(1)
            self.count_visitors_ticket -= 1
        print("it's your turn to buy a ticket.")



