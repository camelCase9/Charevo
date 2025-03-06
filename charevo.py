import os
import dotenv
import tkinter as tk
from tkinter import ttk
from openai import OpenAI
from pathlib import Path

app_name = "charevo"

# Thanks Claude for the help with the file and .env stuff, I'm not very knowledgeable in it; I learned a good deal in the process of getting this and working with it though
def set_api_key(key):
    """
    Sets the API key in a .env file named key.env
    Creates the file if it doesn't exist, otherwise updates it
    """
    env_path = Path(__file__).parent / "key.env"
    
    # Create the .env file if it doesn't exist
    if not env_path.exists():
        with open(env_path, "w"):
            pass
    
    # Load existing env file and update/set the API_KEY
    dotenv.load_dotenv(env_path)
    dotenv.set_key(env_path, "API_KEY", key)
    
    print(f"API key set successfully: {key}")

def get_api_key():
    """
    Checks if key.env exists and contains API_KEY
    If not, prompts the user for an API key
    Returns the API key
    """
    env_path = Path(__file__).parent / "key.env"
    
    if env_path.exists():
        dotenv.load_dotenv(env_path)
        api_key = os.getenv("API_KEY")
        
        if api_key:
            print(f"Using API key: {api_key}")
            return api_key
    
    # If we don't have a key, default to None
    set_api_key("None")
    return "None"

# Basic AI functions and setup \/

# Model variables (for easy updating as/if new models release)
model_reasoning = "r1-1776"
model_search = "sonar"
model_search_pro = "sonar_pro"
model_search_reasoning = "sonar_reasoning"
model_search_reasoning_pro = "sonar_reasoning_pro"
model_search_deep_research = "sonar_deep_research"

pplx = OpenAI(api_key=get_api_key(), base_url="https://api.perplexity.ai") # setting up the client; pplx short for perplexity

ask = pplx.chat.completions.create # just shortening that tongue-twister of a function

# preparing platforms as a class (why didn't they teach us what classes are in school... i hate my school... this feature is peak)
class platform:
    def __init__(self, exec_plat_prompt, prompt_base, fields):
        self.exec_plat_prompt = exec_plat_prompt
        self.fields = fields
        self.prompt_base = prompt_base

characterai = platform( # We all love c.ai. So much. Perfect site. Flawless. Completely incontroversial. Must support.
    exec_plat_prompt = "For the definition field it is recommended that you ask the search model twice and concatenate + format its results; once for lore, and once for dialogue examples. Do this by changing the extra part of the base prompt to specify which half you want, and be stern so we don't waste tokens on it accidentally doing both halves.",
    prompt_base = "", # replace the vars using .format(char_name, char_media, extra)
    fields = {
        "name": "Return the name of the character\n- Remain within the bounds of 20 text characters\n- Do not use emojis.",
        "tagline": "Write a creative and enticing tagline for the character's profile.\n- Emojis and special characters are permitted\n- Remain within the bounds of 50 text characters",
        "description": "\"How would your character describe themselves?\"\n- Write a summary of the key aspects of the character\n- Remain within the bounds of 500 text characters\n- Make sure the text is in first-person and is said as the character would say it!",
        "greeting": "Write a creative headstart to the user's conversation with this character",
        "definition": "Write the character's \"definition\"; a large, free-form field that can contain structured example dialogs or any text content.\n-Your character limit is 32,000, but you probably won't use all of it up.\n- The first three thousand or so are the most important of said characters to the bot.\n- There are a few reserved words or variables that you can use in your definition. They will be recognized and replaced anywhere in your text; {char}, {user}, and {random_user_x} (where X is an integer that identifies the random user. random_user_x generates a random name, and the same name remains for users with the same identification integer for reuse.)\n- The definition is the best place to add detailed lore and should be where you include character dialogue examples. (the syntax for character dialogue examples is as follows:\n{char}: Something the character said\nAnother character: Something another character said\n{user}: Something that the current chatter has previously told this character\n{random_user_x}: Something some random person said)\n Source character dialogue from wiki pages and other text sources."
    }
)

# It's time for the fun part- agentic AI. I may be in over my head but screw it, I'm hours in already!
def create_character(cname, cmedia, plat):
    fields_list = list(plat.fields.keys())  # Extract the list before using it in the f-string
    fields_dict = plat.fields
    initial_prompt = f"""
    You are the executive model behind an agentic AI process. Your goal is to fill all the required fields to create a chatbot of {cname} from {cmedia} for the AI chatbot platform {plat}'s character creation system. As the executive model, your job includes judging the responses of other models, adding to their prompts if it would be beneficial to, and formatting/returning the absolute final submissions. These are the fields you and your fellow models will be working with: {fields_list}

    These are the prompts that will be issued to them for each field:
    {fields_dict}
    """
    print(initial_prompt)
    print(fields_dict)
    # ask(model=model_reasoning, message=initial_prompt)

# UI

tkroot = tk.Tk(); tkroot.title(app_name)

