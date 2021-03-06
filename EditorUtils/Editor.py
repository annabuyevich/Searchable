import tkinter.simpledialog as tksd
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

from pyparsing import basestring

from EditorUtils import Status_Bar
from SearchFeatures import Entity_Analysis, Synonym_Search, Part_Speech_Search, \
    Sentence_Structure_Search, Word_Structure_Search

# set up the frame
master = Tk()
master.title("Searchable")
master.geometry("400x380")

text = Text(master, width=400, height=380, font=("Andale Mono", 12), highlightthickness=0, bd=2)

labelText = StringVar()

status = Status_Bar.StatusBar(master)
status.pack(side=BOTTOM, fill=X)
text.pack()


# Methods
def new():
    ans = messagebox.askquestion(title="Save File", message="Would you like to save this file?")
    if ans is True:
        save()
    delete_all()


def open_file():
    new()
    file = filedialog.askopenfile()
    # take whatever is in file and put it in box
    text.insert(INSERT, file.read())


def save():
    path = filedialog.asksaveasfilename()
    write = open(path, mode='w')
    write.write(text.get("1.0", END))


def close():
    save()
    master.quit()


def cut():
    master.clipboard_clear()
    text.clipboard_append(string=text.selection_get())
    text.delete(index1=SEL_FIRST, index2=SEL_LAST)


def copy():
    master.clipboard_clear()
    text.clipboard_append(string=text.selection_get())


def paste():
    text.insert(INSERT, master.clipboard_get())


def delete():
    text.delete(index1=SEL_FIRST, index2=SEL_LAST)


def select_all():
    text.tag_add(SEL, "1.0", END)


def delete_all():
    text.delete(1.0, END)


def search_synonyms():
    text.tag_remove("tag", "1.0", END)

    # get the text from the text editor
    the_text = text.get("1.0", END)

    user_input = tksd.askstring("Search Synonyms", "Enter your search:", parent=master)

    if len(str(user_input)) == 0:
        messagebox.showinfo("Synonym", "No text in the search.")
        return
    elif text.compare("end-1c", "==", "1.0"):
        messagebox.showinfo("Synonym", "No text in the editor.")
    else:
        search_word = str(user_input).lower()

        result_dict = Synonym_Search.word_to_concepts(the_text)
        print('result_dict: ', result_dict)

        if len(result_dict.values()) == 0:
            return
        elif search_word not in result_dict:
            messagebox.showinfo("Synonym", "Search word not found.")
            return
        else:
            word_syns = result_dict[search_word]

        for item in word_syns:
            print("word: " + str(item[0]) + " line: " + str(item[1]) + " , " + " column: " + str(item[2]))

            if item[2] is None:
                continue
            else:
                print(("tag", str(item[1]) + "." + str(item[2]), str(item[1]) + "." + str(len(item[0]) + item[2])))
                text.tag_add("tag", str(item[1]) + "." + str(item[2]), str(item[1]) + "." + str(len(item[0]) + item[2]))
                text.tag_config("tag", background="#b3b3cc", foreground="black")
        status.set("Synonym search complete for: " + search_word)


def part_speech():
    text.tag_remove("tag", "1.0", END)

    # get the text from the text editor
    the_text = text.get("1.0", END)

    user_input = tksd.askstring("Part of Speech Search", "Enter your grammar search:", parent=master)

    if len(str(user_input)) == 0:
        messagebox.showinfo("Part of Speech Search", "No text in the search.")
        return
    elif text.compare("end-1c", "==", "1.0"):
        messagebox.showinfo("Part of Speech Search", "No text in the editor.")
        return
    else:

        part_word = str(user_input).lower()

        pos_acr_list = Part_Speech_Search.part_of_speech_to_tag(part_word)
        r_dict = Part_Speech_Search.make_dict(the_text, the_text)
        print(r_dict)

        if len(part_word) == 0:
            return
        elif pos_acr_list is None:
            messagebox.showinfo("Part of Speech", str(user_input) + " not part of speech.")
            return

        for pos_acr in pos_acr_list:
            if pos_acr in r_dict.keys():
                word_speech = r_dict[pos_acr]

                for item in word_speech:
                    print("word: " + str(item[0]) + " line: " + str(item[1]) + " , " + " column: " + str(item[2]))
                    if item[2] is None:
                        continue
                    else:
                        text.tag_add("tag", str(item[1]) + "." + str(item[2]),
                                     str(item[1]) + "." + str(len(item[0]) + item[2]))
                        text.tag_config("tag", background="light blue", foreground="black")
        status.set("Part of speech search complete for:  " + part_word)


def entity():
    text.tag_remove("tag", "1.0", END)

    the_text = text.get("1.0", END)

    user_input = tksd.askstring("Entity Search", "Enter your type search:", parent=master)
    s_word = str(user_input).lower()

    if text.compare("end-1c", "==", "1.0"):
        messagebox.showinfo("Entity", "No text in the search.")
        print("hi")
        return
    elif text.compare("end-1c", "==", "1.0"):
        messagebox.showinfo("Entity", "No text in the editor.")
        return
    else:
        s_word = str(user_input).lower()

        # returns a dictionary
        s_dict = Entity_Analysis.create_dict(s_word, the_text)
        print(s_dict)

        if len(s_dict.values()) == 0:
            return
        else:

            # list of values
            word_speech = s_dict[s_word]
            print("word- speech", word_speech)

            # get inside the tuple
            for element in word_speech:

                # check if it is a list
                if not isinstance(element, basestring):

                    # looking at the tuples
                    for item in element:

                        if type(item) is tuple:
                            print(("tag", str(item[0]) + "." + str(item[1]),
                                   str(item[0]) + "." + str(item[1] + word_len)))
                            text.tag_add("tag", str(item[0]) + "." + str(item[1]),
                                         str(item[0]) + "." + str(item[1] + word_len))
                            text.tag_config("tag", background="light green", foreground="black")
                        else:
                            continue

                else:
                    word_len = (len(element))
    status.set("Entity search complete for: " + s_word)
    s_dict.clear()


