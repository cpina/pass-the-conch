#!/usr/bin/env python3

import datetime
import os
import random
import time

import config


def say(text):
    print(text)
    os.system(f'echo {text} | festival --tts')


def write_to_file(person, elapsed):
    f = open('log.txt', 'a')

    now = datetime.datetime.now()

    f.write(f'{now:%d-%m-%Y %H:%M:%S}, {person}, {elapsed:.0f}\n')
    f.close()


def remove_people_off_today(people):
    today = datetime.datetime.today().strftime('%a')

    for person in people:
        if person in config.days_off and today in config.days_off[person]:
            people.remove(person)
            print(f'{person} is off today')


def main():
    starts_process = time.time()

    people = config.people[:]

    remove_people_off_today(people)

    say('Good morning!')
    count_people = 0
    total_people = len(people)

    random.shuffle(people)

    while len(people) > 0:
        chosen = random.choice(people)

        if count_people == 0:
            say(f'The first today is: {chosen}')
        elif len(people) == 1:
            say(f'And finally the last person today is: {chosen}')
        else:
            say(f'Next is: {chosen}')

        starts_person = time.time()
        people.remove(chosen)
        print(f'This is {count_people + 1} of {total_people}')
        print()
        input('Press enter when finished\n')
        elapsed = time.time() - starts_person

        write_to_file(chosen, elapsed)
        count_people += 1

    say(f'Have a nice day!')

    elapsed_process = time.time() - starts_process
    print()
    print(f'Total time: {elapsed_process / 60:.1f} minutes')


if __name__ == '__main__':
    main()