# Welcome text
tkwelcomeframe = ttk.Frame(tkroot) ; tkwelcomeframe.pack()
tkwelcome = ttk.Label(tkwelcomeframe, text=f"Welcome to {app_name}, a Perplexity-based chatbot character creator. Provide an API key, fill in the fields, pick a platform, and let the AI do the rest.") ; tkwelcome.pack(padx=30, pady=10)

# Frame for inputs (uses grid)
tkinputframe = ttk.Frame(tkroot) ; tkinputframe.pack(padx = 30, pady=10)

# API key inputs
tkkeylabel = ttk.Label(tkinputframe, text="API Key:", width=10) ; tkkeylabel.grid(row=1, column=0)
tkkeyinput = ttk.Entry(tkinputframe, width = 50) ; tkkeyinput.grid(row=1, column=1)
tkkeyvaluetext = tk.StringVar()
tkkeyvaluetext.set(f"Current key: {get_api_key()}")
tkkeyvaluelabel = ttk.Label(tkinputframe, textvariable=tkkeyvaluetext) ; tkkeyvaluelabel.grid(row=2, column=1)
def keysubmit():
    set_api_key(tkkeyinput.get())
    tkkeyvaluetext.set(f"Current key: {tkkeyinput.get()}")  # ✅ Update StringVar properly
tkkeysubmit = ttk.Button(tkinputframe, width = 20, text="Save", command=keysubmit) ; tkkeysubmit.grid(row=1, column=2)
tkkeyinfolabel = ttk.Label(tkinputframe, text="Get a key at https://www.perplexity.ai/settings/api (paid)") ; tkkeyinfolabel.grid(row=1, column=3, padx=10)

# Name inputs
char_name = tk.StringVar()
char_name.set("None")
tknamelabel = ttk.Label(tkinputframe, text="Name:", width=10) ; tknamelabel.grid(row=3, column=0)
tknameinput = ttk.Entry(tkinputframe, width = 50) ; tknameinput.grid(row=3, column=1)
tknamevaluetext = tk.StringVar()
tknamevaluetext.set(f"Current name: {char_name.get()}")
tknamevaluelabel = ttk.Label(tkinputframe, textvariable=tknamevaluetext) ; tknamevaluelabel.grid(row=4, column=1)
def namesubmit():
    char_name.set(tknameinput.get())  # ✅ Update the StringVar
    tknamevaluetext.set(f"Current name: {char_name.get()}")  # ✅ Update the label
    print(char_name.get())  
tknamesubmit = ttk.Button(tkinputframe, width = 20, text="Save", command=namesubmit) ; tknamesubmit.grid(row=3, column=2)
tknameinfolabel = ttk.Label(tkinputframe, text="The name of your desired character.") ; tknameinfolabel.grid(row=3, column=3, padx=10)

# Media/IP inputs
char_media = tk.StringVar()
char_media.set("None")
tkmedialabel = ttk.Label(tkinputframe, text="Media:", width=10) ; tkmedialabel.grid(row=5, column=0)
tkmediainput = ttk.Entry(tkinputframe, width = 50) ; tkmediainput.grid(row=5, column=1)
tkmediavaluetext = tk.StringVar()
tkmediavaluetext.set(f"Current media/IP: {char_media.get()}")
tkmediavaluelabel = ttk.Label(tkinputframe, textvariable=tkmediavaluetext) ; tkmediavaluelabel.grid(row=6, column=1)
def mediasubmit():
    char_media.set(tkmediainput.get())  # ✅ Update the StringVar
    tkmediavaluetext.set(f"Current media/IP: {char_media.get()}")  # ✅ Update the label
    print(char_media.get())  
tkmediasubmit = ttk.Button(tkinputframe, width = 20, text="Save", command=mediasubmit) ; tkmediasubmit.grid(row=5, column=2)
tkmediainfolabel = ttk.Label(tkinputframe, text="Your character's IP of origin.") ; tkmediainfolabel.grid(row=5, column=3, padx=10)

# Platform input
char_platform = tk.StringVar()
char_platform.set("None")
tkplatformlabel = ttk.Label(tkinputframe, text="Platform:", width=10) ; tkplatformlabel.grid(row=7, column=0)
tkplatforminput = ttk.OptionMenu(tkinputframe, char_platform, "Tap for platform dropdown", "characterai") ; tkplatforminput.grid(row=7, column=1)
tkplatforminfolabel = ttk.Label(tkinputframe, text="The platform you'd like to generate fields for.") ; tkplatforminfolabel.grid(row=7, column=3, padx=10)

# Final submission frame
tksubmissionframe = ttk.Frame(tkroot) ; tksubmissionframe.pack(padx = 30, pady=40)
tksubmissionlabel = ttk.Button(tksubmissionframe, text=f"Ask the AI to create this chatbot (Warning: This can cost in the range of a dollar or two as it's based off of running multiple requests, sometimes repeatedly! $)", command=lambda: create_character(char_name.get(), char_media.get(), char_platform.get())) ; tksubmissionlabel.pack()

tk.mainloop()
