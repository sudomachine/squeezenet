from algorithm import rearrange
import random

numbers = list(range(10, 20))
print(f"numbers then: {numbers}")

new_order = [1, 6, 2, 0, 5, 4, 3, 7, 9, 8]
#new_order = list(range(len(numbers)))
#random.shuffle(new_order)
print(f"New order: {new_order}")


numbers = rearrange(numbers, new_order)
print(f"numbers now: {numbers}")
