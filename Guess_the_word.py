import tkinter as tk
from tkinter import messagebox
import random

class GuessTheWordApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Угадай слово")
        
        self.questions, self.answers, _ = self.read_questions('questions.txt')  # Убираем описания
        self.used_indices = []
        
        self.question_label = tk.Label(root, text="", wraplength=300)
        self.question_label.pack(pady=10)
        
        self.answer_frame = tk.Frame(root)
        self.answer_frame.pack(pady=5)
        
        self.answer_entry = tk.Entry(root, state='readonly')
        self.answer_entry.pack(pady=5)
        
        self.delete_button = tk.Button(root, text="Удалить последнюю букву", command=self.delete_last_letter)
        self.delete_button.pack(pady=5)
        
        self.check_button = tk.Button(root, text="Проверить", command=self.check_answer)
        self.check_button.pack(pady=5)
        
        self.next_question_button = tk.Button(root, text="Следующий вопрос", command=self.next_question)
        self.next_question_button.pack(pady=5)
        
        self.quit_button = tk.Button(root, text="Выйти", command=root.quit)
        self.quit_button.pack(pady=5)
        
        self.current_chain = ''
        self.used_letters = {}

        self.next_question()

    def read_questions(self, filename):
        questions = []
        answers = []
        descriptions = []
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 3:
                    question, answer, description = parts
                    descriptions.append(description)
                else:
                    question, answer = parts
                    descriptions.append("")  # Добавляем пустое описание
                questions.append(question)
                answers.append(answer)
        return questions, answers, descriptions

    def shuffle_word(self, word):
        word_list = list(word)
        random.shuffle(word_list)
        return ''.join(word_list)

    def next_question(self):
        self.answer_frame.destroy()
        self.answer_frame = tk.Frame(self.root)
        self.answer_frame.pack(pady=5)
        
        if self.questions:
            index = random.choice([i for i in range(len(self.questions)) if i not in self.used_indices])
            self.used_indices.append(index)
            self.current_question = self.questions[index]
            self.current_answer = self.answers[index]
            self.shuffled_word = self.shuffle_word(self.current_answer)
            self.question_label.config(text=self.current_question)
            
            self.word_labels = []
            self.used_letters = {letter: 0 for letter in self.shuffled_word}
            for letter in self.shuffled_word:
                label = tk.Label(self.answer_frame, text=letter, padx=10, pady=5, relief=tk.RAISED, borderwidth=1)
                label.bind('<Button-1>', self.move_letter)
                label.pack(side=tk.LEFT)
                self.word_labels.append(label)
        else:
            messagebox.showinfo("Игра окончена", "Все вопросы закончились!")
            self.root.quit()

    def move_letter(self, event):
        letter_label = event.widget
        letter = letter_label.cget("text")
        if self.used_letters[letter] < self.shuffled_word.count(letter):
            self.used_letters[letter] += 1
            self.current_chain += letter
            letter_label.pack_forget()  # Убираем букву из отображения
            self.update_answer_entry()

    def update_answer_entry(self):
        self.answer_entry.config(state='normal')
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.insert(0, self.current_chain)
        self.answer_entry.config(state='readonly')

    def delete_last_letter(self):
        if self.current_chain:
            last_letter = self.current_chain[-1]
            self.used_letters[last_letter] -= 1
            self.current_chain = self.current_chain[:-1]
            for label in self.word_labels:
                if label.cget("text") == last_letter:
                    label.pack(side=tk.LEFT)  # Возвращаем букву в отображение
            self.update_answer_entry()

    def check_answer(self):
        if all(self.used_letters.values()):
            user_answer = self.answer_entry.get().strip().lower()
            if user_answer == self.current_answer.lower():
                messagebox.showinfo("Правильно", "Вы угадали слово!")
                self.next_question()
            else:
                messagebox.showerror("Неправильно", f"Неправильный ответ. Правильный ответ: {self.current_answer}")
            self.current_chain = ''
            self.update_answer_entry()
        else:
            messagebox.showwarning("Ошибка", "Используйте все доступные буквы!")

root = tk.Tk()
app = GuessTheWordApp(root)
root.mainloop()
