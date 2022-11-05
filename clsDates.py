# Written by Barry Kruyssen Oct 2022.
# Feel free to use as you like :-)
# This class check_Date is used for validaing a date, formatting and manipulating dates.
# It handles both DMY and MDY input/output formats.
#
# It also allows for short cut keys.
# (assuming Australian format - swap "d" and "m" for US date format)
#       "." use last date processed
#       ".." use last date processed plus 1 day
#       "--" use last date processed less 1 day
#       "d" will substitute the month day of the last date processed
#       "ddmm" will substitute the day and month of the last date processed
#       "d/m" will substitute the day and month of the last date processed
#       "ddmmyy" will substitute the expand to a date
# By default short cut keys is turned off so as to run less code when doing
# straight validation. 
#
# Error logging is impemented on all public function while private
# function errors will be logged from the calling public function.
# Error logging is a "work in progress" and will be cleaned up in the next
# week or so.
#
# Please see the test cases at the bottom of the code for examples
#

from dateutil.parser import parse
from datetime import datetime, timedelta
from enum import Enum
import string, sys
import clsErrors as errorLogger

class EF(Enum):
    Day_Month_Year = 0
    Month_Day_Year = 1
    
nullDate = '1900-01-01'
defaultFullDate = "%Y-%m-%d"
defaultFormattedDate = ["%d-%b-%Y", "%b-%d-%Y"]
defaultLogFile = 'myLog.log'
defaultToStdOut = False

