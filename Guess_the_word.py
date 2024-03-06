import tkinter as tk
from tkinter import messagebox
import random

class GuessTheWordApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Угадай слово")
        
        self.questions, self.answers, self.descriptions = self.read_questions('questions.txt')
        self.used_indices = []
        
        self.question_label = tk.Label(root, text="", wraplength=300)
        self.question_label.pack(pady=10)
        
        self.answer_entry = tk.Entry(root)
        self.answer_entry.pack(pady=5)
        
        self.check_button = tk.Button(root, text="Проверить", command=self.check_answer)
        self.check_button.pack(pady=5)
        
        self.next_question_button = tk.Button(root, text="Следующий вопрос", command=self.next_question)
        self.next_question_button.pack(pady=5)
        
        self.quit_button = tk.Button(root, text="Выйти", command=root.quit)
        self.quit_button.pack(pady=5)
        
        self.next_question()

    def read_questions(self, filename):
        questions = []
        answers = []
        descriptions = []
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                question, answer, description = line.strip().split('|')
                questions.append(question)
                answers.append(answer)
                descriptions.append(description)
        return questions, answers, descriptions

    def shuffle_word(self, word):
        word_list = list(word)
        random.shuffle(word_list)
        return ''.join(word_list)

    def next_question(self):
        self.answer_entry.delete(0, tk.END)
        if self.questions:
            index = random.choice([i for i in range(len(self.questions)) if i not in self.used_indices])
            self.used_indices.append(index)
            self.current_question = self.questions[index]
            self.current_answer = self.answers[index]
            self.current_description = self.descriptions[index]
            shuffled_word = self.shuffle_word(self.current_answer)
            self.question_label.config(text=self.current_description + "\n\n" + shuffled_word)
        else:
            messagebox.showinfo("Игра окончена", "Все вопросы закончились!")
            self.root.quit()

    def check_answer(self):
        guess = self.answer_entry.get().strip().lower()
        if guess == self.current_answer.lower():
            messagebox.showinfo("Правильно", "Вы угадали слово!")
            self.next_question()
        else:
            messagebox.showerror("Неправильно", f"Неправильный ответ. Правильный ответ: {self.current_answer}")

root = tk.Tk()
app = GuessTheWordApp(root)
root.mainloop()
