import json
from pathlib import Path


def create_sample_questions():
    """Create sample questions for testing"""
    categories = {
        "mathematical_numerical": [
            {"question": "What is the next number of the sequence 11, 14, 19, 26, ____?", "correct_answer": "35"},
            {"question": "Which number logically follows the series 2, 7, 12, ___?", "correct_answer": "17"},
            {"question": "What is the missing number in the sequence 20, 17, 22, ____, 24?", "correct_answer": "19"},
            {"question": "Which number is the next numbers in this pattern 9, 18, 36, ___, ?", "correct_answer": "72"},
            {"question": "Which of these numbers is not a prime number? 163, 199, 100, 67", "correct_answer": "100"},
            {"question": "If 4+(x) is 11 and 6+(x) is 13, what does x equal to?", "correct_answer": "7"},
            {"question": "What is the place value of the 7 in the number 567986?", "correct_answer": "7,000"},
            {"question": "Which fraction is the biggest: ⅕, 3/5, ½, 4/7?", "correct_answer": "3/5"},
            {"question": "What is the missing number in the series 1, 2, 4, __, 8, 10?", "correct_answer": "6"},
            {"question": "What is the missing number in the series 200, 190, ___, 170, 160?", "correct_answer": "180"},
            {"question": "What is the missing number in '?' place, 3, 2, 9, ?, 15, 14, 21", "correct_answer": "8"},
            {"question": "What is the odd number: 2, 202, 385, 150, 148?", "correct_answer": "385"},
            {"question": "Solve -30 + (-10X) = 0", "correct_answer": "-3"},
            {"question": "What is 1.62 / 3?", "correct_answer": "0.54"},
            {"question": "What is the sum of 140+96+25?", "correct_answer": "261"},
            {"question": "10+(80/2) Equal to?", "correct_answer": "50"},
            {"question": "The product of 315x0x47x18 is?", "correct_answer": "0"},
            {"question": "What is 150% of 4751?", "correct_answer": "7,126.5"},
            {"question": "If x-3=0 then x=?", "correct_answer": "3"},
            {"question": "Which of the following is equal to '21/30' \n '0.71', '0.6', '0.7', '0.3' ?", "correct_answer": "0.7"},
        ],
        "mathematical_text": [
            {"question": "A train traveling at 150 km/h takes 25 seconds to pass a pole. What is the length of the train in meters?", "correct_answer": "1042 m"},
            {"question": "Two workers can complete a job in 8 hours when working together. Worker A alone would take 12 hours to complete the job. How long would Worker B alone take to complete it?", "correct_answer": "24 h"},
            {"question": "A projectile is launched with an initial velocity of 120 m/s at an angle of 30° to the horizontal. What is the maximum height it reaches?", "correct_answer": "183.67 m"},
            {"question": "A cylindrical tank with a diameter of 15 meters and a height of 30 meters is filled with water. If water flows out at a rate of 9 cubic meters per minute, how long will it take to empty the tank?", "correct_answer": "590 minutes"},
            {"question": "A tank with a leak can be filled in 11 hours. When the tank is being filled, the leak reduces the fill rate by 15 liters per hour. If the tank is filled in 10 hours with the leak, what is its capacity in liters?", "correct_answer": "165 liters"},
            {"question": "A company sells 120 units of a product at Rs.6000 each. For every Rs.100 increase in price, they sell 6 fewer units. At what price will the company maximize revenue?", "correct_answer": "Rs.6200"},
            {"question": "A rectangle has a diagonal of 15 cm and one side of 7 cm. What is the length of the other side?", "correct_answer": "13.27 cm"},
            {"question": "A bat and a ball together cost Rs.1200. The bat costs Rs.500 more than the ball. How much does the ball cost?","correct_answer": "Rs.350 (ball), Rs.850 (bat)"},
            {"question": "The sum of the squares of three consecutive integers is 365. What are the integers?", "correct_answer": "10, 11, 12"},
            {"question": "A car travels 50 km at 80 km/h and then another 30 km at 40 km/h. What is the car's average speed for the entire journey?", "correct_answer": "58.18 km/h"},
            {"question": "Two people are standing 200 meters apart. They start walking towards each other, one at 5 m/s and the other at 3 m/s. How many seconds will it take for them to meet?", "correct_answer": "25 seconds"},
            {"question": "A factory produces 400 items per hour. If 3% of the items are defective, how many defective items are produced in 8 hours?", "correct_answer": "96 items"},
            {"question": "A farmer wants to fence a rectangular field with a perimeter of 130 meters. If the length is twice the width, what are the dimensions of the field?","correct_answer": "43.33 m (length), 21.67 m (width)"},
            {"question": "A sum of money doubles itself in 7 years under compound interest. How many years will it take to quadruple?","correct_answer": "14 years"},
            {"question": "A ladder leans against a wall, reaching a height of 10 meters. The base of the ladder is 7 meters away from the wall. What is the length of the ladder?","correct_answer": "12.21 m"},
            {"question": "A tank is 70% full and contains 400 liters of water. How many liters can the tank hold when full?","correct_answer": "571.43 L"},
            {"question": "A pool can be filled in 7 hours using Pipe A and in 10 hours using Pipe B. If both pipes are used together, how long will it take to fill the pool?","correct_answer": "4.12 h"},
            {"question": "A metal rod expands by 0.02 cm for every 15°C rise in temperature. If the rod is 2 meters long, how much will it expand when the temperature rises from 15°C to 85°C?","correct_answer": "0.93 cm"},
            {"question": "A boat travels 30 km downstream in 3 hours and takes 5 hours to travel the same distance upstream. What is the speed of the boat in still water?","correct_answer": "24 km/h"},
            {"question": "A cyclist covers a distance of 35 km in 4 hours. If he increases his speed by 8 km/h, how long will it take him to cover the same distance?","correct_answer": "2.09 hours"}
            
        ],
        "true_false": [
            {"question": "The capital of Sri Lanka is Colombo.","correct_answer": "False"},
            {"question": "2 multiplied by 4 is equal to 2 cubed.","correct_answer": "True"},
            {"question": "Water boils at 100°C at standard atmospheric pressure.","correct_answer": "True"},
            {"question": "The Sun revolves around the Earth.","correct_answer": "False"},
            {"question": "Nimal's father's mother is Nimal's grandmother.","correct_answer": "True"},
            {"question": "Mount Everest is the tallest mountain on Earth.","correct_answer": "True"},
            {"question": "The world's first female Prime Minister was born in India.","correct_answer": "False"},
            {"question": "The speed of light is faster than the speed of sound.","correct_answer": "True"},
            {"question": "The Moon is a planet.","correct_answer": "False"},
            {"question": "Facebook was founded by Mark Zuckerberg.","correct_answer": "True"},
            {"question": "A year on Jupiter is longer than a year on Earth.","correct_answer": "True"},
            {"question": "Every month has 30 days.","correct_answer": "False"},
            {"question": "January is the last month in every country.","correct_answer": "False"},
            {"question": "The Great Wall of China is visible from space.","correct_answer": "False"},
            {"question": "The first citizen of Sri Lanka is considered to be the President.","correct_answer": "True"},
            {"question": "The Moon has its own light source.","correct_answer": "False"},
            {"question": "The chemical symbol for gold is Ag.","correct_answer": "False"},
            {"question": "Sharks are not mammals.","correct_answer": "True"},
            {"question": "The Eiffel Tower was originally intended to be a temporary structure.","correct_answer": "True"},
            {"question": "My father's son's son is a grandson to my mother.","correct_answer": "True"}
        ],
        "logical": [
            {"question": "My father only has one child. So who is my father's son's older brother?","correct_answer": "No one, you are your father's only child."},
            {"question": "All apples are fruits. All fruits grow on trees. Therefore, all apples grow on trees. True or False?","correct_answer": "True"},
            {"question": "If a train leaves City A at 3 PM traveling at 60 km/h, and another train leaves City B at the same time traveling at 80 km/h towards City A, which train will reach the meeting point first?","correct_answer": "Cannot give a correct answer because distance is not given."},
            {"question": "If there are 5 birds on a tree and a hunter shoots one, how many are left on the tree?","correct_answer": "None, as the rest would fly away due to the sound."},
            {"question": "If Saman has twice as many mangoes as Sitha, and Sitha has 2 apples and 4 mangoes, how many mangoes does Saman have?","correct_answer": "8 mangoes"},
            {"question": "A farmer has 17 sheep. All but 9 run away. How many sheep does the farmer have left?","correct_answer": "9 sheep remain."},
            {"question": "If a red house is made of red bricks, and a blue house is made of blue bricks, what is a greenhouse made of?","correct_answer": "Glass."},
            {"question": "Two fathers and two sons go fishing. They catch three fish, and each person has one fish. How is this possible?","correct_answer": "They are a grandfather, a father, and a son."},
            {"question": "A man has Rs.100 and he wants to eat only one apple. The apple costs Rs.50. How many apples does the man buy?","correct_answer": "One apple, because he only wants one apple."},
            {"question": "You are in a race and pass the person in second place. What place are you in now?","correct_answer": "Second place."},
            {"question": "You are in a race, and the person in second place passes the person in front. You end up in second place. What position were you in before?","correct_answer": "First place."},
            {"question": "If 5 cats can catch 5 mice in 5 minutes, how many cats are needed to catch 100 mice in 100 minutes?","correct_answer": "5 cats, the rate of work remains the same."},
            {"question": "I am a number. Multiply me by 4, then subtract 6, and you get 18. What number am I?","correct_answer": "6; 4 × 6 − 6 = 18."},
            {"question": "A bat and a ball together cost Rs.1200. The bat costs Rs.500 more than the ball. How much does the ball cost?","correct_answer": "Rs.350, the bat costs Rs.850."},
            {"question": "A father is 36 years old, and his son is 6 years old. In how many years will the father be five times the age of his son?","correct_answer": "6 years, the father will be 42, and the son will be 12."},
            {"question": "What comes next in the sequence: 1, 1, 2, 3, 5, 8, 13?","correct_answer": "21; it’s the Fibonacci sequence."},
            {"question": "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?","correct_answer": "An echo."},
            {"question": "You are in a room with three light switches. Each switch controls one of three light bulbs in another room. You can only enter the other room once. How do you determine which switch controls which bulb?","correct_answer": "Turn one switch on for a few minutes, turn it off, and turn another on. Go to the room: the lit bulb matches the second switch, the warm bulb matches the first, and the unlit/cool bulb matches the third."},
            {"question": "Tom is twice as old as his sister. Five years ago, he was three times as old. How old is Tom now?","correct_answer": "Tom is 10 years old, and his sister is 5."},
            {"question": "What comes next in the sequence: 4, 4, 2, 2, 1, 1, 14, 4, 4, 2?","correct_answer": "2"}
        ],
        "general_knowledge": [
            {"question": "In which country is the city of Venice located?","correct_answer": "Italy"},
            {"question": "How many muscles control the movement of the human eye?","correct_answer": "6"},
            {"question": "In which country was the Titanic built?","correct_answer": "United Kingdom"},
            {"question": "What is the capital of Nigeria?","correct_answer": "Abuja"},
            {"question": "What is the 29th state of India?","correct_answer": "Telangana"},
            {"question": "Which country is the largest producer of coffee?","correct_answer": "Brazil"},
            {"question": "How many keys are in a piano?","correct_answer": "88"},
            {"question": "Which continent has the most countries?","correct_answer": "Africa"},
            {"question": "What city is known as the eternal city?","correct_answer": "Rome"},
            {"question": "Which country has the most islands?","correct_answer": "Sweden"},
            {"question": "What is the human body part that has fully grown since birth?","correct_answer": "Eyes"},
            {"question": "What is the most widely spoken language in the world by the number of native speakers?","correct_answer": "Mandarin Chinese"},
            {"question": "What is the world's fastest bird?","correct_answer": "Peregrine falcon"},
            {"question": "Which is the only mammal that lays eggs?","correct_answer": "Platypus"},
            {"question": "What is always associated with a dolmen?","correct_answer": "Stone"},
            {"question": "What is the name given to a group of horses?","correct_answer": "Harras"},
            {"question": "What is the smallest bone in the human body?","correct_answer": "Stapes"},
            {"question": "The element with the atomic number 79 is _________, which is often used in _________.","correct_answer": "Gold, jewelry"},
            {"question": "The capital of _________ is the oldest continuously inhabited city in the world.","correct_answer": "Damascus"},
            {"question": "The process by which plants convert _________ and _________ into chemical energy is called _________.","correct_answer": "Sunlight, carbon dioxide, photosynthesis"}
        ]

    }

    # Create questions directory
    questions_dir = Path("questions")
    questions_dir.mkdir(exist_ok=True)
    
    # Save each category to a JSON file
    for category, questions in categories.items():
        with open(questions_dir / f"{category}.json", "w") as f:
            json.dump(questions, f, indent=2)