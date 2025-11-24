import tkinter as tk
from tkinter import messagebox, filedialog, StringVar, ttk
from PyPDF4.pdf import PdfFileReader, PdfFileWriter
import pyttsx3
from speech_recognition import Recognizer, AudioFile
from pydub import AudioSegment
import os

# Declaring global variables related to PDF to Speech conversion
global start_pgNo, end_pgNo
start_pgNo = None
end_pgNo = None

# Function to open the PDF selected and read text from it
def read():
    path = filedialog.askopenfilename()  # Get the path of the PDF based on the user's location selection
    if not path:
        messagebox.showerror("Error", "No file selected")
        return
    
    try:
        pdfLoc = open(path, 'rb')  # Opening the PDF
        pdfreader = PdfFileReader(pdfLoc)  # Creating a PDF reader object for the opened PDF
        speaker = pyttsx3.init()  # Initiating a speaker object
        
        start = int(start_pgNo.get())  # Getting the starting page number input
        end = int(end_pgNo.get())  # Getting the ending page number input
        
        # Reading all the pages from start to end page number
        for i in range(start, end + 1):
            page = pdfreader.getPage(i)  # Getting the page
            txt = page.extractText()  # Extracting the text
            speaker.say(txt)  # Getting the audio output of the text
            speaker.runAndWait()  # Processing the voice commands
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        pdfLoc.close()

# Function to create a GUI and get required inputs for PDF to Audio Conversion
def pdf_to_audio():
    global start_pgNo, end_pgNo
    
    # Creating a window
    wn1 = tk.Toplevel()
    wn1.title("PDF to Audio Converter")
    wn1.geometry('1920x1080')
    wn1.state('zoomed')  # Full-screen mode
    wn1.config(bg='#ffffff')
    
    frame = tk.Frame(wn1, bg='#eef1f8', bd=5, relief=tk.FLAT, padx=20, pady=20)
    frame.place(relx=0.5, rely=0.1, relwidth=0.9, relheight=0.8, anchor='n')
    
    start_pgNo = tk.IntVar(wn1)  # Variable to hold the starting page number
    end_pgNo = tk.IntVar(wn1)  # Variable to hold the ending page number
    
    tk.Label(frame, text='PDF to Audio Converter',
             fg='#1c1c1c', font=('Helvetica', 28, 'bold'), bg='#eef1f8').pack(pady=10)
    
    tk.Label(frame, text='Enter the start and end page numbers to read.\nFor a single page, enter the same number twice.', bg='#eef1f8', wraplength=600, justify='center', font=('Helvetica', 18)).pack(pady=10)
    
    # Getting the input of starting page number
    tk.Label(frame, text="Start Page:", bg='#eef1f8', font=('Helvetica', 20)).pack(pady=5)
    tk.Entry(frame, textvariable=start_pgNo, font=('Helvetica', 20), bg='#f7f9fc', relief=tk.FLAT).pack(pady=5)
    
    # Getting the input of ending page number
    tk.Label(frame, text="End Page:", bg='#eef1f8', font=('Helvetica', 20)).pack(pady=5)
    tk.Entry(frame, textvariable=end_pgNo, font=('Helvetica', 20), bg='#f7f9fc', relief=tk.FLAT).pack(pady=5)
    
    # Button to initiate the read function
    read_button = tk.Button(frame, text="Read PDF", command=read, bg='#3b82f6', fg='white', font=('Helvetica', 20, 'bold'), relief=tk.FLAT, cursor='hand2')
    read_button.pack(pady=20)
    read_button.bind("<Enter>", lambda e: e.widget.config(bg='#2563eb'))
    read_button.bind("<Leave>", lambda e: e.widget.config(bg='#3b82f6'))
    
    wn1.mainloop()  # Runs the window till it is closed

# Function to convert audio to text and write it into a PDF
def convert():
    source_file = filedialog.askopenfilename()  # Get the path of the audio file based on the user's location selection
    if not source_file:
        messagebox.showerror("Error", "No file selected")
        return
    
    try:
        # Converting the audio file to WAV format
        audio = AudioSegment.from_file(source_file)
        audio.export("temp.wav", format="wav")
        source_file = "temp.wav"
        
        # Initializing the recognizer object and converting the audio into text
        recog = Recognizer()
        with AudioFile(source_file) as source:
            recog.pause_threshold = 5
            speech = recog.record(source)
            text = recog.recognize_google(speech)
            write_text(pdf_loc.get(), text)
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        if os.path.exists("temp.wav"):
            os.remove("temp.wav")

