import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pyttsx3
import os
import random
from pathlib import Path
import threading
import time
import winsound
import pygame
import re

class AlphabetLearningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎓 Alphabet Learning App for Beloved")
        self.root.state('zoomed')  # Make window full screen
        self.root.configure(bg="#FFE5E5")  # Light pink background
        
        # Set window icon
        try:
            icon_path = Path("abc.png")
            if icon_path.exists():
                self.root.iconphoto(True, tk.PhotoImage(file=str(icon_path)))
        except Exception as e:
            pass  # Silently fail if icon cannot be set
        
        # Initialize text-to-speech engine
        self.engine = None
        self.init_text_to_speech()
        
        # Initialize audio system
        self.init_audio()
        
        # Musical features
        self.is_playing_music = False
        self.current_melody_thread = None
        self.music_volume = 1.0  # Set to maximum for louder playback
        
        # Quiz mode variables
        self.quiz_mode = False
        self.quiz_score = 0
        self.quiz_total = 0
        self.current_quiz_question = None
        
        # Song mode variables
        self.song_mode = False
        self.current_song_line = 0
        self.current_song_index = 0
        self.songs = [
            {
                "title": "Row, Row, Row Your Boat",
                "lyrics": [
                    "Row, row, row your boat",
                    "Gently down the stream",
                    "Merrily, merrily, merrily, merrily",
                    "Life is but a dream"
                ],
                "melody": ["C4", "C4", "C4", "D4", "E4", "E4", "D4", "E4", "F4", "G4", "C5", "G4", "E4", "C4", "G4", "F4", "E4", "D4", "C4"],
                "tempo": 120
            },
            {
                "title": "Baa Baa Black Sheep",
                "lyrics": [
                    "Baa, baa, black sheep",
                    "Have you any wool?",
                    "Yes sir, yes sir",
                    "Three bags full",
                    "One for the master",
                    "One for the dame",
                    "And one for the little boy",
                    "Who lives down the lane"
                ],
                "melody": ["C4", "C4", "G4", "G4", "A4", "A4", "G4", "F4", "F4", "E4", "E4", "D4", "D4", "C4", "G4", "G4", "F4", "F4", "E4", "E4", "D4", "G4", "G4", "F4", "F4", "E4", "E4", "D4", "C4"],
                "tempo": 100
            },
            {
                "title": "Mary Had a Little Lamb",
                "lyrics": [
                    "Mary had a little lamb",
                    "Little lamb, little lamb",
                    "Mary had a little lamb",
                    "Its fleece was white as snow",
                    "And everywhere that Mary went",
                    "Mary went, Mary went",
                    "Everywhere that Mary went",
                    "The lamb was sure to go"
                ],
                "melody": ["E4", "D4", "C4", "D4", "E4", "E4", "E4", "D4", "D4", "D4", "E4", "G4", "G4", "E4", "D4", "C4", "D4", "E4", "E4", "E4", "E4", "D4", "D4", "E4", "D4", "C4"],
                "tempo": 110
            },
            {
                "title": "Five Little Monkeys",
                "lyrics": [
                    "Five little monkeys jumping on the bed",
                    "One fell off and bumped his head",
                    "Mama called the doctor and the doctor said",
                    "No more monkeys jumping on the bed!",
                    "Four little monkeys jumping on the bed",
                    "One fell off and bumped his head",
                    "Mama called the doctor and the doctor said",
                    "No more monkeys jumping on the bed!"
                ],
                "melody": ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5", "C5", "B4", "A4", "G4", "F4", "E4", "D4", "C4", "C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"],
                "tempo": 90
            },
            {
                "title": "Humpty Dumpty",
                "lyrics": [
                    "Humpty Dumpty sat on a wall",
                    "Humpty Dumpty had a great fall",
                    "All the king's horses",
                    "And all the king's men",
                    "Couldn't put Humpty together again"
                ],
                "melody": ["C4", "E4", "G4", "C5", "G4", "E4", "C4", "G4", "E4", "C4", "F4", "A4", "C5", "A4", "F4", "C4", "F4", "A4", "C5", "A4", "F4", "C4"],
                "tempo": 80
            },
            {
                "title": "The Alphabet Song",
                "lyrics": [
                    "A, B, C, D, E, F, G",
                    "H, I, J, K, L, M, N, O, P",
                    "Q, R, S, T, U, V",
                    "W, X, Y, and Z",
                    "Now I know my ABCs",
                    "Next time won't you sing with me?"
                ],
                "melody": ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5", "D5", "E5", "F5", "G5", "A5", "B5", "C6", "C6", "B5", "A5", "G5", "F5", "E5", "D5", "C5", "B4", "A4", "G4", "F4", "E4", "D4", "C4"],
                "tempo": 100
            },
            # {
            #     "title": "Pussy Cat Pussy Cat",
            #     "lyrics": [
            #         "Pussy cat, pussy cat, where have you been?",
            #         "I've been to London to visit the Queen",
            #         "Pussy cat, pussy cat, what did you there?",
            #         "I frightened a little mouse under her chair"
            #     ],
            #     "melody": ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5", "C5", "B4", "A4", "G4", "F4", "E4", "D4", "C4", "C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"],
            #     "tempo": 95
            # },
            {
                "title": "One Two Buckle My Shoe",
                "lyrics": [
                    "One, two, buckle my shoe",
                    "Three, four, knock at the door",
                    "Five, six, pick up sticks",
                    "Seven, eight, lay them straight",
                    "Nine, ten, a big fat hen",
                    "Eleven, twelve, dig and delve",
                    "Thirteen, fourteen, maids a-courting",
                    "Fifteen, sixteen, maids in the kitchen"
                ],
                "melody": ["C4", "C4", "D4", "D4", "E4", "E4", "F4", "F4", "G4", "G4", "A4", "A4", "B4", "B4", "C5", "C5", "D5", "D5", "E5", "E5", "F5", "F5", "G5", "G5"],
                "tempo": 120
            },
            {
                "title": "Head Shoulders Knees and Toes",
                "lyrics": [
                    "Head, shoulders, knees, and toes",
                    "Knees and toes",
                    "Head, shoulders, knees, and toes",
                    "Knees and toes",
                    "And eyes, and ears, and mouth, and nose",
                    "Head, shoulders, knees, and toes",
                    "Knees and toes"
                ],
                "melody": ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5", "C5", "B4", "A4", "G4", "F4", "E4", "D4", "C4", "C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5", "C5", "B4", "A4", "G4", "F4", "E4", "D4", "C4"],
                "tempo": 110
            },
            {
                "title": "Old MacDonald Had a Farm",
                "lyrics": [
                    "Old MacDonald had a farm",
                    "E-I-E-I-O",
                    "And on his farm he had a cow",
                    "E-I-E-I-O",
                    "With a moo moo here",
                    "And a moo moo there",
                    "Here a moo, there a moo",
                    "Everywhere a moo moo",
                    "Old MacDonald had a farm",
                    "E-I-E-I-O",
                    "And on his farm he had a pig",
                    "E-I-E-I-O",
                    "With an oink oink here",
                    "And an oink oink there",
                    "Here an oink, there an oink",
                    "Everywhere an oink oink",
                    "Old MacDonald had a farm",
                    "E-I-E-I-O"
                ],
                "melody": ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5", "C5", "B4", "A4", "G4", "F4", "E4", "D4", "C4", "C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5", "C5", "B4", "A4", "G4", "F4", "E4", "D4", "C4", "C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5", "C5", "B4", "A4", "G4", "F4", "E4", "D4", "C4"],
                "tempo": 100
            },
            {
                "title": "Numbers Song 1 To 20",
                "lyrics": [
                    "One, two, three, four, five",
                    "Six, seven, eight, nine, ten",
                    "Eleven, twelve, thirteen, fourteen, fifteen",
                    "Sixteen, seventeen, eighteen, nineteen, twenty",
                    "Let's count from one to twenty",
                    "One, two, three, four, five",
                    "Six, seven, eight, nine, ten",
                    "Eleven, twelve, thirteen, fourteen, fifteen",
                    "Sixteen, seventeen, eighteen, nineteen, twenty",
                    "Now we know our numbers one to twenty!"
                ],
                "melody": ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5", "D5", "E5", "F5", "G5", "A5", "B5", "C6", "C6", "B5", "A5", "G5", "F5", "E5", "D5", "C5", "B4", "A4", "G4", "F4", "E4", "D4", "C4", "C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5", "D5", "E5", "F5", "G5", "A5", "B5", "C6"],
                "tempo": 120
            },
            {
                "title": "Finger Family",
                "lyrics": [
                    "Daddy finger, daddy finger, where are you?",
                    "Here I am, here I am, how do you do?",
                    "Mommy finger, mommy finger, where are you?",
                    "Here I am, here I am, how do you do?",
                    "Brother finger, brother finger, where are you?",
                    "Here I am, here I am, how do you do?",
                    "Sister finger, sister finger, where are you?",
                    "Here I am, here I am, how do you do?",
                    "Baby finger, baby finger, where are you?",
                    "Here I am, here I am, how do you do?"
                ],
                "melody": ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5", "C5", "B4", "A4", "G4", "F4", "E4", "D4", "C4", "C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5", "C5", "B4", "A4", "G4", "F4", "E4", "D4", "C4", "C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5", "C5", "B4", "A4", "G4", "F4", "E4", "D4", "C4"],
                "tempo": 110
            },
            {
                "title": "Learn Transports Vehicles",
                "lyrics": [
                    "Car, car, car goes vroom vroom vroom",
                    "Bus, bus, bus goes beep beep beep",
                    "Train, train, train goes choo choo choo",
                    "Airplane, airplane goes zoom zoom zoom",
                    "Boat, boat, boat goes splash splash splash",
                    "Bicycle, bicycle goes ring ring ring",
                    "Motorcycle, motorcycle goes brr brr brr",
                    "Truck, truck, truck goes honk honk honk",
                    "Let's learn about transportation",
                    "All the vehicles that help us move!"
                ],
                "melody": ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5", "D5", "E5", "F5", "G5", "A5", "B5", "C6", "C6", "B5", "A5", "G5", "F5", "E5", "D5", "C5", "B4", "A4", "G4", "F4", "E4", "D4", "C4", "C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5", "D5", "E5", "F5", "G5", "A5", "B5", "C6"],
                "tempo": 115
            },
            {
                "title": "Johny Johny Yes Papa Baby",
                "lyrics": [
                    "Johny, Johny",
                    "Yes, Papa",
                    "Eating sugar?",
                    "No, Papa",
                    "Telling lies?",
                    "No, Papa",
                    "Open your mouth",
                    "Ha, ha, ha!",
                    "Johny, Johny",
                    "Yes, Papa",
                    "Eating sugar?",
                    "No, Papa",
                    "Telling lies?",
                    "No, Papa",
                    "Open your mouth",
                    "Ha, ha, ha!"
                ],
                "melody": ["C4", "C4", "D4", "D4", "E4", "E4", "F4", "F4", "G4", "G4", "A4", "A4", "B4", "B4", "C5", "C5", "C5", "C5", "B4", "B4", "A4", "A4", "G4", "G4", "F4", "F4", "E4", "E4", "D4", "D4", "C4", "C4"],
                "tempo": 100
            }
        ]
        
        # Separate navigation tracking
        self.learning_index = 0  # For learning mode navigation
        self.quiz_index = 0      # For quiz mode navigation
        
        # Alphabet data with letters, words, emojis, and image paths
        self.alphabet_data = [
            ("A", "Apple", "🍎", "apple"), ("B", "Ball", "⚽", "ball"), 
            ("C", "Cat", "🐱", "cat"), ("D", "Dog", "🐕", "dog"),
            ("E", "Elephant", "🐘", "elephant"), ("F", "Fish", "🐟", "fish"), 
            ("G", "Giraffe", "🦒", "giraffe"), ("H", "House", "🏠", "house"),
            ("I", "Ice Cream", "🍦", "ice_cream"), ("J", "Jellyfish", "🪼", "jellyfish"), 
            ("K", "Kangaroo", "🦘", "kangaroo"), ("L", "Lion", "🦁", "lion"),
            ("M", "Monkey", "🐒", "monkey"), ("N", "Nest", "🪺", "nest"), 
            ("O", "Orange", "🍊", "orange"), ("P", "Penguin", "🐧", "penguin"),
            ("Q", "Queen", "👑", "queen"), ("R", "Rabbit", "🐰", "rabbit"), 
            ("S", "Sun", "☀️", "sun"), ("T", "Tree", "🌳", "tree"),
            ("U", "Umbrella", "☂️", "umbrella"), ("V", "Violin", "🎻", "violin"), 
            ("W", "Whale", "🐋", "whale"), ("X", "Xylophone", "🎵", "xylophone"),
            ("Y", "Yatch", "🛥️", "yatch"), ("Z", "Zebra", "🦓", "zebra")
        ]
        
        # Object information data for detailed view
        self.object_info = {
            "apple": {
                "name": "Apple",
                "description": "A round, red fruit that grows on trees. Apples are sweet and crunchy, and they're good for your health!",
                "fun_facts": [
                    "🍎 Apples come in many colors: red, green, and yellow",
                    "🌳 Apple trees can live for over 100 years",
                    "💪 Eating apples helps keep the doctor away",
                    "🍎 There are over 7,500 different types of apples"
                    "Apple is one of the most popular and widely consumed fruits in the world. It belongs to the Rosaceae family and the Malus domestica species."\

"Apples originated in Central Asia, particularly in the region of modern-day Kazakhstan. They are typically round in shape with smooth skin that can be red, green, or yellow, and their flesh is white to pale yellow. The taste of apples varies depending on the variety, ranging from sweet to tart"
"Nutritionally, apples are rich in dietary fiber, especially pectin, as well as vitamin C and various antioxidants. These nutrients contribute to several health benefits. Eating apples may boost heart health, aid digestion, support weight management, and reduce the risk of developing certain chronic diseases such as type 2 diabetes."
"Apples are very versatile in their uses. They can be eaten fresh as a snack, juiced, used in baking (like in apple pies), added to salads, or made into sauces. Dried apples are also a popular and convenient snack."
"A well-known saying associated with the fruit is 'An apple a day keeps the doctor away,' which reflects the apple's reputation as a nutritious and health-promoting food."                ]
            },
            "ball": {
                "name": "Ball",
                "description": "A round object used for playing games and sports. Balls can bounce, roll, and be thrown!",
                "fun_facts": [
                    "⚽ Balls come in many sizes and colors",
                    "🏀 Basketballs are orange and bouncy",
                    "⚽ Soccer balls are black and white",
                    "🎾 Tennis balls are fuzzy and green"
                ]
            },
            "cat": {
                "name": "Cat",
                "description": "A furry pet animal that likes to sleep, play, and chase mice. Cats are very independent and clean!",
                "fun_facts": [
                    "🐱 Cats can sleep for 16 hours a day",
                    "😺 Cats have excellent night vision",
                    "🐾 Cats have retractable claws",
                    "😸 Cats purr when they're happy"
                ]
            },
            "dog": {
                "name": "Dog",
                "description": "A friendly pet animal that loves to play, walk, and be with people. Dogs are very loyal friends!",
                "fun_facts": [
                    "🐕 Dogs are descended from wolves",
                    "👃 Dogs have an amazing sense of smell",
                    "🐾 Dogs have wet noses to help them smell better",
                    "🦮 Dogs can learn many commands and tricks"
                ]
            },
            "elephant": {
                "name": "Elephant",
                "description": "A very large gray animal with a long trunk and big ears. Elephants are very smart and gentle!",
                "fun_facts": [
                    "🐘 Elephants are the largest land animals",
                    "🦷 Elephants have the longest teeth (tusks)",
                    "👂 Elephants have the biggest ears of any animal",
                    "🧠 Elephants have excellent memories"
                ]
            },
            "fish": {
                "name": "Fish",
                "description": "Animals that live in water and breathe through gills. Fish come in many beautiful colors!",
                "fun_facts": [
                    "🐟 Fish have been around for 500 million years",
                    "🌊 Fish live in oceans, rivers, and lakes",
                    "🐠 Some fish can change colors",
                    "🦈 Sharks are a type of fish"
                ]
            },
            "giraffe": {
                "name": "Giraffe",
                "description": "A tall animal with a very long neck and legs. Giraffes can reach leaves high up in trees!",
                "fun_facts": [
                    "🦒 Giraffes are the tallest animals on Earth",
                    "🦒 A giraffe's neck can be 6 feet long",
                    "🦒 Giraffes only need to sleep 2 hours a day",
                    "🦒 Baby giraffes are 6 feet tall when born"
                ]
            },
            "house": {
                "name": "House",
                "description": "A building where people live. Houses keep us safe, warm, and dry from the weather!",
                "fun_facts": [
                    "🏠 Houses can be made of wood, brick, or stone",
                    "🏠 Some houses have attics and basements",
                    "🏠 Houses have rooms for sleeping, eating, and playing",
                    "🏠 Houses have windows to let in light and air"
                ]
            },
            "ice_cream": {
                "name": "Ice Cream",
                "description": "A cold, sweet dessert made from milk and sugar. Ice cream comes in many delicious flavors!",
                "fun_facts": [
                    "🍦 Ice cream was invented in China over 4,000 years ago",
                    "🍦 Vanilla is the most popular ice cream flavor",
                    "🍦 Ice cream melts when it gets warm",
                    "🍦 Some ice cream has chocolate chips or sprinkles"
                ]
            },
            "jellyfish": {
                "name": "Jellyfish",
                "description": "Sea animals that look like jelly and float in the ocean. They have long tentacles!",
                "fun_facts": [
                    "🪼 Jellyfish have been around for 500 million years",
                    "🪼 Jellyfish don't have brains or hearts",
                    "🪼 Some jellyfish can glow in the dark",
                    "🪼 Jellyfish are made mostly of water"
                ]
            },
            "kangaroo": {
                "name": "Kangaroo",
                "description": "Australian animals that hop on their strong back legs. Baby kangaroos live in their mother's pouch!",
                "fun_facts": [
                    "🦘 Kangaroos can hop up to 30 feet in one jump",
                    "🦘 Baby kangaroos are called joeys",
                    "🦘 Kangaroos can't walk backwards",
                    "🦘 Kangaroos use their tails for balance"
                ]
            },
            "lion": {
                "name": "Lion",
                "description": "Large cats that live in groups called prides. Lions are known as the 'King of the Jungle'!",
                "fun_facts": [
                    "🦁 Lions are the only cats that live in groups",
                    "🦁 Male lions have big manes around their heads",
                    "🦁 Lions can roar very loudly",
                    "🦁 Lions are excellent hunters"
                ]
            },
            "monkey": {
                "name": "Monkey",
                "description": "Playful animals that love to climb trees and swing from branches. Monkeys are very smart!",
                "fun_facts": [
                    "🐒 Monkeys use their hands and feet to climb",
                    "🐒 Some monkeys can use tools",
                    "🐒 Monkeys communicate with sounds and gestures",
                    "🐒 Monkeys like to eat fruits and nuts"
                ]
            },
            "nest": {
                "name": "Nest",
                "description": "A home that birds build using twigs, grass, and other materials. Birds lay their eggs in nests!",
                "fun_facts": [
                    "🪺 Birds build nests to keep their eggs safe",
                    "🪺 Nests can be round, cup-shaped, or hanging",
                    "🪺 Some birds use mud to build their nests",
                    "🪺 Birds often return to the same nest each year"
                ]
            },
            "orange": {
                "name": "Orange",
                "description": "A round, orange fruit that grows on trees. Oranges are juicy and full of vitamin C!",
                "fun_facts": [
                    "🍊 Oranges are actually berries",
                    "🍊 Orange trees can live for 100 years",
                    "🍊 Oranges float in water",
                    "🍊 Orange juice is very healthy for you"
                ]
            },
            "penguin": {
                "name": "Penguin",
                "description": "Birds that cannot fly but are excellent swimmers. Penguins live in cold places like Antarctica!",
                "fun_facts": [
                    "🐧 Penguins are excellent swimmers",
                    "🐧 Penguins huddle together to stay warm",
                    "🐧 Male penguins take care of the eggs",
                    "🐧 Penguins can jump out of water onto ice"
                ]
            },
            "queen": {
                "name": "Queen",
                "description": "A female ruler of a country. Queens wear beautiful crowns and live in palaces!",
                "fun_facts": [
                    "👑 Queens often wear beautiful crowns",
                    "👑 Queens live in big palaces",
                    "👑 Queens help make important decisions",
                    "👑 Queens are respected leaders"
                ]
            },
            "rabbit": {
                "name": "Rabbit",
                "description": "Small, furry animals with long ears and fluffy tails. Rabbits love to hop and eat carrots!",
                "fun_facts": [
                    "🐰 Rabbits can hop up to 3 feet high",
                    "🐰 Rabbits have very good hearing",
                    "🐰 Rabbits can turn their ears 180 degrees",
                    "🐰 Baby rabbits are called bunnies"
                ]
            },
            "sun": {
                "name": "Sun",
                "description": "A bright, hot star that gives us light and warmth. The sun is at the center of our solar system!",
                "fun_facts": [
                    "☀️ The sun is actually a star",
                    "☀️ The sun is 93 million miles away from Earth",
                    "☀️ The sun gives us light and heat",
                    "☀️ Plants need sunlight to grow"
                ]
            },
            "tree": {
                "name": "Tree",
                "description": "Tall plants with a trunk, branches, and leaves. Trees give us oxygen and provide homes for animals!",
                "fun_facts": [
                    "🌳 Trees can live for hundreds of years",
                    "🌳 Trees give us oxygen to breathe",
                    "🌳 Trees provide homes for birds and animals",
                    "🌳 Trees help clean the air"
                ]
            },
            "umbrella": {
                "name": "Umbrella",
                "description": "A tool that protects us from rain and sun. Umbrellas have a handle and a fabric top!",
                "fun_facts": [
                    "☂️ Umbrellas were invented in ancient China",
                    "☂️ Umbrellas can be many different colors",
                    "☂️ Umbrellas protect us from rain and sun",
                    "☂️ Some umbrellas are very big and fancy"
                ]
            },
            "violin": {
                "name": "Violin",
                "description": "A musical instrument with strings that you play with a bow. Violins make beautiful music!",
                "fun_facts": [
                    "🎻 Violins have four strings",
                    "🎻 Violins are made of wood",
                    "🎻 You play violin with a bow",
                    "🎻 Violins can make high and low sounds"
                ]
            },
            "whale": {
                "name": "Whale",
                "description": "Very large sea animals that breathe air. Whales are gentle giants of the ocean!",
                "fun_facts": [
                    "🐋 Whales are the largest animals in the ocean",
                    "🐋 Whales breathe air through blowholes",
                    "🐋 Whales can sing beautiful songs",
                    "🐋 Baby whales are called calves"
                ]
            },
            "xylophone": {
                "name": "Xylophone",
                "description": "A musical instrument with wooden bars that you hit with mallets. Xylophones make bright, happy sounds!",
                "fun_facts": [
                    "🎵 Xylophones have wooden bars of different sizes",
                    "🎵 You hit the bars with special mallets",
                    "🎵 Bigger bars make lower sounds",
                    "🎵 Xylophones are fun to play"
                ]
            },
            "yatch": {
                "name": "Yacht",
                "description": "A fancy boat used for pleasure and recreation. Yachts are like floating houses on the water!",
                "fun_facts": [
                    "🛥️ Yachts are luxury boats",
                    "🛥️ Yachts can have bedrooms and kitchens",
                    "🛥️ Yachts are used for fun trips on the water",
                    "🛥️ Some yachts are very big and expensive"
                ]
            },
            "zebra": {
                "name": "Zebra",
                "description": "Horse-like animals with black and white stripes. Each zebra has a unique stripe pattern!",
                "fun_facts": [
                    "🦓 No two zebras have the same stripe pattern",
                    "🦓 Zebras are related to horses",
                    "🦓 Zebras live in groups called herds",
                    "🦓 Zebras can run very fast to escape predators"
                ]
            }
        }
        
        # Image cache
        self.image_cache = {}
        self.current_image = None
        
        # Create images directory if it doesn't exist
        self.images_dir = Path("images")
        self.images_dir.mkdir(exist_ok=True)
        
        self.setup_ui()
        self.learning_frame.pack(expand=True, fill="both")
        
        # Ensure UI is fully rendered before displaying first letter
        self.root.update_idletasks()
        # Do not call self.update_display() with speech on startup
        # self.root.after(200, self.update_display)
    
    def init_text_to_speech(self):
        """Initialize text-to-speech engine"""
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)
            self.engine.setProperty('volume', 0.8)
            # Get available voices and set a child-friendly voice if available
            voices = self.engine.getProperty('voices')
            for voice in voices:
                if 'female' in voice.name.lower() or 'child' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
        except Exception as e:
            pass  # Silently fail if text-to-speech is not available
    
    def init_audio(self):
        """Initialize audio system"""
        try:
            pygame.mixer.init()
        except Exception as e:
            pass  # Silently fail if audio is not available
    
    def play_note(self, note, duration=0.3):
        """Play a musical note using winsound"""
        try:
            # Simple frequency mapping for basic notes
            note_frequencies = {
                'C4': 261, 'D4': 293, 'E4': 329, 'F4': 349, 'G4': 392, 'A4': 440, 'B4': 493,
                'C5': 523, 'D5': 587, 'E5': 659, 'F5': 698, 'G5': 784, 'A5': 880, 'B5': 987,
                'C6': 1047
            }
            frequency = note_frequencies.get(note, 440)
            winsound.Beep(frequency, int(duration * 1000))
        except Exception as e:
            pass  # Silently fail if audio is not available
    
    def play_melody(self, melody, tempo):
        """Play a melody using threading to avoid blocking"""
        if self.current_melody_thread and self.current_melody_thread.is_alive():
            self.current_melody_thread.join(timeout=0.1)
        
        def melody_thread():
            try:
                for note in melody:
                    if not self.is_playing_music:
                        break
                    self.play_note(note, 60/tempo)
                    time.sleep(0.1)
            except Exception as e:
                pass  # Silently fail if melody playback fails
        
        self.current_melody_thread = threading.Thread(target=melody_thread)
        self.current_melody_thread.daemon = True
        self.current_melody_thread.start()
    
    def stop_music(self):
        """Stop current music playback and any playing music file, and stop song line updater."""
        self.is_playing_music = False
        if self.current_melody_thread and self.current_melody_thread.is_alive():
            self.current_melody_thread.join(timeout=0.1)
        # Also stop the music file
        self.stop_music_file()
        # Stop the song line updater
        if hasattr(self, 'song_line_updater_active'):
            self.song_line_updater_active = False
    
    def setup_ui(self):
        """Set up the user interface"""
        # Main frame
        main_frame = tk.Frame(self.root, bg="#FFE5E5")
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)  # Less padding
        self.main_frame = main_frame

        # Main Menu Frame
        self.main_menu_frame = tk.Frame(main_frame, bg="#FFE5E5")
        self.main_menu_frame.pack(expand=True, fill="both")

        menu_title = tk.Label(
            self.main_menu_frame,
            text="🎓 Alphabet Learning App for Kids",
            font=("Comic Sans MS", 32, "bold"),
            bg="#FFE5E5",
            fg="#FF6B9D"
        )
        menu_title.pack(pady=40)

        menu_button_frame = tk.Frame(self.main_menu_frame, bg="#FFE5E5")
        menu_button_frame.pack(pady=30)

        learn_btn = tk.Button(
            menu_button_frame,
            text="📚 Learning Mode",
            command=self.enter_learning_mode,
            font=("Comic Sans MS", 22, "bold"),
            bg="#4A90E2",
            fg="WHITE",
            relief="groove",
            borderwidth=5,
            padx=60,
            pady=30,
            cursor="hand2"
        )
        learn_btn.pack(pady=15, fill="x")

        quiz_btn = tk.Button(
            menu_button_frame,
            text="🎯 Quiz Mode",
            command=self.enter_quiz_mode,
            font=("Comic Sans MS", 22, "bold"),
            bg="#FFD700",
            fg="WHITE",
            relief="groove",
            borderwidth=5,
            padx=60,
            pady=30,
            cursor="hand2"
        )
        quiz_btn.pack(pady=15, fill="x")

        song_btn = tk.Button(
            menu_button_frame,
            text="🎵 Song Mode",
            command=self.enter_song_mode,
            font=("Comic Sans MS", 22, "bold"),
            bg="#9B59B6",
            fg="WHITE",
            relief="groove",
            borderwidth=5,
            padx=60,
            pady=30,
            cursor="hand2"
        )
        song_btn.pack(pady=15, fill="x")

        # Title and mode indicator
        title_frame = tk.Frame(main_frame, bg="#FFE5E5")
        title_frame.pack(fill="x", pady=(0, 10))
        self.title_frame = title_frame

        self.mode_label = tk.Label(
            title_frame,
            text="",
            font=("Comic Sans MS", 14, "bold"),
            bg="#4A90E2",
            fg="white",
            padx=10,
            pady=5
        )
        self.mode_label.pack(side="right")
        
        # Content frame - this will contain the learning/quiz content
        self.content_frame = tk.Frame(main_frame, bg="#FFE5E5")
        self.content_frame.pack(expand=True, fill="both", pady=(0, 10))
        
        # Learning mode content
        self.setup_learning_mode()
        
        # Quiz mode content (hidden initially)
        self.setup_quiz_mode()
        
        # Song mode content (hidden initially)
        self.setup_song_mode()
        
        # Bind keyboard events
        self.root.bind("<Left>", lambda e: self.previous_letter())
        self.root.bind("<Right>", lambda e: self.next_letter())
        self.root.bind("<space>", lambda e: self.speak_letter())
        self.root.bind("<Return>", lambda e: self.speak_letter())
        self.root.bind("<q>", lambda e: self.toggle_mode())
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        # Show main menu on startup
        self.show_main_menu()

        # Add a File menu with Exit submenu
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=self.on_closing)
        menubar.add_cascade(label="File", menu=filemenu)
        self.root.config(menu=menubar)
    
    def show_main_menu(self):
        self.stop_music()  # Stop any music and song line updater when returning to main menu
        self.learning_frame.pack_forget()
        self.quiz_frame.pack_forget()
        self.song_frame.pack_forget()
        self.main_menu_frame.pack(expand=True, fill="both")
        self.title_frame.pack_forget()
        self.content_frame.pack_forget()

    def enter_learning_mode(self):
        self.quiz_mode = False
        self.song_mode = False
        self.main_menu_frame.pack_forget()
        self.title_frame.pack(fill="x", pady=(0, 10))
        self.content_frame.pack(expand=True, fill="both", pady=(0, 10))
        self.learning_frame.pack(expand=True, fill="both")
        self.quiz_frame.pack_forget()
        self.song_frame.pack_forget()
        self.mode_label.config(text="📚 Learning Mode", bg="#4A90E2")
        self.learning_index = 0  # Reset learning index
        self.update_display()
        # Speak only when user enters learning mode
        self.speak_letter()

    def enter_quiz_mode(self):
        self.quiz_mode = True
        self.song_mode = False
        self.main_menu_frame.pack_forget()
        self.title_frame.pack(fill="x", pady=(0, 10))
        self.content_frame.pack(expand=True, fill="both", pady=(0, 10))
        self.quiz_frame.pack(expand=True, fill="both")
        self.learning_frame.pack_forget()
        self.song_frame.pack_forget()
        self.mode_label.config(text="🎯 Quiz Mode", bg="#FFD700")
        # Quiz session setup
        self.quiz_total_questions = 10
        self.quiz_score = 0
        self.quiz_total = 0
        self.remaining_quiz_indices = random.sample(range(len(self.alphabet_data)), self.quiz_total_questions)
        self.quiz_index = None  # No current question yet
        self.current_quiz_question = None
        self.quiz_finished = False
        # Hide answer and spelling UI until quiz starts
        self.answer_frame.pack_forget()
        self.feedback_label.pack_forget()
        self.spelling_entry.pack_forget()
        self.check_spelling_button.pack_forget()
        self.spelling_feedback_label.pack_forget()
        # Remove any existing start quiz button from navigation frame
        if hasattr(self, 'start_quiz_button'):
            self.start_quiz_button.pack_forget()
        self.question_label.config(text="Click 'Start Quiz' to begin!", fg="#333333")
        self.start_quiz_button.pack(pady=20)

    def enter_song_mode(self):
        self.quiz_mode = False
        self.song_mode = True
        self.main_menu_frame.pack_forget()
        self.title_frame.pack(fill="x", pady=(0, 10))
        self.content_frame.pack(expand=True, fill="both", pady=(0, 10))
        self.song_frame.pack(expand=True, fill="both")
        self.learning_frame.pack_forget()
        self.quiz_frame.pack_forget()
        self.mode_label.config(text="🎵 Song Mode", bg="#9B59B6")
        self.current_song_index = 0  # Reset song index
        self.current_song_line = 0   # Reset song line
        self.update_song_display()

    def setup_learning_mode(self):
        """Set up the learning mode interface"""
        self.learning_frame = tk.Frame(self.content_frame, bg="#FFE5E5")
        
        # Letter display
        self.letter_label = tk.Label(
            self.learning_frame,
            text="",
            font=("Arial", 80, "bold"),  # Smaller font
            bg="#FFE5E5",
            fg="#4A90E2"
        )
        self.letter_label.pack(pady=10)  # Less padding
        
        # Word display
        self.word_label = tk.Label(
            self.learning_frame,
            text="",
            font=("Comic Sans MS", 24, "bold"),
            bg="#FFE5E5",
            fg="#FF6B9D"
        )
        self.word_label.pack(pady=5)
        
        # Image display placeholder
        self.image_frame = tk.Frame(self.learning_frame, bg="#FFE5E5", width=200, height=140)
        self.image_frame.pack(pady=10)
        self.image_frame.pack_propagate(False)
        
        self.image_label = tk.Label(
            self.image_frame,
            text="🖼️",
            font=("Arial", 60),
            bg="#FFE5E5",
            cursor="hand2"  # Make it look clickable
        )
        self.image_label.pack(expand=True)
        
        # Click hint text
        self.click_hint_label = tk.Label(
            self.learning_frame,
            text="👆 Click the image to learn more!",
            font=("Comic Sans MS", 12, "bold"),
            bg="#FFE5E5",
            fg="#4A90E2"
        )
        self.click_hint_label.pack(pady=5)
        
        # NAVIGATION CONTROLS DIRECTLY IN LEARNING FRAME
        nav_frame = tk.Frame(self.learning_frame, bg="#FFE5E5", height=250)  # Increased height
        nav_frame.pack(pady=20, fill="x")  # More padding
        nav_frame.pack_propagate(False)
        
        # Test label
        test_label = tk.Label(
            nav_frame,
            text="🎮 Navigation Controls",
            font=("Comic Sans MS", 18, "bold"),  # Larger title
            bg="#FFE5E5",
            fg="#4A90E2"
        )
        test_label.pack(pady=10)  # More padding
        
        # Button container
        button_frame = tk.Frame(nav_frame, bg="#FFE5E5")
        button_frame.pack(pady=15)  # More padding
        
        # Navigation buttons - much larger design
        self.prev_button = tk.Button(
            button_frame,
            text="⬅️ Previous",
            command=self.previous_letter,
            font=("Comic Sans MS", 18, "bold"),  # Larger font
            bg="#4A90E2",
            fg="WHITE",
            relief="groove",
            borderwidth=5,  # Thicker border
            padx=40,  # Much more horizontal padding
            pady=20,  # Much more vertical padding
            cursor="hand2"
        )
        self.prev_button.pack(side="left", padx=15, pady=10)  # Much more spacing
        
        # Add a mute/unmute button with a speaker icon to the navigation row
        self.speech_muted = False
        def toggle_speech():
            self.speech_muted = not self.speech_muted
            if self.speech_muted:
                self.mute_button.config(text="🔇")
            else:
                self.mute_button.config(text="🔊")
        self.mute_button = tk.Button(
            button_frame,
            text="🔊",
            command=toggle_speech,
            font=("Arial", 18, "bold"),  # Larger font
            bg="#FFD700",
            fg="WHITE",
            relief="groove",
            borderwidth=5,  # Thicker border
            padx=20,  # More horizontal padding
            pady=15,  # More vertical padding
            cursor="hand2"
        )
        self.mute_button.pack(side="left", padx=15, pady=10)
        
        self.speak_button = tk.Button(
            button_frame,
            text="🔊 Say It!",
            command=self.speak_letter,
            font=("Comic Sans MS", 18, "bold"),  # Larger font
            bg="#FF6B9D",
            fg="WHITE",
            relief="groove",
            borderwidth=5,  # Thicker border
            padx=40,  # Much more horizontal padding
            pady=20,  # Much more vertical padding
            cursor="hand2"
        )
        self.speak_button.pack(side="left", padx=15, pady=10)  # Much more spacing
        
        self.next_button = tk.Button(
            button_frame,
            text="Next ➡️",
            command=self.next_letter,
            font=("Comic Sans MS", 18, "bold"),  # Larger font
            bg="#4A90E2",
            fg="WHITE",
            relief="groove",
            borderwidth=5,  # Thicker border
            padx=40,  # Much more horizontal padding
            pady=20,  # Much more vertical padding
            cursor="hand2"
        )
        self.next_button.pack(side="left", padx=15, pady=10)  # Much more spacing
        
        # Progress label
        self.progress_label = tk.Label(
            nav_frame,
            text="Letter 1 of 26",
            font=("Comic Sans MS", 14, "bold"),  # Larger font
            bg="#FFE5E5",
            fg="#666666"
        )
        self.progress_label.pack(pady=10)  # More padding
        
        # Add 'Back to Main Menu' button in the navigation row
        self.back_to_menu_button = tk.Button(
            button_frame,
            text="🏠 Main Menu",
            command=self.show_main_menu,
            font=("Comic Sans MS", 18, "bold"),
            bg="#27AE60",  # Green
            fg="WHITE",
            relief="groove",
            borderwidth=5,
            padx=40,
            pady=20,
            cursor="hand2"
        )
        self.back_to_menu_button.pack(side="left", padx=15, pady=10)
    
    def setup_quiz_mode(self):
        """Set up the quiz mode interface (with dedicated frames for each section)"""
        self.quiz_frame = tk.Frame(self.content_frame, bg="#FFE5E5")
        
        # Title frame
        title_frame = tk.Frame(self.quiz_frame, bg="#FFE5E5")
        title_frame.pack(fill="x", pady=(30, 0))
        quiz_title = tk.Label(
            title_frame,
            text="🎯 Alphabet Quiz!",
            font=("Comic Sans MS", 28, "bold"),
            bg="#FFE5E5",
            fg="#FF6B9D"
        )
        quiz_title.pack()
        
        # Score and progress frame
        score_progress_frame = tk.Frame(self.quiz_frame, bg="#FFE5E5")
        score_progress_frame.pack(fill="x", pady=(10, 0))
        self.score_label = tk.Label(
            score_progress_frame,
            text="Score: 0/0",
            font=("Comic Sans MS", 18, "bold"),
            bg="#FFE5E5",
            fg="#4A90E2"
        )
        self.score_label.pack(side="left", padx=40)
        self.quiz_progress_label = tk.Label(
            score_progress_frame,
            text="Quiz Mode - Letter 1 of 26",
            font=("Comic Sans MS", 14, "bold"),
            bg="#FFE5E5",
            fg="#666666"
        )
        self.quiz_progress_label.pack(side="right", padx=40)

        # Question frame
        question_frame = tk.Frame(self.quiz_frame, bg="#FFE5E5")
        question_frame.pack(fill="x", pady=(20, 0))
        self.question_label = tk.Label(
            question_frame,
            text="Click 'Start Quiz' to begin!",
            font=("Comic Sans MS", 24, "bold"),
            bg="#FFE5E5",
            fg="#333333",
            wraplength=800,
            justify="center"
        )
        self.question_label.pack(fill="x")
        
        # Start Quiz button
        self.start_quiz_button = tk.Button(
            self.quiz_frame,
            text="Start Quiz",
            font=("Comic Sans MS", 18, "bold"),
            bg="#27AE60",
            fg="white",
            command=self.start_quiz_session
        )
        self.start_quiz_button.pack(pady=20)

        # Answer frame
        self.answer_frame = tk.Frame(self.quiz_frame, bg="#FFE5E5")
        self.answer_buttons = []

        # Feedback label for correct/incorrect
        self.feedback_label = tk.Label(self.quiz_frame, text="", font=("Comic Sans MS", 18, "bold"), bg="#FFE5E5", fg="#333333")

        # Spelling frame
        spelling_frame = tk.Frame(self.quiz_frame, bg="#FFE5E5")
        self.spelling_entry = tk.Entry(spelling_frame, font=("Comic Sans MS", 16), width=16)
        self.check_spelling_button = tk.Button(spelling_frame, text="Check Spelling", font=("Comic Sans MS", 14), command=self.check_spelling)
        self.spelling_feedback_label = tk.Label(spelling_frame, text="", font=("Comic Sans MS", 14), bg="#FFE5E5", fg="#333333")

        # Navigation frame (only Back to Main Menu)
        self.nav_frame = tk.Frame(self.quiz_frame, bg="#FFE5E5", height=100)
        self.nav_frame.pack(side="bottom", fill="x", pady=(30, 10))
        self.nav_frame.pack_propagate(False)  # Prevent frame from shrinking
        self.quiz_back_to_menu_button = tk.Button(
            self.nav_frame,
            text="⬅️ Back to Main Menu",
            command=self.show_main_menu,
            font=("Comic Sans MS", 14, "bold"),
            bg="#95A5A6",
            fg="WHITE",
            relief="groove",
            borderwidth=3,
            padx=15,
            pady=8,
            cursor="hand2"
        )
        self.quiz_back_to_menu_button.pack(side="left", padx=10, pady=10)
    
    def start_quiz_session(self):
        # Hide start button, show answer and spelling UI
        self.start_quiz_button.pack_forget()
        self.answer_frame.pack(pady=(20, 0))
        self.feedback_label.pack(pady=(10, 0))
        self.spelling_entry.pack(side="left", padx=5)
        self.check_spelling_button.pack(side="left", padx=5)
        self.spelling_feedback_label.pack(side="left", padx=5)
        self.spelling_entry.master.pack(pady=(10, 0))
        self.update_quiz_display()
    
    def update_display(self):
        """Update the display with current letter and word"""
        if self.quiz_mode:
            self.update_quiz_display()
        elif self.song_mode:
            self.update_song_display()
        else:
            self.update_learning_display()
    
    def update_learning_display(self):
        """Update learning mode display"""
        letter, word, emoji, _ = self.alphabet_data[self.learning_index]
        self.letter_label.config(text=letter)
        self.word_label.config(text=f"for {word}")
        self.load_image(letter)
        progress_text = f"Letter {self.learning_index + 1} of 26"
        self.progress_label.config(text=progress_text)
        self.prev_button.config(state="normal" if self.learning_index > 0 else "disabled")
        self.next_button.config(state="normal" if self.learning_index < 25 else "disabled")
        self.root.update_idletasks()
        # Do NOT call self.speak_letter() or any speech here
        # self.root.after(100, self.speak_letter)
    
    def update_quiz_display(self):
        # End of quiz
        if self.quiz_finished or not self.remaining_quiz_indices:
            remark = ""
            if self.quiz_score >= 8:
                remark = "Excellent! You are an Alphabet Star!"
            elif self.quiz_score >= 5:
                remark = "Good job! Keep practicing!"
            else:
                remark = "Keep trying! Practice makes perfect!"
            self.question_label.config(
                text=f"Quiz Finished!\nYour Score: {self.quiz_score}/{self.quiz_total_questions}\n\n{remark}",
                fg="#27AE60" if self.quiz_score > self.quiz_total_questions//2 else "#E74C3C"
            )
            for button in self.answer_buttons:
                button.destroy()
            self.answer_buttons.clear()
            self.spelling_entry.delete(0, 'end')
            self.spelling_entry.pack_forget()
            self.check_spelling_button.pack_forget()
            self.spelling_feedback_label.pack_forget()
            self.feedback_label.config(text="", fg="#333333")
            self.quiz_back_to_menu_button.config(state="normal")
            
            # Show Start Quiz button beside Main Menu in navigation frame
            self.start_quiz_button.config(text="Start Quiz Again")
            self.start_quiz_button.pack_forget()  # Remove from current location
            self.start_quiz_button.config(
                font=("Comic Sans MS", 14, "bold"),
                bg="#27AE60",
                fg="WHITE",
                relief="groove",
                borderwidth=3,
                padx=15,
                pady=8,
                cursor="hand2"
            )
            self.start_quiz_button.pack(side="left", padx=10, pady=10, in_=self.nav_frame)
            return
            
        # Remove Start Quiz button if present (unless at end)
        self.start_quiz_button.pack_forget()
        
        # Pick a new question if needed
        if self.quiz_index is None:
            self.quiz_index = self.remaining_quiz_indices.pop()
            self.current_quiz_question = None
            
        # Update score and progress
        self.score_label.config(text=f"Score: {self.quiz_score}/{self.quiz_total_questions}")
        self.quiz_progress_label.config(text=f"Question {self.quiz_total+1} of {self.quiz_total_questions}")
        
        # Always update the question label
        if self.current_quiz_question is None:
            self.generate_quiz_question()
        qtext = self.current_quiz_question.get('question_text', '')
        self.question_label.config(text=qtext, fg="#333333")
        
        # Clear and repopulate answer buttons
        for button in self.answer_buttons:
            button.destroy()
        self.answer_buttons.clear()
        for answer in self.current_quiz_question.get('answers', []):
            button = tk.Button(
                self.answer_frame,
                text=answer,
                font=("Comic Sans MS", 16, "bold"),
                bg="#4A90E2",
                fg="white",
                relief="groove",
                borderwidth=3,
                padx=20,
                pady=10,
                cursor="hand2",
                command=lambda a=answer: self.check_answer(a)
            )
            button.pack(side="left", padx=10)
            self.answer_buttons.append(button)
            
        # Reset feedback
        self.feedback_label.config(text="", fg="#333333")
        
        # Reset spelling
        self.spelling_entry.delete(0, 'end')
        self.spelling_entry.pack(side="left", padx=5)
        self.check_spelling_button.pack(side="left", padx=5)
        self.spelling_feedback_label.pack(side="left", padx=5)
        self.spelling_feedback_label.config(text="", fg="#333333")

    def generate_quiz_question(self):
        # Clear previous answer buttons
        for button in self.answer_buttons:
            button.destroy()
        self.answer_buttons.clear()
        # Use shuffled order for quiz
        current_idx = self.quiz_index if hasattr(self, 'quiz_order') else self.quiz_index
        question_types = ["letter_to_word", "word_to_letter", "emoji_to_letter"]
        question_type = random.choice(question_types)
        correct_letter, correct_word, correct_emoji, _ = self.alphabet_data[current_idx]
        # Generate wrong answers
        wrong_answers = []
        all_letters = [item[0] for item in self.alphabet_data]
        all_words = [item[1] for item in self.alphabet_data]
        while len(wrong_answers) < 3:
            if question_type == "letter_to_word":
                wrong_word = random.choice(all_words)
                if wrong_word != correct_word and wrong_word not in wrong_answers:
                    wrong_answers.append(wrong_word)
            elif question_type == "word_to_letter":
                wrong_letter = random.choice(all_letters)
                if wrong_letter != correct_letter and wrong_letter not in wrong_answers:
                    wrong_answers.append(wrong_letter)
            else:  # emoji_to_letter
                wrong_letter = random.choice(all_letters)
                if wrong_letter != correct_letter and wrong_letter not in wrong_answers:
                    wrong_answers.append(wrong_letter)
        # Create answers list
        answers = [correct_word if question_type == "letter_to_word" else correct_letter] + wrong_answers
        random.shuffle(answers)
        # Set up question (make it interactive with emoji)
        if question_type == "letter_to_word":
            question_text = f"What word starts with the letter {correct_letter} {correct_emoji}?"
            correct_answer = correct_word
        elif question_type == "word_to_letter":
            question_text = f"What letter does '{correct_word}' {correct_emoji} start with?"
            correct_answer = correct_letter
        else:  # emoji_to_letter
            question_text = f"What letter does this represent? {correct_emoji}"
            correct_answer = correct_letter
        self.current_quiz_question = {
            "type": question_type,
            "correct": correct_answer,
            "answers": answers,
            "question_text": question_text
        }

    def check_answer(self, selected_answer):
        correct_answer = self.current_quiz_question["correct"]
        # Disable all answer buttons after a pick
        for button in self.answer_buttons:
            button.config(state="disabled")
        if selected_answer == correct_answer:
            self.quiz_score += 1
            self.feedback_label.config(text="✅ Correct!", fg="#27AE60")
            self.animate_feedback(True)
        else:
            self.feedback_label.config(text=f"❌ Incorrect! The correct answer is {correct_answer}", fg="#E74C3C")
            self.animate_feedback(False)
        self.quiz_total += 1
        # Move to next question after a short delay
        self.quiz_index = None
        self.current_quiz_question = None
        self.quiz_frame.after(1200, self.update_quiz_display)

    def animate_feedback(self, correct):
        # Simple color flash animation
        orig_color = self.feedback_label.cget("fg")
        flash_color = "#27AE60" if correct else "#E74C3C"
        def flash():
            self.feedback_label.config(fg=flash_color)
            self.feedback_label.after(200, lambda: self.feedback_label.config(fg=orig_color))
        flash()

    def check_spelling(self):
        current_idx = self.quiz_index if self.quiz_index is not None else 0
        correct_word = self.alphabet_data[current_idx][1]
        user_spelling = self.spelling_entry.get().strip()
        if user_spelling.lower() == correct_word.lower():
            self.spelling_feedback_label.config(text="✅ Correct spelling!", fg="#27AE60")
        else:
            self.spelling_feedback_label.config(text=f"❌ Try again!", fg="#E74C3C")
    
    def toggle_mode(self):
        """Toggle between learning and quiz modes"""
        self.quiz_mode = not self.quiz_mode
        
        if self.quiz_mode:
            self.learning_frame.pack_forget()
            self.quiz_frame.pack(expand=True, fill="both")
            self.mode_label.config(text="🎯 Quiz Mode", bg="#FFD700")
        else:
            self.quiz_frame.pack_forget()
            self.learning_frame.pack(expand=True, fill="both")
            self.mode_label.config(text="📚 Learning Mode", bg="#4A90E2")
        
        self.update_display()
    
    def speak_letter(self):
        """Speak the current letter and word, unless muted. No keyboard sound in any mode."""
        if not self.engine or getattr(self, 'speech_muted', False):
            return
        
        def speak_only():
            try:
                letter, word, _, _ = self.alphabet_data[self.learning_index]
                self.engine.say(f"{letter} for {word}")
                self.engine.runAndWait()
            except Exception as e:
                pass  # Silently fail if speech fails
        
        # Run speech in a separate thread to avoid blocking
        speech_thread = threading.Thread(target=speak_only)
        speech_thread.daemon = True
        speech_thread.start()
    
    def next_letter(self):
        """Go to the next letter or quiz question, depending on mode"""
        if self.quiz_mode:
            # Quiz mode navigation only affects quiz_index
            if self.quiz_index < 25:
                self.quiz_index += 1
                self.current_quiz_question = None  # Force new question
                self.update_display()
        elif not self.song_mode:
            # Learning mode navigation only affects learning_index
            if self.learning_index < 25:
                self.learning_index += 1
                self.update_display()
                self.speak_letter()  # Speak automatically in learning mode
    
    def previous_letter(self):
        """Go to the previous letter or quiz question, depending on mode"""
        if self.quiz_mode:
            # Quiz mode navigation only affects quiz_index
            if self.quiz_index > 0:
                self.quiz_index -= 1
                self.current_quiz_question = None  # Force new question
                self.update_display()
        elif not self.song_mode:
            # Learning mode navigation only affects learning_index
            if self.learning_index > 0:
                self.learning_index -= 1
                self.update_display()
    
    def on_closing(self):
        """Handle window closing"""
        # Stop any playing music
        self.stop_music()
        
        # Stop text-to-speech
        if self.engine:
            try:
                self.engine.stop()
            except:
                pass
        
        self.root.destroy()

    def toggle_song_mode(self):
        """Toggle between learning and song modes"""
        if self.song_mode:
            # Switch back to learning mode
            self.song_mode = False
            self.song_frame.pack_forget()
            self.learning_frame.pack(expand=True, fill="both")
            self.mode_label.config(text="📚 Learning Mode", bg="#4A90E2")
        else:
            # Switch to song mode
            self.song_mode = True
            self.learning_frame.pack_forget()
            self.song_frame.pack(expand=True, fill="both")
            self.mode_label.config(text="🎵 Song Mode", bg="#9B59B6")
            # Reset to first song and first line
            self.current_song_index = 0
            self.current_song_line = 0
            self.update_song_display()
    
    def update_song_display(self):
        """Update song mode display"""
        current_song = self.songs[self.current_song_index]
        
        # Update song title
        self.song_title_label.config(text=f"🎵 {current_song['title']} 🎵")
        
        if self.current_song_line < len(current_song["lyrics"]):
            current_line = current_song["lyrics"][self.current_song_line]
            self.song_line_label.config(text=current_line)
            self.song_progress_label.config(text=f"Song {self.current_song_index + 1} of {len(self.songs)} - Line {self.current_song_line + 1} of {len(current_song['lyrics'])}")
            
            # Update button states
            if hasattr(self, 'song_prev_button'):
                self.song_prev_button.config(state="normal" if self.current_song_line > 0 else "disabled")
            if hasattr(self, 'song_next_button'):
                self.song_next_button.config(state="normal" if self.current_song_line < len(current_song['lyrics']) - 1 else "disabled")
        
        # Update song navigation button states
        if hasattr(self, 'song_prev_song_button'):
            self.song_prev_song_button.config(state="normal" if self.current_song_index > 0 else "disabled")
        if hasattr(self, 'song_next_song_button'):
            self.song_next_song_button.config(state="normal" if self.current_song_index < len(self.songs) - 1 else "disabled")
    
    def next_song_line(self):
        """Go to the next song line"""
        if self.current_song_line < len(self.songs[self.current_song_index]["lyrics"]) - 1:
            self.current_song_line += 1
            self.update_song_display()
    
    def previous_song_line(self):
        """Go to the previous song line"""
        if self.current_song_line > 0:
            self.current_song_line -= 1
            self.update_song_display()
    
    def next_song(self):
        """Go to the next song and play it automatically"""
        if self.current_song_index < len(self.songs) - 1:
            self.current_song_index += 1
            self.current_song_line = 0  # Reset to first line of new song
            self.update_song_display()
            self.play_current_song_melody()
    
    def previous_song(self):
        """Go to the previous song and play it automatically"""
        if self.current_song_index > 0:
            self.current_song_index -= 1
            self.current_song_line = 0  # Reset to first line of new song
            self.update_song_display()
            self.play_current_song_melody()
    
    def sing_current_line(self):
        """(Disabled) No singing or keyboard for sing line button in song mode."""
        pass

    def play_music_file(self, filename):
        """Play a music file using pygame"""
        try:
            pygame.mixer.music.load(filename)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play()
        except Exception as e:
            pass  # Silently fail if music file cannot be played
    
    def stop_music_file(self):
        """Stop currently playing music file"""
        try:
            pygame.mixer.music.stop()
        except Exception as e:
            pass  # Silently fail if music cannot be stopped

    def play_current_song_melody(self):
        """Play the melody for the current song"""
        if self.is_playing_music:
            self.stop_music()
        
        self.is_playing_music = True
        current_song = self.songs[self.current_song_index]
        
        # Normalize song title for file lookup
        import re
        def normalize_title(title):
            title = title.lower()
            title = re.sub(r'[^a-z0-9 ]', '', title)  # Remove punctuation
            title = title.replace(' ', '_')
            return title
        song_title_normalized = normalize_title(current_song["title"])
        music_file = None
        
        # Check for .mp3 file
        if os.path.exists(f"music/{song_title_normalized}.mp3"):
            music_file = f"music/{song_title_normalized}.mp3"
        # Check for .wav file
        elif os.path.exists(f"music/{song_title_normalized}.wav"):
            music_file = f"music/{song_title_normalized}.wav"
        
        # Special handling for 'Row, Row, Row Your Boat': only play file, no fallback
        if current_song["title"].lower().startswith("row, row, row your boat"):
            if music_file:
                try:
                    self.play_music_file(music_file)
                except Exception as e:
                    pass  # Silently fail if file cannot be played
            # Do not play keyboard melody fallback for this song
        else:
            if music_file:
                try:
                    self.play_music_file(music_file)
                except Exception as e:
                    # Fall back to generated melody
                    self.play_melody(current_song["melody"], current_song["tempo"])
            else:
                # Fall back to generated melody
                self.play_melody(current_song["melody"], current_song["tempo"])
        
        # Update the lyrics display
        def update_lines():
            try:
                if self.is_playing_music:
                    self.update_song_display()
                    self.root.after(1000, update_lines)
            except Exception as e:
                pass  # Silently fail if update fails
        
        update_lines()

    def next_quiz_question(self):
        if self.quiz_index < 25:
            self.quiz_index += 1
            self.current_quiz_question = None  # Force new question
            self.update_display()

    def previous_quiz_question(self):
        if self.quiz_index > 0:
            self.quiz_index -= 1
            self.current_quiz_question = None  # Force new question
            self.update_display()

    def setup_song_mode(self):
        """Set up the song mode interface"""
        self.song_frame = tk.Frame(self.content_frame, bg="#FFE5E5")
        # Song title (will be updated dynamically)
        self.song_title_label = tk.Label(
            self.song_frame,
            text="🎵 Row, Row, Row Your Boat 🎵",
            font=("Comic Sans MS", 28, "bold"),
            bg="#FFE5E5",
            fg="#9B59B6"
        )
        self.song_title_label.pack(pady=20)
        # Current line display
        self.song_line_label = tk.Label(
            self.song_frame,
            text="",
            font=("Comic Sans MS", 32, "bold"),
            bg="#FFE5E5",
            fg="#333333"
        )
        self.song_line_label.pack(pady=30)
        # Song navigation controls
        song_nav_frame = tk.Frame(self.song_frame, bg="#FFE5E5", height=250)
        song_nav_frame.pack(pady=20, fill="x")
        song_nav_frame.pack_propagate(False)
        # Song navigation title
        song_nav_title = tk.Label(
            song_nav_frame,
            text="🎵 Song Navigation Controls",
            font=("Comic Sans MS", 18, "bold"),
            bg="#FFE5E5",
            fg="#9B59B6"
        )
        song_nav_title.pack(pady=10)
        # Song button container
        song_button_frame = tk.Frame(song_nav_frame, bg="#FFE5E5")
        song_button_frame.pack(pady=15)
        song_button_frame.rowconfigure(0, weight=1, minsize=70)
        song_button_frame.rowconfigure(1, weight=1, minsize=55)
        # Row 0, Col 0: Next Line
        self.song_next_button = tk.Button(
            song_button_frame,
            text="Next Line ➡️",
            command=self.next_song_line,
            font=("Comic Sans MS", 16, "bold"),
            bg="#9B59B6",
            fg="WHITE",
            relief="groove",
            borderwidth=7,
            padx=25,
            pady=12,
            cursor="hand2"
        )
        self.song_next_button.grid(row=0, column=0, padx=10, pady=8, sticky="nsew")
        # Row 0, Col 1: Previous Song
        self.song_prev_song_button = tk.Button(
            song_button_frame,
            text="⬅️ Previous Song",
            command=self.previous_song,
            font=("Comic Sans MS", 16, "bold"),
            bg="#E67E22",
            fg="WHITE",
            relief="groove",
            borderwidth=7,
            padx=25,
            pady=12,
            cursor="hand2"
        )
        self.song_prev_song_button.grid(row=0, column=1, padx=10, pady=8, sticky="ew")
        # Row 0, Col 2: Next Song
        self.song_next_song_button = tk.Button(
            song_button_frame,
            text="Next Song ➡️",
            command=self.next_song,
            font=("Comic Sans MS", 16, "bold"),
            bg="#E67E22",
            fg="WHITE",
            relief="groove",
            borderwidth=7,
            padx=25,
            pady=12,
            cursor="hand2"
        )
        self.song_next_song_button.grid(row=0, column=2, padx=10, pady=8, sticky="nsew")
        # Row 0, Col 3: Previous Line
        self.song_prev_button = tk.Button(
            song_button_frame,
            text="⬅️ Previous Line",
            command=self.previous_song_line,
            font=("Comic Sans MS", 16, "bold"),
            bg="#9B59B6",
            fg="WHITE",
            relief="groove",
            borderwidth=7,
            padx=25,
            pady=12,
            cursor="hand2"
        )
        self.song_prev_button.grid(row=0, column=3, padx=10, pady=8, sticky="ew")
        # Row 1, Col 0: Play Music button
        self.play_music_button = tk.Button(
            song_button_frame,
            text="🎵 Play Melody!",
            command=self.play_current_song_melody,
            font=("Comic Sans MS", 16, "bold"),
            bg="#27AE60",
            fg="WHITE",
            relief="groove",
            borderwidth=7,
            padx=25,
            pady=12,
            cursor="hand2"
        )
        self.play_music_button.grid(row=1, column=0, padx=10, pady=8, sticky="ew")
        # Row 1, Col 1: Stop Music button
        self.stop_music_button = tk.Button(
            song_button_frame,
            text="⏹️ Stop Music",
            command=self.stop_music,
            font=("Comic Sans MS", 16, "bold"),
            bg="#95A5A6",
            fg="WHITE",
            relief="groove",
            borderwidth=7,
            padx=25,
            pady=12,
            cursor="hand2"
        )
        self.stop_music_button.grid(row=1, column=1, padx=10, pady=8, sticky="nsew")
        # Song progress label
        self.song_progress_label = tk.Label(
            song_nav_frame,
            text="Line 1 of 4",
            font=("Comic Sans MS", 14, "bold"),
            bg="#FFE5E5",
            fg="#666666"
        )
        self.song_progress_label.pack(pady=10)
        # Add 'Back to Main Menu' button
        self.song_back_to_menu_button = tk.Button(
            self.song_frame,
            text="⬅️ Back to Main Menu",
            command=self.show_main_menu,
            font=("Comic Sans MS", 14, "bold"),
            bg="#95A5A6",
            fg="WHITE",
            relief="groove",
            borderwidth=3,
            padx=15,
            pady=8,
            cursor="hand2"
        )
        self.song_back_to_menu_button.pack(pady=10)

    def load_image(self, letter):
        """Load and display image for the given letter"""
        try:
            # Check if image is already cached
            if letter in self.image_cache:
                image = self.image_cache[letter]
            else:
                # Try to load image from images directory
                image_path = self.images_dir / f"{letter.lower()}.png"
                if image_path.exists():
                    pil_image = Image.open(image_path)
                    # Resize image to fit the display area
                    pil_image = pil_image.resize((130, 130), Image.Resampling.LANCZOS)
                    image = ImageTk.PhotoImage(pil_image)
                    self.image_cache[letter] = image
                else:
                    # Create a placeholder image if file doesn't exist
                    placeholder = Image.new('RGB', (200, 200), color='#FFE5E5')
                    image = ImageTk.PhotoImage(placeholder)
                    self.image_cache[letter] = image
            
            # Update the image label and make it clickable
            if hasattr(self, 'image_label'):
                self.image_label.config(image=image)
                self.current_image = image  # Keep a reference
                # Bind click event to show detailed view
                self.image_label.bind("<Button-1>", self.show_object_details)
        except Exception as e:
            pass  # Silently fail if image loading fails
    
    def show_object_details(self, event=None):
        """Show detailed view of the current object"""
        if not self.quiz_mode and not self.song_mode:  # Only in learning mode
            letter, word, emoji, image_key = self.alphabet_data[self.learning_index]
            self.create_detail_window(letter, word, emoji, image_key)
    
    def create_detail_window(self, letter, word, emoji, image_key):
        """Create a new window with detailed object information"""
        # Create new window
        detail_window = tk.Toplevel(self.root)
        detail_window.title(f"Learn About {word}")
        detail_window.geometry("800x700")
        detail_window.configure(bg="#FFE5E5")
        detail_window.resizable(True, True)
        
        # Set window icon for detail window
        try:
            icon_path = Path("abc.png")
            if icon_path.exists():
                detail_window.iconphoto(True, tk.PhotoImage(file=str(icon_path)))
        except Exception as e:
            pass  # Silently fail if icon cannot be set
        
        # Center the window
        detail_window.transient(self.root)
        detail_window.grab_set()
        
        # Get object information
        obj_info = self.object_info.get(image_key, {
            "name": word,
            "description": f"A {word.lower()} that starts with the letter {letter}.",
            "fun_facts": [
                f"✨ {word} is a great word to learn!",
                f"🔤 {word} starts with the letter {letter}",
                f"📚 You can find {word} in many books",
                f"🎯 {word} is fun to say and learn about!"
            ]
        })
        
        # Main content frame with proper padding
        main_frame = tk.Frame(detail_window, bg="#FFE5E5")
        main_frame.pack(expand=True, fill="both", padx=15, pady=15)
        
        # Title section - more compact
        title_frame = tk.Frame(main_frame, bg="#FFE5E5")
        title_frame.pack(fill="x", pady=(0, 15))
        
        title_label = tk.Label(
            title_frame,
            text=f"{letter} for {word} {emoji}",
            font=("Comic Sans MS", 28, "bold"),
            bg="#FFE5E5",
            fg="#4A90E2"
        )
        title_label.pack()
        
        # Create a frame for image and description side by side
        content_frame = tk.Frame(main_frame, bg="#FFE5E5")
        content_frame.pack(fill="both", expand=True, pady=10)
        
        # Left side - Large image
        image_frame = tk.Frame(content_frame, bg="#FFE5E5", width=350, height=300)
        image_frame.pack(side="left", padx=(0, 15))
        image_frame.pack_propagate(False)
        
        try:
            # Load and display large image
            image_path = self.images_dir / f"{letter.lower()}.png"
            if image_path.exists():
                pil_image = Image.open(image_path)
                # Resize to fit the frame
                pil_image = pil_image.resize((300, 300), Image.Resampling.LANCZOS)
                large_image = ImageTk.PhotoImage(pil_image)
                
                image_label = tk.Label(
                    image_frame,
                    image=large_image,
                    bg="#FFE5E5"
                )
                image_label.image = large_image  # Keep reference
                image_label.pack(expand=True)
            else:
                # Show placeholder if image doesn't exist
                placeholder_label = tk.Label(
                    image_frame,
                    text=f"{emoji}",
                    font=("Arial", 150),
                    bg="#FFE5E5",
                    fg="#4A90E2"
                )
                placeholder_label.pack(expand=True)
        except Exception as e:
            # Show emoji if image loading fails
            placeholder_label = tk.Label(
                image_frame,
                text=f"{emoji}",
                font=("Arial", 150),
                bg="#FFE5E5",
                fg="#4A90E2"
            )
            placeholder_label.pack(expand=True)
        
        # Right side - Description and facts
        info_frame = tk.Frame(content_frame, bg="#FFE5E5")
        info_frame.pack(side="right", fill="both", expand=True)
        
        # Description section - more compact
        desc_label = tk.Label(
            info_frame,
            text=obj_info["description"],
            font=("Comic Sans MS", 14),
            bg="#FFE5E5",
            fg="#333333",
            wraplength=400,
            justify="left"
        )
        desc_label.pack(anchor="w", pady=(0, 15))
        
        # Fun facts section - more compact
        facts_title = tk.Label(
            info_frame,
            text="🎉 Fun Facts!",
            font=("Comic Sans MS", 18, "bold"),
            bg="#FFE5E5",
            fg="#FF6B9D"
        )
        facts_title.pack(anchor="w", pady=(0, 10))
        
        # Create a frame for facts with proper scrolling
        facts_container = tk.Frame(info_frame, bg="#FFE5E5")
        facts_container.pack(fill="both", expand=True)
        
        # Create canvas and scrollbar for facts
        canvas = tk.Canvas(facts_container, bg="#FFE5E5", height=200, highlightthickness=0)
        scrollbar = tk.Scrollbar(facts_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#FFE5E5")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add fun facts with better formatting
        for i, fact in enumerate(obj_info["fun_facts"]):
            fact_frame = tk.Frame(scrollable_frame, bg="#FFE5E5")
            fact_frame.pack(fill="x", pady=3, padx=5)
            
            fact_label = tk.Label(
                fact_frame,
                text=f"{i+1}. {fact}",
                font=("Comic Sans MS", 12),
                bg="#FFE5E5",
                fg="#333333",
                wraplength=380,
                justify="left"
            )
            fact_label.pack(anchor="w")
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bottom section - Close button
        bottom_frame = tk.Frame(main_frame, bg="#FFE5E5")
        bottom_frame.pack(fill="x", pady=(15, 0))
        
        close_button = tk.Button(
            bottom_frame,
            text="✖️ Close",
            command=detail_window.destroy,
            font=("Comic Sans MS", 14, "bold"),
            bg="#E74C3C",
            fg="WHITE",
            relief="groove",
            borderwidth=3,
            padx=15,
            pady=8,
            cursor="hand2"
        )
        close_button.pack()
        
        # Bind escape key to close window
        detail_window.bind("<Escape>", lambda e: detail_window.destroy())
        
        # Focus on the new window
        detail_window.focus_set()

def main():
    """Main function to run the application"""
    try:
        root = tk.Tk()
        app = AlphabetLearningApp(root)
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        root.mainloop()
    except Exception as e:
        pass  # Silently fail if application fails to start

if __name__ == "__main__":
    main() 