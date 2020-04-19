# pass-the-conch
Pass the conch is a sentece from Lord of the Flies (https://en.wikipedia.org/wiki/Lord_of_the_Flies ).

Who has the conch can speak.

In a small team meeting where everyone need to explain a quick report of what happened yesterday and what is going to happen today: often there is a "who goes first" moment, "who would like to start today", "who is next now?".

Using `pass-the-conch` the computer will decide randomly the order and change it every day.

## Requirements
 - Python 3
 - Festival installed

## Usage
 - Copy the file `config.example.py` to `config.py`
 - Edit the names of the people
 - Execute `pass-the-conch.py`

If some people are not in the meeting today:
`pass-the-conch.py --missing paul john`

## About people_transliterated
In the config.py there is a language setting and a people_transliterated.

`festival` software can synthesize different languages. In our team we wanted festival to read English in Russian accent: for this we transliterated to Russian. The names also need to be transliterated so this is what we did.
