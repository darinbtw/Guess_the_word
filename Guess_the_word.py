import openai
import random

# Установка ключа API
openai.api_key = 'https://api.openai.com/v1/completions'

# Функция для генерации слова с помощью OpenAI API
def generate_word():
    prompt = "Сгенерируйте слово для игры про угадывание слов на русском языке с описанием этого загаданного слова:"
    response = openai.Completion.create(
        engine="text-davinci-003",  # Можно использовать другие модели, если нужно
        prompt=prompt,
        temperature=0.7,  # Регулирует разнообразие ответа
        max_tokens=50,  # Максимальное количество токенов в ответе
        n=1,  # Количество ответов, которые нужно сгенерировать
        stop=None,  # Условие остановки генерации
        timeout=None,  # Таймаут запроса
    )
    return response.choices[0].text.strip()

# Функция для перемешивания букв в слове
def shuffle_word(word):
    word_list = list(word)
    random.shuffle(word_list)
    return ''.join(word_list)

# Функция для проверки правильности ответа
def check_guess(actual_word, guessed_word):
    return actual_word == guessed_word

# Главная функция игры
def play_game():
    print("Добро пожаловать в игру 'Угадай слово'!")
    print("Я сгенерирую слово, а вы должны будете его угадать.")
    print("Вот ваше первое слово:")
    generated_word = generate_word()
    shuffled_word = shuffle_word(generated_word)
    print("Загаданное слово:", shuffled_word)
    guess = input("Ваш ответ: ").strip().lower()
    if check_guess(generated_word, guess):
        print("Правильно! Вы угадали слово.")
    else:
        print("Неправильно. Правильный ответ:", generated_word)

# Запуск игры
play_game()
