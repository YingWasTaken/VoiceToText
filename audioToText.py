import tkinter as tk
import speech_recognition as sr
import threading
import pyperclip

class VoiceToTextApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reconocimiento de voz en tiempo real")

        self.text_area = tk.Text(root, height=10, width=50)
        self.text_area.pack(pady=10)

        self.button = tk.Button(root, text="Activar", bg="green", fg="white", 
                                font=("Arial", 14), height=2, width=20, command=self.toggle_listening)
        self.button.pack(pady=5)

        self.copy_button = tk.Button(root, text="Copiar Texto", bg="blue", fg="white",
                                     font=("Arial", 12), height=1, width=15, command=self.copy_to_clipboard)
        self.copy_button.pack(pady=5)

        self.clear_button = tk.Button(root, text="Limpiar Texto", bg="orange", fg="white",
                              font=("Arial", 12), height=1, width=15, command=self.clear_text)
        self.clear_button.pack(pady=5)

        self.save_button = tk.Button(root, text="Guardar Texto", bg="purple", fg="white",
                             font=("Arial", 12), height=1, width=15, command=self.save_text)
        self.save_button.pack(pady=5)

        # selector idioma
        self.language_var = tk.StringVar(value="es-ES")  # Valor por defecto: Español
        languages = {"Español": "es-ES", "Inglés": "en-US", "Francés": "fr-FR", "Alemán": "de-DE", "Italiano": "it-IT"}
        self.language_menu = tk.OptionMenu(root, self.language_var, *languages.keys())
        self.language_menu.pack(pady=5)


        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.listening = False
        self.languages = languages  

    def toggle_listening(self):
        if self.listening:
            self.listening = False
            self.button.config(text="Activar", bg="green")
        else:
            self.listening = True
            self.button.config(text="Desactivar", bg="red")
            threading.Thread(target=self.listen, daemon=True).start()

    def listen(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)  # Ajusta el ruido ambiente
            while self.listening:
                try:
                    print("Escuchando...")
                    audio = self.recognizer.listen(source, timeout=None, phrase_time_limit=5)  
                    selected_language = self.languages[self.language_var.get()]  # Obtener el idioma seleccionado
                    text = self.recognizer.recognize_google(audio, language=selected_language)
                    self.text_area.insert(tk.END, text + "\n")
                except sr.UnknownValueError:
                    self.text_area.insert(tk.END, "[No se entendió el audio]\n")
                except sr.RequestError:
                    self.text_area.insert(tk.END, "[Error con el servicio de reconocimiento]\n")
                except sr.WaitTimeoutError:
                    print("[Tiempo de espera agotado, esperando otra frase...]")

    def copy_to_clipboard(self):
        text = self.text_area.get("1.0", tk.END).strip() 
        if text:
            pyperclip.copy(text)
            print("Texto copiado al portapapeles") 

    def clear_text(self):
        self.text_area.delete("1.0", tk.END)

    def save_text(self):
        text = self.text_area.get("1.0", tk.END).strip()
        if text:
            with open("transcripcion.txt", "w", encoding="utf-8") as file:
                file.write(text)
            self.copy_label.config(text="Texto guardado en transcripcion.txt", fg="blue")
            self.root.after(2000, lambda: self.copy_label.config(text=""))


if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceToTextApp(root)
    root.mainloop()
