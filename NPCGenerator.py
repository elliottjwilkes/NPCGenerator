import openai
import requests
from PIL import Image
from PIL import ImageTk
import tkinter as tk
from io import BytesIO

openai.api_key = 'YOUR KEY HERE' 

character_name = input("What is your character's name: ")

character_gender = input("What is your character's gender: ")
character_race = input("What is your character's race: ")
character_appearance = input("Who's face is?: ")
character_outfit = input("Who's wearing?: ")
character_location = input("In a?: ")
character_misc = input("Any more added detail (this will be a sentence at the end of the prompt):")

character_personality = input("Describe the character's personality, occupation, and any other details:")

character_prompt = "A realistic portrait of a " + character_gender + ", " + character_race + " who's face is " + character_appearance + " and is wearing " + character_outfit + " in a " + character_location + ". " + character_misc

response = openai.Image.create(
  prompt=character_prompt,
  n=1,
  size="1024x1024"
)

image_url = response['data'][0]['url']

response = requests.get(image_url)
image_data = response.content

image = Image.open(BytesIO(image_data))

messages = [
    {"role": "system", "content": "You are called " + character_name + "and you are " + character_personality},
]

def submit_input():
    message = input_box.get()
    if message:
        text_widget.insert(tk.END, "User: " + message + "\n\n")
        messages.append({"role": "user", "content": message})
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        reply = chat.choices[0].message.content
        text_widget.insert(tk.END, f"{character_name}: {reply}\n\n")
        input_box.delete(0, tk.END)
        messages.append({"role": "assistant", "content": reply})

root = tk.Tk()
root.title(character_name)

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

photo = ImageTk.PhotoImage(image)
image_label = tk.Label(frame, image=photo)
image_label.grid(row=0, column=0)

input_box = tk.Entry(frame, width=40)
input_box.grid(row=0, column=1, padx=10, pady=10)

submit_button = tk.Button(frame, text="Submit", command=submit_input)
submit_button.grid(row=0, column=2, padx=10, pady=10)

text_widget = tk.Text(root, height=10, width=40)
text_widget.pack(side="right", fill="both", expand=True)

root.mainloop()
