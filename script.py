# Imports
import simpy
import random
import statistics

# List to store the wait times of customers.
wait_times = []

# Create a bank object to hold the resources.
class Bank(object):
    # Constructor to create the resources and environment
    def __init__(self, env, num_tellers, num_atms):
        self.env = env
        self.teller = simpy.Resource(env, num_tellers)
        self.atm = simpy.Resource(env, num_atms)
    # Set the service time for the teller with a uniform distribution
    def go_teller(self, customer):
        yield self.env.timeout(random.randint(2, 8))
    # Set the service time of the ATM with a uniform distribution.
    def use_atm(self, customer):
        yield self.env.timeout(random.randint(1, 4))

# Start the bank simulation
def go_to_bank(env, customer, bank):
    # Set the arrival time for the bank.
    arrival_time = env.now

    choice = random.randint(1, 2)

    if choice == 1:
        with bank.teller.request() as request:
            yield request
            yield env.process(bank.go_teller(customer))
    else:
        with bank.atm.request() as request:
            yield request
            yield env.process(bank.use_atm(customer))


    # Moviegoer heads into the theater
    wait_times.append(env.now - arrival_time)


def run_theater(env, num_tellers, num_atms):
    bank = Bank(env, num_tellers, num_atms)

    for customer in range(3):
        env.process(go_to_bank(env, customer, bank))

    while True:
        yield env.timeout(4)  #interarrival time of 4 mins.

        customer += 1
        env.process(go_to_bank(env, customer, bank))


def get_average_wait_time(wait_times):
    average_wait = statistics.mean(wait_times)
    # Pretty print the results
    minutes, frac_minutes = divmod(average_wait, 1)
    seconds = frac_minutes * 60
    return round(minutes), round(seconds)


def get_user_input():
    num_tellers = input("Input # of tellers working: ")
    num_atms = input("Input # of atms available: ")
    params = [num_tellers, num_atms]
    if all(str(i).isdigit() for i in params):  # Check input is valid
        params = [int(x) for x in params]
    else:
        print(
            "Could not parse input. Simulation will use default values:",
            "\n1 teller, 2 atms.",
        )
        params = [1, 2]
    return params


def main():
    # Setup
    random.seed(20)
    num_tellers, num_atms = get_user_input()

    # Run the simulation
    env = simpy.Environment()
    env.process(run_theater(env, num_tellers, num_atms))
    env.run(until=360) 

    # View the results
    mins, secs = get_average_wait_time(wait_times)
    print(
        "Running simulation...",
        f"\nThe average wait time is {mins} minutes and {secs} seconds.",
    )


if __name__ == "__main__":
    main()