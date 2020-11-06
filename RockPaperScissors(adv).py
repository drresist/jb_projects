import random

random.seed(42)

# Set username

username = input("Enter your name: ")
print("Hello, %s" % username)
std_rules = ['scissors', 'rock', 'paper']

# All possible variants
all_cases = ['rock', 'fire', 'scissors', 'snake', 'human', 'tree', 'wolf', 'sponge', 'paper', 'air', 'water', 'dragon',
             'devil', 'lightning', 'gun']

condition = {}
cases_length = len(all_cases)
tmp = all_cases.copy()
# Generator of winning condition
for i in range(cases_length):
    condition[all_cases[i]] = tmp[i + 1:int(cases_length / 2) + i]
    tmp.append(all_cases[i])


# Check user rating
def check_rating(name):
    file = open('rating.txt')
    local_score = 0
    for line in file:
        if line.split()[0] == name:
            local_score = int(line.split()[1])
    file.close()
    return local_score


possible_vars = input().split(',')
print("Okay, let's start")
if len(possible_vars) < 2:
    possible_vars = std_rules.copy()
score = check_rating(username)
end = False
# print(possible_vars)
while not end:
    user_inp = input()
    # exm: rock
    ai_inp = random.choice(possible_vars)
    # exm: gun
    if user_inp in list(condition.keys()) and ai_inp in condition[user_inp] and user_inp in possible_vars:
        if ai_inp in possible_vars:
            print("Well done. The computer chose %s and failed" % ai_inp)
            score += 100
        elif user_inp == "!rating":
            print("Your rating %i" % score)
        elif user_inp == ai_inp:
            print("There is a draw (%s)" % ai_inp)
            score += 50
        elif user_inp == "!exit":
            print("Bye!")
            end = True
        elif user_inp in possible_vars and ai_inp in possible_vars:
            print("Sorry, but the computer chose %s" % ai_inp)
        else:
            print("Invalid input")
    elif user_inp == "!rating":
        print("Your rating %i" % score)
    elif user_inp == ai_inp:
        print("There is a draw (%s)" % ai_inp)
        score += 50
    elif user_inp == "!exit":
        print("Bye!")
        end = True
    elif user_inp in possible_vars and ai_inp in possible_vars:
        print("Sorry, but the computer chose %s" % ai_inp)
    else:
        print("Invalid input")