def word_structure_search():
    text.tag_remove("tag", "1.0", END)

    the_text = text.get("1.0", END)

    user_input = tksd.askstring("Similar Structure - Word", "Enter a word in the text:", parent=master)
    max_distance = tksd.askstring("Similar Structure - Word",
                                  "Enter the upper bound for the word structure search:", parent=master)

    if len(str(user_input)) == 0:
        messagebox.showinfo("Similar Structure - Word", "No text in the search.")
        return
    if text.compare("end-1c", "==", "1.0"):
        messagebox.showinfo("Similar Structure - Word", "No text in the editor.")
        return
    else:
        word = str(user_input).lower()
        max_distance = int(max_distance)

        if Word_Structure_Search.find_word(word, max_distance, the_text) is not None:
            l_dict = Word_Structure_Search.find_word(word, max_distance, the_text)

        print(l_dict)

        if len(l_dict.values()) == 0:
            return
        elif word not in the_text:
            messagebox.showinfo("Similar Structure - Word", "Word not in text.")
            return
        else:
            word_list = l_dict[word]

            for item in word_list:
                print("word: " + str(item[0]) + " line: " + str(item[1]) + " , " + " column: " + str(item[2]))
                if item[2] is None:
                    continue
                else:
                    text.tag_add("tag", str(item[1]) + "." + str(item[2]),
                                 str(item[1]) + "." + str(len(item[0]) + item[2]))
                    text.tag_config("tag", background="light pink", foreground="black")

        status.set("Similar Structure for word: " + word + " - " + str(max_distance))


def sentence_structure_search():
    text.tag_remove("tag", "1.0", END)
    the_text = text.get("1.0", END)

    sentence_one = tksd.askstring("Similar Structure - Sentence", "Enter a sentence for similar structure search:",
                                  parent=master)

    max_distance = tksd.askstring("Similar Structure - Sentence",
                                  "Enter the upper bound for similar structure search:", parent=master)

    max_distance = int(max_distance)

    if len(str(sentence_one)) == 0:
        messagebox.showinfo("Similar Structure - Sentence", "No text in the search.")
        return
    elif len(the_text) == 1:
        messagebox.showinfo("Similar Structure - Sentence", "No text in the editor.")
        return
    else:
        result_list = Sentence_Structure_Search.create_list(sentence_one, the_text, max_distance)
        print('result ', result_list)
        for item in result_list:
            text.tag_add("tag", item[0], item[1])
            text.tag_config("tag", background="#ff8080", foreground="black")

        status.set("Similar Structure for Sentence: " + sentence_one + "  - " + str(max_distance))


def get_sentiment():
    text.tag_remove("tag", "1.0", END)
    the_text = text.get("1.0", END)

    sentiment = Entity_Analysis.GetData.get_sentiment(the_text)
    messagebox.showinfo("Text Sentiment:", "sentiment: " + sentiment[3] + "\nscore: " + str(sentiment[1]))


def get_emotion():
    text.tag_remove("tag", "1.0", END)
    the_text = text.get("1.0", END)

    emotions = Entity_Analysis.GetData.get_emotion(the_text)
    result = ""
    for emotion in emotions.keys():
        result += emotion + ": " + str(emotions[emotion]) + "\n"
    messagebox.showinfo("Text Emotion:", result)


# File Menu
menu = Menu(master)
# set menu and makes main menu
master.config(menu=menu)
file_menu = Menu(menu)

menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_separator()
file_menu.add_command(label="Close", command=close)
file_menu.add_command(label="Save", command=save)

# Edit Menu
edit_menu = Menu(menu)
menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Undo", command=text.edit_undo)
edit_menu.add_command(label="Redo", command=text.edit_redo)
edit_menu.add_separator()
edit_menu.add_command(label="Cut", command=cut)
edit_menu.add_command(label="Copy", command=copy)
edit_menu.add_command(label="Paste", command=paste)
edit_menu.add_command(label="Delete", command=delete)
edit_menu.add_separator()
edit_menu.add_command(label="Select All", command=select_all)

# Search Menu

search_menu = Menu(menu)
menu.add_cascade(label="Search", menu=search_menu)
search_menu.add_command(label="Synonyms", command=search_synonyms)
search_menu.add_command(label="Entity", command=entity)
search_menu.add_cascade(label="Part of Speech", command=part_speech)

extra_menu = Menu(menu)
search_menu.add_cascade(label="Similar Structure", menu=extra_menu)
extra_menu.add_command(label="Word", command=word_structure_search)
extra_menu.add_command(label="Sentences", command=sentence_structure_search)

text_analysis_menu = Menu(menu)
menu.add_cascade(label="Analyze", menu=text_analysis_menu)
text_analysis_menu.add_command(label="Sentiment", command=get_sentiment)
text_analysis_menu.add_command(label="Emotion", command=get_emotion)

text.focus_set()

master.mainloop()
