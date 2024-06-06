import tkinter as tk
from tkinter import Menu
from enum import Enum

class State(Enum):
    NONE = "white"
    INPUT = "gold"
    MOORE = "orange"
    CLOCK = "lime"
    COMB = "coral"
    OUTPUT = "yellow"
    WIRE = "black"

class DrawingApp:
    def __init__(self):

        self.__root = tk.Tk()
        self.__root.geometry("800x600")
        self.__root.title("Drawing Application")

        self.__left_frame = tk.Frame(self.__root, width=350, bg='cyan')
        self.__left_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.__left_frame.pack_propagate(0)

        self.__canvas = tk.Canvas(self.__root, bg='lightblue')
        self.__canvas.pack(fill=tk.BOTH, expand=True)

        self.__menu = Menu(self.__root)
        self.__root.config(menu=self.__menu)

        self.__draw_menu = Menu(self.__menu, tearoff=0)
        self.__menu.add_cascade(label="Draw", menu=self.__draw_menu)
        self.__draw_menu.add_command(label="Input Block", command=self.__createInput)
        self.__draw_menu.add_command(label="Moore Machine", command=self.__createMoore)
        self.__draw_menu.add_command(label="Clock", command=self.__createClock)
        self.__draw_menu.add_command(label="Combinational Block", command=self.__createComb)
        self.__draw_menu.add_command(label="Output Block", command=self.__createOutput)
        self.__draw_menu.add_command(label="Wire", command=self.__createWire)

        self.__start_x = None
        self.__start_y = None
        self.__current_mode = None

        self.__canvas.bind("<Button-1>", self.__on_click)
        self.__canvas.bind("<B1-Motion>", self.__on_drag)
        self.__canvas.bind("<ButtonRelease-1>", self.__on_release)
        self.__canvas.bind("<Button-3>", self.__on_right_click)

        self.addInfoLabel()

        self.__items = {}
        self.__state = State.NONE
        self.__highlightedItem = None

        self.__root.mainloop()

    def __set_box_mode(self):
        self.__current_mode = "box"
        self.__canvas.config(cursor="crosshair")

    def __createInput(self):
        self.__state = State.INPUT
        self.__set_box_mode()

    def __createMoore(self):
        self.__state = State.MOORE
        self.__set_box_mode()
    
    def __createClock(self):
        self.__state = State.CLOCK
        self.__set_box_mode()
    
    def __createComb(self):
        self.__state = State.COMB
        self.__set_box_mode()
    
    def __createOutput(self):
        self.__state = State.OUTPUT
        self.__set_box_mode()

    def __set_line_mode(self):
        self.__current_mode = "line"
        self.__canvas.config(cursor="crosshair")

    def __createWire(self):
        self.__state = State.WIRE
        self.__set_line_mode()

    def __on_click(self, event):
        self.__start_x = event.x
        self.__start_y = event.y

    def __on_drag(self, event):
        self.__canvas.delete("preview")
        if self.__current_mode == "box":
            self.__canvas.create_rectangle(self.__start_x, self.__start_y, event.x, event.y, outline='black', tag="preview")
        elif self.__current_mode == "line":
            self.__canvas.create_line(self.__start_x, self.__start_y, event.x, event.y, fill='black', tag="preview")

    def __on_release(self, event):
        if self.__current_mode == None:
            return
        
        self.__canvas.delete("preview")
        self.__remove_highlight()
        if self.__current_mode == "box":
            id = self.__canvas.create_rectangle(self.__start_x, self.__start_y, event.x, event.y, outline='black', fill = self.__state.value)
        elif self.__current_mode == "line":
            id = self.__canvas.create_line(self.__start_x, self.__start_y, event.x, event.y, fill='black')
        
        self.__assign(id, event)
        self.__add_highlight(id)
        self.__items[id].display()
        self.__current_mode = None
        self.__canvas.config(cursor="arrow")

    def __assign(self, id, event):
        if(self.__state == State.INPUT):
            self.__items[id] = Input(id, self)
        elif(self.__state == State.MOORE):
            self.__items[id] = Moore(id, self)
        elif(self.__state == State.CLOCK):
            self.__items[id] = Clock(id, self)
        elif(self.__state == State.COMB):
            self.__items[id] = Combinational(id, self)
        elif(self.__state == State.OUTPUT):
            self.__items[id] = Output(id, self)
        elif(self.__state == State.WIRE):
            self.__items[id] = Wire(id, self)
            return
        else:
            return
        
        self.__items[id].drawLabel(self.__start_x, self.__start_y, event.x, event.y)
    
    def __on_right_click(self, event):
        clicked_item = self.__canvas.find_closest(event.x, event.y)
        if clicked_item:
            self.__remove_highlight()
            self.__add_highlight(clicked_item[0])
            self.__items[clicked_item[0]].display()
        else:
            self.__remove_highlight()

    def __add_highlight(self, item_id):
        self.__highlightedItem = item_id
        self.__canvas.itemconfig(item_id, outline='red', width=3)

    def __remove_highlight(self):
        if self.__highlightedItem:
            self.__canvas.itemconfig(self.__highlightedItem, outline='black', width=1)
            self.__highlightedItem = None

    def deleteLeftPane(self):
        for widget in self.__left_frame.winfo_children():
            widget.destroy()
        self.addInfoLabel()
    
    def addInfoLabel(self):
        self.__info_label = tk.Label(self.__left_frame, text="Right Click on a block to see its information", bg = "cyan")
        self.__info_label.pack(pady=10)

    def addFields(self, fields, id):
        entries = {}

        for i, (label, value) in enumerate(fields.items()):
            frame = tk.Frame(self.__left_frame, bg="#e6e6e6")
            frame.pack(fill=tk.X, padx=10, pady=(5, 10))
            tk.Label(frame, text=label + ":", font=("Arial", 10), fg="#333333", bg="#e6e6e6").pack(side=tk.LEFT)
            entry = tk.Entry(frame, font=("Arial", 10), bg="#ffffff", fg="#333333", relief=tk.FLAT)
            entry.insert(0, value)
            entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
            entries[label] = entry

        submit_button = tk.Button(self.__left_frame, text="Submit", command=lambda : self.update_fields(entries, fields))
        submit_button.pack(pady=(0, 10))
    
    def update_fields(self, entries, fields):
        for label, entry in entries.items():
            fields[label] = entry.get()
        
    def getCanvas(self):
        return self.__canvas
        