class check_date:
    # The class is initialised with:
    #  - an errorLog object can be passed in (so we only have one error log object for the whole application)
    #    else a default error log is used.
    #  - a date may be passed in which will be validated (eleviating the need to call the checkDate function)
    #  - formatting is passed in if you want a different date output
    #  - the expectedInputFormat defines whether we are using US date format or not (default is NOT)
    #  - if allowShortCutKeys, this defaults to False as for processing the short cut keys should only be
    #    needed when called from a GUI. 
    def __init__(self, errorLogObj = None,
                 date = nullDate, formatting = "",
                 expectedInputFormat = EF.Day_Month_Year,
                 allowShortCutKeys = False):
        # initialise all variables
        self.isValid = False
        self.expectedInputFormat = expectedInputFormat
        self.dateObj = datetime.strptime(nullDate, defaultFullDate)
        self.allowShortCutKeys = allowShortCutKeys
        self.__setSelf(formatting)

        if errorLogObj == None:
            self.errorLog = errorLogger.logger(defaultLogFile, defaultToStdOut)
        else:
            self.errorLog = errorLogObj

        # validate date
        self.dateCheck(date, formatting)
        
    def __setSelf(self, formatting = ""):
        formatting = self.__setDefaultFormattedDate(formatting)

        self.day = self.dateObj.day
        self.month = self.dateObj.month
        self.year = self.dateObj.year
        self.fullDate = datetime.strftime(self.dateObj, defaultFullDate)
        self.formattedDate = self.dateObj.strftime(formatting)
        self.priorObj = self.dateObj

    def __setDefaultFormattedDate(self, formatting = ""):
        if formatting == '':
            formatting = defaultFormattedDate[self.expectedInputFormat.value]
        return formatting

    def __replaceSeperators(self, date):
        # replace all date seperators with "-" for uniformity
        space_punct_dict = dict((ord(punct), '-') for punct in string.punctuation)
        return date.translate(space_punct_dict)
        
    def __processShortCutKeys(self, date):
        # check if the date is using the prior date object to calc a new date
        if date == 't':                             # use today's date
            date = datetime.today().strftime(self.__setDefaultFormattedDate(''))
        if date == '.':                             # use prior date
            date = self.formattedDate
        elif date == '..':                          # prior date plus 1 day
            dateobj = self.priorObj + timedelta(days = 1)
            date = dateobj.strftime(self.__setDefaultFormattedDate(''))
        elif date == '--':                          # prior date less 1 day
            dateobj = self.priorObj + timedelta(days = -1)
            date = dateobj.strftime(self.__setDefaultFormattedDate(''))

        # replace all date seperators with "-" for uniformity
        tmpDate = self.__replaceSeperators(date)

        # check if incomplete date, try to format and add year if required
        if len(tmpDate) <= 6:
            tmpArray = str(tmpDate).split('-')
            if len(tmpArray) == 1:
                if len(tmpDate) <= 2:
                    if self.expectedInputFormat == EF.Day_Month_Year:
                        tmpDate = str(tmpDate)[:2] + '-' + str(self.priorObj.month) + '-' + str(self.priorObj.year)
                    else:
                        tmpDate = str(self.priorObj.month) + '-' + str(tmpDate)[:2] + '-' + str(self.priorObj.year)
                if len(tmpDate) == 4:
                    tmpDate = str(tmpDate)[:2] + '-' + str(tmpDate)[2:] + '-' + str(self.priorObj.year)
                if len(tmpDate) == 6:
                    tmpDate = str(tmpDate)[:2] + '-' + str(tmpDate)[2:4] + '-' + str(tmpDate)[4:]
            elif len(tmpArray) == 2:
                tmpDate = str(tmpArray[0]) + '-' + str(tmpArray[1]) + '-' + str(self.priorObj.year)
        return tmpDate

    # Function dateCheck is the main function that does checking and processing
    #  - a date (or possible date) is passed in be validated or processed as a short cut key
    #  - formatting is passed in if you want a different date output
    def dateCheck(self, date, formatting = ""):
        # Initialise date object
        self.dateObj = datetime.strptime(nullDate, defaultFullDate)

        try:
            if date:
                if self.allowShortCutKeys:
                    tmpDate = self.__processShortCutKeys(date)
                else:
                    # replace all date seperators with "-" for uniformity
                    tmpDate = self.__replaceSeperators(date)

                dayFirst = False        # US format mm-dd-yyyy
                if self.expectedInputFormat == EF.Day_Month_Year:
                    dayFirst = True     # Australian format dd-mm-yyyy

                try:# deactivate the system wide error trapping as an error
                    # is expected when an invalid date is passed in.
                    
                    # get date object - The next line is where the actual date is validated                                                                                         is whe                                                         
                    self.dateObj = parse(tmpDate, dayfirst = dayFirst)
                    self.isValid = datetime.strftime(self.dateObj, defaultFullDate) != nullDate
                except Exception as e:
                    self.isValid = False
                    print(e)

                # only allow dates upto 5 years in the future
                if self.dateObj.year > datetime.today().year + 5:
                    tmpYear = self.dateObj.year - 100
                    self.dateObj = self.dateObj.replace(year = tmpYear)

                # reset variables
                self.__setSelf(self.__setDefaultFormattedDate(formatting))
        except Exception as e:
            self.isValid = False
            self.errorLog.log(e, sys.exc_info())                

        return self.formattedDate
    
    def formatDate(self, date = nullDate, formatting = ""):
        try:
            if date == nullDate:
                date = self.formattedDate    # date hasn't changed so use current Object (faster when reusing date object)
            else:            
                self.dateCheck(date, formatting)    # check date passed in
        except Exception as e:
            self.isValid = False
            self.errorLog.log(e, sys.exc_info())                

        return self.formattedDate
        
    def addDay(self, numberOfDays = 1, formatting = "", date = nullDate):
        try:
            if date != nullDate:
                self.dateCheck(date, formatting)    # check date passed in

            dateobj = self.dateObj + timedelta(days = numberOfDays)
            self.dateCheck(dateobj.strftime(self.__setDefaultFormattedDate(formatting)), formatting)
        except Exception as e:
            self.isValid = False
            self.errorLog.log(e, sys.exc_info())                

        return self.formattedDate

    def subtractDay(self, numberOfDays = 1, formatting = "", date = nullDate):
        returnDate = self.formattedDate
        
        try:
            returnDate = self.addDay(numberOfDays * -1, formatting, date)
        except Exception as e:
            self.isValid = False
            self.errorLog.log(e, sys.exc_info())                
            
        return returnDate

