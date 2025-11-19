import random

QUOTES = [
    # Swami Vivekananda (15)
    "Arise, awake, and stop not till the goal is reached. - Swami Vivekananda",
    "Take risks in your life. If you win, you can lead; if you lose, you can guide. - Swami Vivekananda",
    "Talk to yourself once in a day, otherwise you may miss meeting an excellent person in this world. - Swami Vivekananda",
    "You cannot believe in God until you believe in yourself. - Swami Vivekananda",
    "In a conflict between the heart and the brain, follow your heart. - Swami Vivekananda",
    "Strength is life, weakness is death. - Swami Vivekananda",
    "Stand up, be bold, be strong. Take the whole responsibility on your own shoulders. - Swami Vivekananda",
    "The world is the great gymnasium where we come to make ourselves strong. - Swami Vivekananda",
    "All power is within you; you can do anything and everything. - Swami Vivekananda",
    "Be a hero. Always say, 'I have no fear.' - Swami Vivekananda",
    "Dare to be free, dare to go as far as your thought leads. - Swami Vivekananda",
    "The greatest religion is to be true to your own nature. - Swami Vivekananda",
    "Nothing can withstand the energy of the human soul. - Swami Vivekananda",
    "The fire that warms us can also consume us; it is all in the intensity of the flame. - Swami Vivekananda",
    "Talk to yourself, it helps you find your own truth. - Swami Vivekananda",

    # Albert Einstein (5)
    "Life is like riding a bicycle. To keep your balance you must keep moving. - Albert Einstein",
    "Imagination is more important than knowledge. - Albert Einstein",
    "Try not to become a man of success, but rather try to become a man of value. - Albert Einstein",
    "In the middle of difficulty lies opportunity. - Albert Einstein",
    "Logic will get you from A to B. Imagination will take you everywhere. - Albert Einstein",

    # Mahatma Gandhi (5)
    "Be the change that you wish to see in the world. - Mahatma Gandhi",
    "The best way to find yourself is to lose yourself in the service of others. - Mahatma Gandhi",
    "Strength does not come from physical capacity. It comes from an indomitable will. - Mahatma Gandhi",
    "Live as if you were to die tomorrow. Learn as if you were to live forever. - Mahatma Gandhi",
    "Happiness is when what you think, what you say, and what you do are in harmony. - Mahatma Gandhi",

    # Steve Jobs (5)
    "The people who are crazy enough to think they can change the world are the ones who do. - Steve Jobs",
    "Stay hungry, stay foolish. - Steve Jobs",
    "Your work is going to fill a large part of your life, and the only way to be truly satisfied is to do what you believe is great work. - Steve Jobs",
    "Innovation distinguishes between a leader and a follower. - Steve Jobs",
    "Don't let the noise of others' opinions drown out your own inner voice. - Steve Jobs",

    # Winston Churchill (5)
    "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill",
    "Continuous effort—not strength or intelligence—is the key to unlocking our potential. - Winston Churchill",
    "To improve is to change; to be perfect is to change often. - Winston Churchill",
    "Courage is rightly esteemed the first of human qualities. - Winston Churchill",
    "Attitude is a little thing that makes a big difference. - Winston Churchill",

    # Theodore Roosevelt (5)
    "Do what you can, with what you have, where you are. - Theodore Roosevelt",
    "Believe you can and you're halfway there. - Theodore Roosevelt",
    "Far and away the best prize that life has to offer is the chance to work hard at work worth doing. - Theodore Roosevelt",
    "Keep your eyes on the stars, and your feet on the ground. - Theodore Roosevelt",
    "It is hard to fail, but it is worse never to have tried to succeed. - Theodore Roosevelt",

    # Confucius (5)
    "It does not matter how slowly you go as long as you do not stop. - Confucius",
    "Our greatest glory is not in never falling, but in rising every time we fall. - Confucius",
    "Choose a job you love, and you will never have to work a day in your life. - Confucius",
    "Real knowledge is to know the extent of one’s ignorance. - Confucius",
    "When it is obvious that the goals cannot be reached, don't adjust the goals, adjust the action steps. - Confucius",
]

def get_random_quote():
    """Return a random quote from the list."""
    return random.choice(QUOTES)
