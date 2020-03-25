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

    today = datetime.datetime.today()

    f.write(f'{today:%d-%m-%Y}, {person}, {elapsed:.0f}\n')
    f.close()


def main():
    starts_process = time.time()

    people = config.people[:]

    while len(people) > 0:
        chosen = random.choice(people)
        say(f'Next is: {chosen}')
        starts_person = time.time()
        people.remove(chosen)
        input('Press enter when finished\n')
        elapsed = time.time() - starts_person

        write_to_file(chosen, elapsed)

    elapsed_process = time.time() - starts_process
    print()
    print(f'Total time: {elapsed_process / 60:.1f} minutes')


if __name__ == '__main__':
    main()
