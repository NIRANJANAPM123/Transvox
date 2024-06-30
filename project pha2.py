import tkinter as tk
from tkinter import Text, Scrollbar
from googletrans import Translator
from gtts import gTTS
import os

class BrailleTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TRANSVOX-Braille Translator")
        self.translator = Translator()
        
        self.setup_style()
        #self.create_splash_screen()
        # Braille keyboard
        self.create_braille_keyboard()

        # Braille input area
        self.create_braille_input_area()

        # Translation result area
        self.create_translation_result_area()
        self.center_window()
        
    def setup_style(self):
        self.root.configure(bg='#f0f0f0')
        self.default_font=("Arial",12)
        self.heading_font=("Arial",16,"bold")
    '''def create_splash_screen(self):
        splash_frame=tk.Frame(self.root,bg='#ffffff')
        splash_frame.place(relx=0.5,rely=0.5,anchor='center')
        splash_label=tk.Label(splash_frame,text="TRANSVOX",font=("helvetica",50),bg="blue")
        splash_label.pack()
        self.root.after(10000,splash_frame.destroy)'''
        
    def create_braille_keyboard(self):
        braille_keys = [
        ('a','⠁'), ('b','⠃'), ('c','⠉'), ('d','⠙'), ('e','⠑'),
        ('f','⠋'), ('g','⠛'), ('h','⠓'), ('i','⠊'), ('j','⠚'),
        ('k','⠅'), ('l','⠇'), ('m','⠍'), ('n','⠝'), ('o','⠕'),
        ('p','⠏'), ('q','⠟'), ('r','⠗'), ('s','⠎'), ('t','⠞'),
        ('u','⠥'), ('v','⠧'), ('w','⠺'), ('x','⠭'), ('y','⠽'),
        ('z','⠵'), ('space', ' ')
         ]

        keyboard_frame = tk.Frame(self.root,bg='#ffffff')
        keyboard_frame.place(relx=0.5,rely=0.25,anchor='center')
        tranvox_label=tk.Label(self.root,text='TRANSVOX-Braille Translator',font=("helvetica",30,"bold"))

        tranvox_label.place(relx=0.5,rely=0.06,anchor='center')
        '''self.title_label=tk.Label(self.root,text='',font=("helvetica",30))
        self.title_label.place(relx=0.5,rely=0.06,anchor='center')
        self.animate_title("TRANSVOX","BRAILLE TRANSLATOR")'''
        #keyboard_frame.grid(row=0, column=0, padx=10, pady=10)
        #window_width=self.root.winfo_reqwidth()
        #window_height=self.root.winfo_reqheight()
        #x_position=(window_width-keyboard_frame.winfo_reqwidth())//2
        #y_position=(window_height-keyboard_frame.winfo_reqheight())//2
        #self.root.geometry("+{}+{}".format(x_position,y_position))
        
        

        for i, (braille, alphabet) in enumerate(braille_keys):
            btn = tk.Button(keyboard_frame, text=braille + '\n' + alphabet, width=5, height=3,font=("Arial",10,"bold"),bg='#bfbfbf',fg='#333333', command=lambda a=alphabet: self.insert_braille_char(a))
            btn.grid(row=i // 10, column=i % 10, padx=2, pady=2)
    def create_braille_input_area(self):
        input_frame = tk.Frame(self.root,bg='#ffffff',bd=2,relief='groove')
        input_frame.place(relx=0.5,rely=0.55,anchor="center")
        #input_frame.grid(row=1, column=0, padx=10, pady=10,sticky='nsew',columnspan=10)

        input_label = tk.Label(input_frame, text="Braille Input:",font=self.heading_font,bg='#ffffff')
        input_label.grid(row=0, column=0, sticky='w')

        self.braille_text = Text(input_frame, height=5, width=60, wrap='word',bd=2,relief='sunken')
        self.braille_text.grid(row=1, column=0, pady=5,sticky='nsew')

        translate_button = tk.Button(input_frame, text="Translate",font=self.default_font,bg='#4CAF90',fg="white", command=self.translate_and_speak)
        translate_button.grid(row=2, column=0, pady=5)

        clear_button=tk.Button(input_frame,text="Clear",font=self.default_font,bg='#4CAF90',fg="white",command=self.clear_braille_input)
        clear_button.grid(row=3,column=0,pady=6)

    def clear_braille_input(self):
        self.braille_text.delete('1.0',tk.END)

    def create_translation_result_area(self):
        result_frame = tk.Frame(self.root,bg='#ffffff',bd=2,relief='groove')
        #result_frame.grid(row=2, column=0, padx=10, pady=10,sticky='nsew')
        result_frame.place(relx=0.5,rely=0.85,anchor='center')

        result_label = tk.Label(result_frame, text="Translation Result:",font=self.heading_font,bg='#ffffff')
        result_label.grid(row=0, column=0, sticky='w')
        

        self.result_text = Text(result_frame, height=8, width=60, wrap='word', state='disabled',bd=2,relief='sunken')
        self.result_text.grid(row=1, column=0, pady=5,sticky='nsew')

        

    def insert_braille_char(self, char):
        self.braille_text.insert(tk.END, char)

    def translate_and_speak(self):
        braille_text = self.braille_text.get("1.0", tk.END).strip()
        english_text = self.braille_to_english(braille_text)
        self.result_text.config(state='normal')
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, english_text)
        self.result_text.config(state='disabled')

        # Translate and speak
        translate_and_speak(english_text)

    def braille_to_english(self, braille_text):
         braille_alphabet = {
        'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑',
        'f': '⠋', 'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚',
        'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝', 'o': '⠕',
        'p': '⠏', 'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞',
        'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭', 'y': '⠽',
        'z': '⠵', ' ': ' '
        }
    
    # Convert Braille to English
         english_text = ''
         current_word = ''
         for char in braille_text:
            if char in braille_alphabet.values():
                for key, value in braille_alphabet.items():
                    if char == value:
                        current_word += key
                        break
            elif char == ' ':  # Space character
                if current_word:
                     english_text += current_word + ' '
                     current_word = ''
            elif char == '⠼':  # Number indicator
                 continue  # Skip number indicator
            elif char == '\n':  # Newline character
                 if current_word: 
                    english_text += current_word + '\n'
                    current_word = ''
            else:
            # If an unsupported character is encountered, ignore it
                continue
    
         if current_word:
            english_text += current_word
    
         return english_text

        # Your braille_to_english function implementation here
        # ...
    def center_window(self):
         screen_width=self.root.winfo_screenwidth()
         screen_height=self.root.winfo_screenheight()
         window_width=600
         window_height=400
         x_coordinate=(screen_width-window_width)//2
         y_coordinate=(screen_height-window_height)//2
         self.root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
    

def translate_and_speak(text, target_language='ml'):
    translator = Translator()

    # Translate the text to Malayalam
    translated_text = translator.translate(text, dest=target_language).text

    # Convert the translated text to speech
    speech = gTTS(translated_text, lang=target_language)

    # Save the speech to a file
    speech.save("translated_speech.mp3")

    # Play the saved speech
    os.system("start translated_speech.mp3")


if __name__ == "__main__":
    root = tk.Tk()
    app = BrailleTranslatorApp(root)
    #root.configure(bg="grey")
   
    root.mainloop()
