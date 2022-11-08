import tkinter as tk
from tkinter import ttk

# An implementation of ttk.Entry with Events, Validation and Formatting
class EntryWithEvents(ttk.Entry):
    def __init__(self, master, max_len = None, widget_name = None, 
                 validation_method = None, set_justifiction = None, **kw):
        super().__init__(master, **kw)
        
        self.master = master        
        self.max_len = max_len
        self.widget_name = widget_name
        self.validation_method = validation_method
        self.set_justifiction = set_justifiction
        
        text_checker = self.master.register(self.is_valid_input)
        self.configure(validate="all", 
                       validatecommand=(text_checker, "%d", "%i","%P", 
                                        "%s", "%S", "%V", "%W"))

        self.bind('<Control-a>', self.__select_all)
        self.bind('<FocusOut>', self.do_validation)
        self.bind('<Return>', self.do_validation)
        
        # Initialise the field
        self.do_validation(None)
        
    def is_valid_input(self, d_action, i_index, P_text, 
                       s_prior_text, S_changed_text,  
                       V_callback, W_widget_name):
                       
        if False:
            print(self.widget_name + ", " + d_action + ', ' + i_index + ', ' + 
                  P_text + ', ' + 
                  s_prior_text + ', ' + S_changed_text + ', ' + 
                  V_callback + ', ' + W_widget_name)
        
        if V_callback == 'focusin':
            # select text after 100ms
            self.master.after(100, self.select_all)
            
        if V_callback == 'focusout':
            # deselect text
            self.select_clear()

        if self.max_len:
            if len(P_text) > self.max_len:
                return False
            
            return True

    def do_validation(self, e):
        if not self.validation_method == None:
            data = self.get()
            
            # vaidate date using function passed in
            result = self.validation_method(data)
            
            if self.set_justifiction == None:
                if not result[2] == None:
                    self.configure(justify = result[2])
    
            if result[0]:   # is valid so overwite data (delete and insert new)
                self.delete(0, len(data))
                self.insert(0, result[1])
            elif len(data) > 0:
                self.master.after(1, lambda: self.focus_set())

    def __select_all(self, key_press_event):
        self.master.after(1, self.select_all)
        
    def select_all(self):
        # select text
        self.select_range(0, 'end')
        # move cursor to the end
        self.icursor('end')
        #stop propagation
        return 'break'
