# clsErrors.py - class to log errors

import sys
import traceback as trace_Back 
import logging

class logger:
    def __init__(self, logger_file_name = 'mylog.log', display_err_stout = False):
        self.display_err_stout = display_err_stout
        self.traceBack = trace_Back
        
        # Create or get the logger
        self.logger = logging.getLogger(__name__)  

        handler = logging.FileHandler(logger_file_name)
        # create a logging format
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        # set log level
        self.logger.setLevel(logging.ERROR)

    def log(self, errException, sys_exc_info):
        self.logger.exception(errException)

        exc_type, exc_value, exc_traceback = sys_exc_info
        # eventually log to file and/or email
        self.traceBack.print_stack  
        if self.display_err_stout:
            self.traceBack.print_exception(exc_value, file=sys.stdout)


if __name__ == "__main__":
    errorLog = logger('mylog.log', True)
    
    # ==== Test above class ====
    try:
        y = 2
        x = y / 0
    except Exception as e:
        errorLog.log(e, sys.exc_info())
    
