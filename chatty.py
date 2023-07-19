import openai
import speech_recognition as sr
from tkinter.constants import DISABLED, NORMAL
import tkinter as tk

# Set up OpenAI API credentials
openai.api_key = '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'

def ask_openai(question):
    model_engine = "text-davinci-003"
    prompt = f"Q: {question}\nA:"
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.,
    )

    message = completions.choices[0].text.strip()
    return message

# Function to recognize speech using microphone
def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Sorry, I could not understand you, try asking something eles!"
    except sr.RequestError:
        return "Sorry, my speech recognition service is currently down come back later when I may be back working "

class ChatbotGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("JarvisGPT")
        self.window.geometry("400x600")
        self.window.configure(bg='white')

        self.scroll_frame = tk.Frame(self.window)
        self.scroll_frame.pack(side="top", fill="both", expand=True)

        self.chat_history = tk.Text(self.scroll_frame, wrap="word", state="disabled")
        self.chat_history.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.scroll_frame, orient="vertical", command=self.chat_history.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.chat_history.configure(yscrollcommand=self.scrollbar.set, bg= "#00ff8f")

        self.question_entry = tk.Entry(self.window, width=200, font=("Garamond", 16), bg= "#00ff8f")
        self.question_entry.pack(pady=10)
        self.window.bind('<Return>', self.ask_question)

        self.ask_button = tk.Button(self.window, text="Ask", width=200, command=self.ask_question, font=("Garamond", 16))
        self.ask_button.pack(pady=10)

        self.clear_button = tk.Button(self.window, text="Clear", width=200, command=self.clear_all, font=("Garamond", 16))
        self.clear_button.pack(pady=10)

        self.listen_button = tk.Button(self.window, text="Text to Speech only for Nerd.",width=200, command=self.listen_question, font=("Garamond", 16))
        self.listen_button.pack(pady=10)

        self.window.mainloop()
        


    def clear_all(self):
        self.chat_history.configure(state="normal")
        self.chat_history.delete("1.0", tk.END)
        self.chat_history.configure(state="disabled")

    def ask_question(self, event):
        question = self.question_entry.get().strip()
        if question != "":
            response = ask_openai(question)
            self.update_chat_history(question, response)

    def listen_question(self):
        question = recognize_speech()
        self.question_entry.delete(0, tk.END)
        self.question_entry.insert(0, question)
        response = ask_openai(question)
        self.update_chat_history(question, response)

    def update_chat_history(self, question, response):
        self.chat_history.configure(state="normal")
        if self.chat_history.index('end') != None:
            self.chat_history.insert('end', "You: " + question + "\n", 'bold')
            self.chat_history.insert('end', "Jarvis: " + response + "\n\n", 'bold')
            self.chat_history.tag_configure('bold', font=("Garamond", 16, 'bold'))
            self.chat_history.configure(state="disabled")
            self.chat_history.yview('end')

if __name__ == "__main__":
    gui = ChatbotGUI()