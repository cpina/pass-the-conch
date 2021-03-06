#!/usr/bin/env python3

# MIT License
# pass-the-conch
#
# Copyright © 2020 Carles Pina i Estany <carles@pina.cat>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import argparse
import datetime
import os
import random
import sys
import time

try:
    import config
except ModuleNotFoundError:
    print('config.py cannot be imported. You might need to rename config.example.py to config.py', sys.stderr)
    exit(1)

sentences_transliterated = {
    'Good morning!': {'russian': 'ГуД mopнинГ!'},
    'Have a nice day': {'russian': 'Have a nice day!'},
    'Next is: {name}': {'russian': 'Неxт иc {name}'},
    'The first today is: {name}': {'russian': 'де фирст тодаЙ ис: {name}'},
    'The last person is: {name}': {'russsian': 'де ласт персон ис {name}'}
}


def say(text, **variables):
    if config.language and config.language != 'english':
        text = sentences_transliterated[text][config.language]
        language = config.language
    else:
        language = 'english'

    for key, content in variables.items():
        if key == 'name' and content in config.people_transliterated and \
                config.language in config.people_transliterated[content]:
            print(content)
            content = config.people_transliterated[content][config.language]

        text = text.replace(f'{{{key}}}', content)

    print(f'Say: {text}')
    os.system(f'echo {text} | festival --tts --language {language}')


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


def remove_missing(people, missing_people):
    if missing_people is None:
        return

    for missing_person in missing_people:
        missing_person_found = False
        for person in people:
            if person.lower() == missing_person.lower():
                people.remove(person)
                missing_person_found = True

        if missing_person_found:
            print(f'{missing_person} removed')
        else:
            print(f'Warning: tried to remove "{missing_person}" but not found')


def main(missing=None, only=None):
    starts_process = time.time()

    if only is not None:
        people = only
    else:
        people = config.people[:]

        remove_missing(people, missing)
        remove_people_off_today(people)

    people.sort()

    print('People participating today:', ", ".join(people))

    say('Good morning!')
    count_people = 0
    total_people = len(people)

    while len(people) > 0:
        chosen = random.choice(people)

        if count_people == 0:
            say('The first today is: {name}', name=chosen)
        elif len(people) == 1:
            say('The last person is: {name}', name=chosen)
        else:
            say('Next is: {name}', name=chosen)

        starts_person = time.time()
        people.remove(chosen)
        print(f'This is {count_people + 1} of {total_people}')
        print()
        input('Press enter when finished\n')
        elapsed = time.time() - starts_person

        write_to_file(chosen, elapsed)
        count_people += 1

    say('Have a nice day')
    elapsed_process = time.time() - starts_process
    print()
    print(f'Total time: {elapsed_process / 60:.1f} minutes')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--missing', nargs='+', help='Missing people. Case insensitive', required=False)
    parser.add_argument('--only', nargs='+', help='Only this people', required=False)

    args = parser.parse_args()
    main(missing=args.missing, only=args.only)