if __name__ == "__main__":
    def testCheck(testId, expectedResult, restultReturned, now, displayErrorsOnly = True):
        isError = ''
        if expectedResult != restultReturned:
            isError = 'Error: '
            
        if (not displayErrorsOnly) or len(isError) > 0:
            actualNow = datetime.now()
            deltaTime = (actualNow - now)
            print(("%.6f" % deltaTime.total_seconds()) + ' ' + isError + testId + ' - Expected "' +
                  expectedResult + '": = ' + restultReturned)

        now = datetime.now() # time object

        return now
            
    # Test cases
    startTime = datetime.now() # time object
    print('-------------------- Testing Started ' + str(startTime.time()) + ' --------------------')
    displayErrorsOnly = False
    now = datetime.now() # time object
    
    chk = check_date(None, nullDate)
    now = testCheck('chk0 initialise class', 'nothing', 'nothing', now, displayErrorsOnly)
    now = testCheck('chk1', 'False', str(chk.isValid), now, displayErrorsOnly)

    x = check_date(errorLogger.logger('myLogX.log', True), '23-09-71')
    now = testCheck('get another instance of class', 'nothing', 'nothing', now, displayErrorsOnly)
    now = testCheck('x0', 'True', str(x.isValid), now, displayErrorsOnly)
    now = testCheck('x1', '1971-09-23', str(x.fullDate), now, displayErrorsOnly)
    now = testCheck('x2', '23', str(x.day), now, displayErrorsOnly)
    now = testCheck('x3', '23-Sep-1971', x.formattedDate, now, displayErrorsOnly)
    now = testCheck('x4', 'Feb-01-1960', str(x.formatDate('01/02/1960', '%b-%d-%Y')), now, displayErrorsOnly) # US formatted
    now = testCheck('x5', '1960-02-01', str(x.fullDate), now, displayErrorsOnly)      
    now = testCheck('x6', '1963 Sep 23', str(x.formatDate('1963-Sep-23', '%Y %b %d')), now, displayErrorsOnly)
    now = testCheck('x7', '1963-09-23', str(x.fullDate), now, displayErrorsOnly)
    x.expectedInputFormat = EF.Month_Day_Year
    now = testCheck('x8', '2022-Mar-01', x.formatDate('03/01/22', '%Y-%b-%d'), now, displayErrorsOnly)
    now = testCheck('x9', '2022-03-01', str(x.fullDate), now, displayErrorsOnly)      
    now = testCheck('x10', '2022-Mar-01', str(x.formattedDate), now, displayErrorsOnly)      
    now = testCheck('x11', 'Mar-02-2022', str(x.addDay(1,'%b-%d-%Y')), now, displayErrorsOnly)
    now = testCheck('x12', 'Apr-01-2022', str(x.addDay(30)), now, displayErrorsOnly)
    now = testCheck('x13', 'Apr-02-2022', str(x.addDay()), now, displayErrorsOnly)
    now = testCheck('x14', 'Dec-17-2022', str(x.formatDate('17 Dec 2022')), now, displayErrorsOnly)
    now = testCheck('x15', 'Jan-02-1960', x.dateCheck('01.02,1960'), now, displayErrorsOnly)
    x.allowShortCutKeys = True
    now = testCheck('x16', 'Jan-02-1960', x.dateCheck('.'), now, displayErrorsOnly)
    now = testCheck('x17', 'Jan-03-1960', x.dateCheck('..'), now, displayErrorsOnly)
    now = testCheck('x18', 'Jan-02-1960', x.dateCheck('--'), now, displayErrorsOnly)
    now = testCheck('x19', 'Sep-23-1963', x.dateCheck('092363'), now, displayErrorsOnly)
    now = testCheck('x20', 'Sep-23-1963', x.dateCheck('09/23'), now, displayErrorsOnly)
    now = testCheck('x21', 'Sep-23-1963', x.dateCheck('0923'), now, displayErrorsOnly)
    now = testCheck('x22', 'Apr-05-1963', x.dateCheck('4/5'), now, displayErrorsOnly)
    now = testCheck('x23', 'Apr-11-1963', x.dateCheck('11'), now, displayErrorsOnly)
    x.expectedInputFormat = EF.Day_Month_Year
    now = testCheck('x23', '03-Apr-1963', x.dateCheck('3'), now, displayErrorsOnly)
    now = testCheck('x24', '02-Apr-1963', str(x.subtractDay()), now, displayErrorsOnly)
    x.allowShortCutKeys = False
    now = testCheck('x25', '01-Jan-1900', x.dateCheck('--'), now, displayErrorsOnly)
    now = testCheck('x26', 'False', str(x.isValid), now, displayErrorsOnly)
    now = testCheck('x27', '01-Sep-1963', str(x.dateCheck('01-09-63')), now, displayErrorsOnly)
    now = testCheck('chk2', '23-Sep-1963', str(chk.dateCheck('23-09-63')), now, displayErrorsOnly)
    now = testCheck('x28', '01-Sep-1963', x.formattedDate, now, displayErrorsOnly)

    deltaTime = (now - startTime)

    print('----------- Testing Ended ' + str(now.time()) + ' in ' + ("%.6f" % deltaTime.total_seconds()) + ' seconds -----------')