# Function to write the text into a PDF
def write_text(pdf_loc, text):
    try:
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(PdfFileReader(io.BytesIO(text.encode('utf-8'))).getPage(0))
        with open(pdf_loc, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to create a GUI and get required inputs for Audio to PDF Conversion
def audio_to_pdf():
    global pdf_loc
    
    # Creating a window
    wn2 = tk.Toplevel()
    wn2.title("Audio to PDF Converter")
    wn2.geometry('1920x1080')
    wn2.state('zoomed')  # Full-screen mode
    wn2.config(bg='#ffffff')
    
    frame = tk.Frame(wn2, bg='#eef1f8', bd=5, relief=tk.FLAT, padx=20, pady=20)
    frame.place(relx=0.5, rely=0.1, relwidth=0.9, relheight=0.8, anchor='n')
    
    pdf_loc = StringVar(wn2)  # Variable to get the PDF path input
    
    tk.Label(frame, text='Audio to PDF Converter',
             fg='#1c1c1c', font=('Helvetica', 28, 'bold'), bg='#eef1f8').pack(pady=10)
    
    # Getting the PDF path input
    tk.Label(frame, text='Enter the PDF file location where you want to save (with extension):', bg='#eef1f8', font=('Helvetica', 20)).pack(pady=10)
    tk.Entry(frame, width=50, textvariable=pdf_loc, font=('Helvetica', 20), bg='#f7f9fc', relief=tk.FLAT).pack(pady=5)
    
    tk.Label(frame, text='Choose the audio file location that you want to read (.wav or .mp3 extensions only):',
             fg='#1c1c1c', bg='#eef1f8', font=('Helvetica', 20)).pack(pady=10)
    
    # Button to select the audio file and do the conversion
    convert_button = tk.Button(frame, text='Choose', bg='#3b82f6', fg='white', font=('Helvetica', 20, 'bold'), relief=tk.FLAT, cursor='hand2', command=convert)
    convert_button.pack(pady=20)
    convert_button.bind("<Enter>", lambda e: e.widget.config(bg='#2563eb'))
    convert_button.bind("<Leave>", lambda e: e.widget.config(bg='#3b82f6'))
    
    wn2.mainloop()  # Runs the window till it is closed

# Function to show tooltips
def create_tooltip(widget, text):
    tooltip = tk.Toplevel(widget, bg="#ffffff", padx=1, pady=1)
    tooltip.wm_overrideredirect(True)
    tooltip.wm_geometry("0x0")
    tooltip_label = tk.Label(tooltip, text=text, background="white", relief=tk.SOLID, borderwidth=1, wraplength=300)
    tooltip_label.pack()
    
    def show_tooltip(event):
        x = widget.winfo_rootx() + 30
        y = widget.winfo_rooty() + 30
        tooltip.wm_geometry(f"+{x}+{y}")
        tooltip_label.lift()

    def hide_tooltip(event):
        tooltip.wm_geometry("0x0")
        
    widget.bind("<Enter>", show_tooltip)
    widget.bind("<Leave>", hide_tooltip)

# Function to open About window
def open_about():
    about_window = tk.Toplevel()
    about_window.title("About")
    about_window.geometry('600x400')
    about_window.config(bg='#eef1f8')
    tk.Label(about_window, text="PDF to Audio and Audio to PDF Converter", fg='#1c1c1c', font=('Helvetica', 20, 'bold'), bg='#eef1f8').pack(pady=20)
    tk.Label(about_window, text="Version 1.0", fg='#1c1c1c', font=('Helvetica', 16), bg='#eef1f8').pack(pady=10)
    tk.Label(about_window, text="Developed by Your Name", fg='#1c1c1c', font=('Helvetica', 16), bg='#eef1f8').pack(pady=10)
    tk.Label(about_window, text="This application allows you to convert PDF files to audio and audio files to PDF.", wraplength=400, justify='center', font=('Helvetica', 14), bg='#eef1f8').pack(pady=10)
    about_window.mainloop()

# Creating the main window
wn = tk.Tk()
wn.title("PDF to Audio and Audio to PDF Converter")
wn.geometry('1920x1080')
wn.state('zoomed')  # Full-screen mode
wn.config(bg='#ffffff')

# Adding a menu
menu = tk.Menu(wn)
wn.config(menu=menu)
file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open PDF to Audio Converter", command=pdf_to_audio)
file_menu.add_command(label="Open Audio to PDF Converter", command=audio_to_pdf)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=wn.quit)

help_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=open_about)

# Main frame
frame = tk.Frame(wn, bg='#eef1f8', bd=5, relief=tk.FLAT, padx=20, pady=20)
frame.place(relx=0.5, rely=0.1, relwidth=0.9, relheight=0.8, anchor='n')

tk.Label(frame, text='PDF to Audio and Audio to PDF Converter',
         fg='#1c1c1c', font=('Helvetica', 32, 'bold'), bg='#eef1f8').pack(pady=20)

# Button to convert PDF to Audio form
pdf_to_audio_button = tk.Button(frame, text="Convert PDF to Audio", bg='#3b82f6', fg='white', font=('Helvetica', 24, 'bold'),
                                command=pdf_to_audio, relief=tk.FLAT, cursor='hand2')
pdf_to_audio_button.pack(pady=20)
pdf_to_audio_button.bind("<Enter>", lambda e: e.widget.config(bg='#2563eb'))
pdf_to_audio_button.bind("<Leave>", lambda e: e.widget.config(bg='#3b82f6'))
create_tooltip(pdf_to_audio_button, "Convert your PDF files into audio format.")

# Button to convert Audio to PDF form
audio_to_pdf_button = tk.Button(frame, text="Convert Audio to PDF", bg='#3b82f6', fg='white', font=('Helvetica', 24, 'bold'),
                                command=audio_to_pdf, relief=tk.FLAT, cursor='hand2')
audio_to_pdf_button.pack(pady=20)
audio_to_pdf_button.bind("<Enter>", lambda e: e.widget.config(bg='#2563eb'))
audio_to_pdf_button.bind("<Leave>", lambda e: e.widget.config(bg='#3b82f6'))
create_tooltip(audio_to_pdf_button, "Convert your audio files into PDF format.")

# Progress Bar
progress = ttk.Progressbar(frame, orient=tk.HORIZONTAL, length=300, mode='determinate')
progress.pack(pady=20)

def update_progress(value):
    progress['value'] = value
    wn.update_idletasks()

wn.mainloop()
