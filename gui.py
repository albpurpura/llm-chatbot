import tkinter as tk
from tkinter import Scrollbar, Text, Button, ttk, PhotoImage
import argparse
import atexit
import yaml
from rich.console import Console

from language_model import LLM
from utils import suppress_stdout_stderr, verify_download_model

THEME_COLOR = "#02537f"


def chat(input_text):
    # Replace this with your chatbot logic
    gen = llm.reply(input_text)
    return gen


# Function to update the chat history with the response token by token
def update_chat_history(input_text):
    chat_history_text.config(state=tk.NORMAL)  # Allow editing the text widget
    chat_history_len = len(chat_history_text.get("1.0", tk.END))

    if chat_history_len > 1:
        chat_history_text.insert(tk.END, "\nYou: " + input_text.strip())
    else:
        chat_history_text.insert(tk.END, "You: " + input_text.strip())
    chat_history_text.insert(tk.END, "\nChatbot: ")
    chat_history_text.config(state=tk.DISABLED)  # Disable text editing
    root.update()
    for token in chat(input_text):
        chat_history_text.config(state=tk.NORMAL)  # Allow editing the text
        chat_history_text.insert(tk.END, token)
        chat_history_text.see(tk.END)  # Scroll to the end of the text widget
        chat_history_text.config(state=tk.DISABLED)  # Disable text editing
        root.update()
    chat_history_text.config(state=tk.DISABLED)


def handle_keypress(event):
    # Detect Shift + Enter to add a new line
    if (
        event.keysym == "Return" and event.state == 1
    ):  # Shift key has state 1 when pressed
        user_input_text.insert(tk.END, "")


# Function to handle sending a message
def send_message(*args):
    user_input = user_input_text.get(
        "1.0", "end-1c"
    )  # Get user input from the Text widget
    if user_input.strip():
        user_input_text.delete("0.0", tk.END)  # Clear the user input field
        update_chat_history(user_input)


def close_window():
    root.quit()


# Create the main application window
root = tk.Tk()
root.title("Chatbot")
img = PhotoImage(file="icon.ppm")
root.iconphoto(False, img)

# Create a style for themed widgets (using the 'clam' theme)
style = ttk.Style(root)
style.theme_use("clam")

# Set the background color of the root window to purple
root.configure(bg=THEME_COLOR)

# Create a Frame for chat history
frame = ttk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Create a PanedWindow for chat history and user input
paned_window = ttk.PanedWindow(frame, orient=tk.VERTICAL)
paned_window.pack(fill=tk.BOTH, expand=True)

# Create a Text widget to display the chat history
chat_history_text = Text(
    paned_window,
    wrap=tk.WORD,
    state=tk.DISABLED,
    font=("Helvetica", 12),
    height=5,
)
scrollbar = Scrollbar(chat_history_text, command=chat_history_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_history_text.config(yscrollcommand=scrollbar.set)

# Create a Text widget for user input
user_input_text = Text(
    paned_window,
    wrap=tk.WORD,
    font=("Helvetica", 12),
    height=1,
)
scrollbar = Scrollbar(
    user_input_text,
    command=user_input_text.yview,
)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
user_input_text.config(yscrollcommand=scrollbar.set)
user_input_text.bind("<Return>", send_message)
user_input_text.bind("<Shift-Return>", handle_keypress)  # Bind Shift + Enter

# Add the widgets to the PanedWindow
paned_window.add(chat_history_text, weight=10)
paned_window.add(user_input_text, weight=1)
# user_input_text.place(x=0, y=0, relwidth=1.0, relheight=0.1)
# Create a Send button to send user input
send_button = Button(
    frame,
    text="Send",
    command=send_message,
    bg=THEME_COLOR,
    fg="#ffffff",
    font=("Helvetica", 12),
)
send_button.pack(pady=10)

root.geometry("600x400")
parser = argparse.ArgumentParser()
parser.add_argument(
    "--config",
    default="./config/config.yaml",
    help="Config file path",
)
console = Console()
args = parser.parse_args()

with open(args.config) as f:
    conf = yaml.safe_load(f)

verify_download_model(conf["model_path"], conf["model_url"])

with suppress_stdout_stderr():
    llm = LLM(conf, console)

root.protocol("WM_DELETE_WINDOW", close_window)
atexit.register(close_window)

# Start the GUI application
root.mainloop()
