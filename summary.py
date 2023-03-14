import PyPDF2
import openai
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import time
import pyperclip
from tkinter.ttk import Progressbar

openai.api_key = "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"

progress_var = None
output_text = None
status_var = None


from PyPDF2 import PdfReader

import PyPDF4


def extract_text(filepath):
    # Open the PDF file in read-binary mode
    with open(filepath, 'rb') as pdf_file:
        # Create a PDF reader object
        pdf_reader = PyPDF4.PdfFileReader(pdf_file)

        # Create an empty string to store the text
        text = ''

        # Loop through each page in the PDF file
        for page_num in range(pdf_reader.getNumPages()):
            # Update the progress bar
            progress_var.set(page_num + 1)
            root.update_idletasks()
            root.update()

            # Get the page object
            page_obj = pdf_reader.getPage(page_num)

            # Extract the text from the page
            page_text = page_obj.extractText()

            # Add the text to the string
            text += page_text

    return text






def generate_summary(text):
    status_var.set('Generating summary...')
    words = text.split()
    max_words = 300
    prompt = " ".join(words[:max_words])
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Summarize this: {prompt}",
        temperature=0.9,
        max_tokens=256,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    summary = response.choices[0].text
    status_var.set('Summary generated')
    progress_var.set(100)
    return summary


def browse_file():
    filepath = filedialog.askopenfilename()
    if filepath.endswith('.pdf'):
        file_path_var.set(filepath)
        output_text.delete(1.0, tk.END)
    else:
        messagebox.showerror(title='Error', message='Please select a PDF file.')


def clear_output():
    output_text.delete(1.0, tk.END)


def copy_to_clipboard():
    pyperclip.copy(output_text.get(1.0, tk.END))


def save_summary():
    filepath = filedialog.asksaveasfilename(defaultextension='.txt')
    with open(filepath, 'w') as f:
        f.write(output_text.get(1.0, tk.END))


def summarize():
    filepath = file_path_var.get()
    if filepath:
        progress_var.set(0)
        pdf_text = extract_text(filepath)
        summary = generate_summary(pdf_text)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, summary)
    else:
        messagebox.showerror(title='Error', message='Please select a PDF file.')


root = tk.Tk()
root.title('Research paper PDF Summarizer ')

# File path label and entry field
file_path_label = tk.Label(root, text='File path:')
file_path_label.pack(pady=10)

file_path_var = tk.StringVar()
file_path_entry = tk.Entry(root, textvariable=file_path_var, width=100)
file_path_entry.pack()

# Browse button
browse_button = tk.Button(root,
text='Browse',
command=browse_file)
browse_button.pack(pady=10)

summarize_button = tk.Button(root,
text='Summarize',
command=summarize)
summarize_button.pack(pady=10)

clear_button = tk.Button(root,
text='Clear Output',
command=clear_output)
clear_button.pack(pady=10)

save_button = tk.Button(root,
text='Save Summary',
command=save_summary)
save_button.pack(pady=10)

copy_button = tk.Button(root,
text='Copy to Clipboard',
command=copy_to_clipboard)
copy_button.pack(pady=10)

output_text_label = tk.Label(root, text='Summary:')
output_text_label.pack(pady=10)

output_text = tk.Text(root, height=20, width=100)
output_text.pack()

progress_label = tk.Label(root, text='Progress:')
progress_label.pack(pady=10)

progress_var = tk.IntVar()
progress_bar = Progressbar(root, mode='determinate', variable=progress_var, maximum=100)
progress_bar.pack()

status_var = tk.StringVar()
status_var.set('Ready')
status_label = tk.Label(root, textvariable=status_var)
status_label.pack(pady=10)

root.mainloop()