class Block:
    
    def __init__(self, id, app):
        self.__id = id
        self.__app = app
        self._labelText = "Block"
        self._fields = {}

    def drawLabel(self, start_x, start_y, x, y):
        text_x = (start_x + x) / 2
        text_y = (start_y + y) / 2
        self.__app.getCanvas().create_text(text_x, text_y, text=f"{self._labelText}", fill="black")
    
    def display(self):
        self.__app.deleteLeftPane()
        self.__app.addFields(self._fields, self.__id)
        
class Input(Block):
    def __init__(self, id, app):
        super().__init__(id, app)
        self._labelText = "INPUT"
        self._fields["filePath"] = "filePath"
        self._fields["plot"] = "False"
        self._fields["blockID"] = "Input"

class Moore(Block):
    def __init__(self, id, app):
        super().__init__(id, app)
        self._labelText = "MOORE MACHINE"
        self._fields["maxOutSize"] = 0
        self._fields["plot"] = "False"
        self._fields["blockID"] = "Moore"
        self._fields["nsl"] = "lambda ps, i:0"
        self._fields["ol"] = "lambda ps:0"
        self._fields["startingState"] = 0

class Clock(Block):
    def __init__(self, id, app):
        super().__init__(id, app)
        self._labelText = "CLOCK"
        self._fields["plot"] = "False"
        self._fields["blockID"] = "Clock"
        self._fields["timePeriod"] = 1.2
        self._fields["onTime"] = 0.6
        self._fields["initialValue"] = 0

class Combinational(Block):
    def __init__(self, id, app):
        super().__init__(id, app)
        self._labelText = "COMBINATIONAL"
        self._fields["maxOutSize"] = 0
        self._fields["plot"] = "False"
        self._fields["blockID"] = "Combinational"
        self._fields["function"] = "lambda x:x"
        self._fields["delay"] = 0
        self._fields["initialValue"] = 0

class Output(Block):
    def __init__(self, id, app):
        super().__init__(id, app)
        self._labelText = "OUTPUT"
        self._fields["plot"] = "False"
        self._fields["blockID"] = "Output"

class Wire(Block):
    def __init__(self, id, app):
        super().__init__(id, app)
        self._labelText = "WIRE"

if __name__ == "__main__":
    
    app = DrawingApp()
    
