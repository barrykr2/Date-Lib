import tkinter as tk
import clsDates as dateLib
import clsStatusBar as status_bar

chkDate = dateLib.check_date(None, dateLib.nullDate)
chkDate.allowShortCutKeys = True

# All methods here MUST return a tupple with 3 elements
#         0 - Is Valid True/False
#         1 - The formated value
#         2 - The justification in the field
class validate:
    def __init__(self, statusBarObj = None, errorLogObj = None):
        self.statusBarObj = statusBarObj
        self.errorLogObj = errorLogObj
    
    # ------ Start of Data Type Validations ------
    def validate_decimal(self, value = None, decimal_places = 2):
        formatting = "{: ." + str(decimal_places) + "f}"
        returnValue = (False, formatting.format(0), tk.RIGHT)
        
        if value:
            try:
                returnValue = (True, formatting.format(float(value)), returnValue[2])
            except Exception as e:
                pass
        
            self.update_status_bar(not returnValue[0], 'Error: "' + str(value) + '" not a number (type: decimal(' + str(decimal_places) + '))')
        return returnValue
    
    def validate_float(self, value = None):
        returnValue = (False, 0, tk.RIGHT)
        
        if value:
            try:
                returnValue = (True, float(value), returnValue[2])
            except Exception as e:
                pass
        
            self.update_status_bar(not returnValue[0], 'Error: "' + str(value) + '" not a number (type: float)')
        return returnValue
    
    def validate_integer(self, value = None):
        returnValue = (False, 0, tk.RIGHT)
        
        if value:
            try:
                returnValue = (True, int(value), returnValue[2])
                self.update_status_bar(not returnValue[0], 'Error: "' + str(value) + '" not a number (type: integer)')
            except Exception as e:
                tmpVal = self.validate_float(value)
                if tmpVal[0]:
                    returnValue = (True, round(float(value)), returnValue[2])
                    if float(value) > float(returnValue[1]):
                        self.update_status_bar(True, 'Info: "' + str(value) + '" rounded down (type: integer)')
                    else:
                        self.update_status_bar(True, 'Info: "' + str(value) + '" rounded up (type: integer)')
                else:
                    self.update_status_bar(not returnValue[0], 'Error: "' + str(value) + '" not a number (type: integer)')
        return returnValue
    
    def validate_Date(self, value = None):
        returnValue = (False, dateLib.nullDate, tk.CENTER)
        print(value)
        if value:
            try:
                chkDate.dateCheck(value)
                self.update_status_bar(not chkDate.isValid, chkDate.messages)                
                returnValue = (chkDate.isValid, chkDate.formattedDate, returnValue[2])
            except Exception as e:
                pass
        
        return returnValue
    # ------ End of Data Type Validations ------
    
    def update_status_bar(self, display_message = False, message = None):
        if not self.statusBarObj == None:
            if display_message:
                self.statusBarObj.statusVar.set(message)
            else:
                self.statusBarObj.statusVar.set(self.statusBarObj.default_text)
        
            self.statusBarObj.sbar.update()
    