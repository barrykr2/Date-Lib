import tkinter as tk
from tkinter import ttk
import clsStatusBar as status_bar
import clsValidateData as validate
import wgtEntryWithEvents as myWidgetEntryWithEvents 

root = tk.Tk()
root.geometry("400x400")

# first always create the status bar
sbar = status_bar.status_bar_obj(root, "Ready", "Loading...")
val = validate.validate(sbar)

# Initial an implementation of ttk.Entry with Events, Validation and Formatting
EntryWithEvents = myWidgetEntryWithEvents.EntryWithEvents

        
entry_date = EntryWithEvents(root, max_len = 11, widget_name = 'entry_date', 
                             validation_method = val.validate_Date,
                             set_justifiction = tk.LEFT)
entry_date.pack(expand=True)


entry_details = EntryWithEvents(root, max_len = 11, widget_name = 'entry_detail', 
                                validation_method = val.validate_Date)
entry_details.pack(expand=True)


entry_float = EntryWithEvents(root, max_len = 15, widget_name = 'entry_float', 
                              validation_method = val.validate_float)
entry_float.pack(expand=True)


entry_decimal = EntryWithEvents(root, max_len = 15, widget_name = 'entry_decimal', 
                              validation_method = val.validate_decimal)
entry_decimal.pack(expand=True)


entry_integer = EntryWithEvents(root, max_len = 15, widget_name = 'entry_integer', 
                              validation_method = val.validate_integer)
entry_integer.pack(expand=True)


entry_none = EntryWithEvents(root)
entry_none.pack(expand=True)

# set focus to the field I want
root.after(1, lambda: entry_date.focus_set())

sbar.update()

root.mainloop()