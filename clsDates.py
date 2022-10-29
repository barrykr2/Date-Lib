# Written by Barry Kruyssen Oct 2022.
# Feel free to use as you like :-)
# This class check_Date is used for validaing a date, formatting and manipulating dates.
# It handles both DMY and MDY input/output formats.
#
# It also allows for short cut keys. (assuming Australian format - swap "d" and "m" for US date format)
#       "." use last date processed
#       ".." use last date processed plus 1 day
#       "--" use last date processed less 1 day
#       "d" will substitute the month day of the last date processed
#       "ddmm" will substitute the day and month of the last date processed
#       "d/m" will substitute the day and month of the last date processed
#       "ddmmyy" will substitute the expand to a date
#
# Please see the test cases at the bottom of the code for examples
#
# TODO:
#   - add error logging

from dateutil.parser import parse
from datetime import datetime, timedelta
from enum import Enum
import string

class EF(Enum):
    Day_Month_Year = 0
    Month_Day_Year = 1
    
nullDate = '1900-01-01'
defaultFullDate = "%Y-%m-%d"
defaultFormattedDate = ["%d-%b-%Y", "%b-%d-%Y"]

class check_date:
    def __init__(self, date, formatting = "", expectedInputFormat = EF.Day_Month_Year, allowShortCutKeys = False):
        # initialise all variables
        self.isValid = False
        self.expectedInputFormat = expectedInputFormat
        self.dateObj = datetime.strptime(nullDate, defaultFullDate)
        self.allowShortCutKeys = allowShortCutKeys
        self.setSelf(formatting)
        
        # validate date
        self.dateCheck(date, formatting)
        
    def setSelf(self, formatting = ""):
        formatting = self.setDefaultFormattedDate(formatting)
            
        self.day = self.dateObj.day
        self.month = self.dateObj.month
        self.year = self.dateObj.year
        self.fullDate = datetime.strftime(self.dateObj, defaultFullDate)
        self.formattedDate = self.dateObj.strftime(formatting)
        self.priorObj = self.dateObj

    def setDefaultFormattedDate(self, formatting = ""):
        if formatting == '':
            formatting = defaultFormattedDate[self.expectedInputFormat.value]
        return formatting

    def processShortCutKeys(self, date):
        # check if the date is using the prior date object to calc a new date
        if date == '.':                             # use prior date
            date = self.formattedDate
        elif date == '..':                          # prior date plus 1 day
            dateobj = self.priorObj + timedelta(1)
            date = dateobj.strftime(defaultFullDate)
        elif date == '--':                          # prior date less 1 day
            dateobj = self.priorObj + timedelta(-1)
            date = dateobj.strftime(defaultFullDate)

        # replace all date seperators with "-" for uniformity
        space_punct_dict = dict((ord(punct), '-') for punct in string.punctuation)
        tmpDate = date.translate(space_punct_dict)

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

    def dateCheck(self, date, formatting = ''):
        # Initialise date object
        self.dateObj = datetime.strptime(nullDate, defaultFullDate)
        
        if date:
            try:
                if self.allowShortCutKeys:
                    tmpDate = self.processShortCutKeys(date)
                else:
                    # replace all date seperators with "-" for uniformity
                    space_punct_dict = dict((ord(punct), '-') for punct in string.punctuation)
                    tmpDate = date.translate(space_punct_dict)

                dayFirst = False        # US format mm-dd-yyyy
                if self.expectedInputFormat == EF.Day_Month_Year:
                    dayFirst = True     # Australian format dd-mm-yyyy

                # get date object
                self.dateObj = parse(tmpDate, dayfirst = dayFirst)
                self.isValid = datetime.strftime(self.dateObj, defaultFullDate) != nullDate

                # only allow dates upto 5 years in the future
                if self.dateObj.year > datetime.today().year + 5:
                    tmpYear = self.dateObj.year - 100
                    self.dateObj = self.dateObj.replace(year = tmpYear)

                # reset variables
                self.setSelf(self.setDefaultFormattedDate(formatting))
            except Exception as e:
                self.isValid = False
                print(e)
                
        return self.formattedDate
    
    def formatDate(self, date = nullDate, formatting = ""):
        if date == nullDate:
            date = self.fullDate    # date hasn't changed so use current Object (faster when reusing date object)
        else:            
            self.dateCheck(date, formatting)    # check date passed in
        return self.formattedDate
        
    def addDay(self, numberOfDays = 1, formatting = "", date = nullDate):
        if date != nullDate:
            self.dateCheck(date, formatting)    # check date passed in

        dateobj = self.dateObj + timedelta(numberOfDays)
        self.dateCheck(dateobj.strftime(defaultFullDate), formatting)
        return self.formattedDate

if __name__ == "__main__":
    def testCheck(testId, expectedResult, restultReturned, displayErrorsOnly = True):
        isError = ''
        if expectedResult != restultReturned:
            isError = 'Error: '
            
        if (not displayErrorsOnly) or len(isError) > 0:
            print(isError + testId + ' - Expected "' + expectedResult + '": = ' + restultReturned)
            
    # Test code
    displayErrorsOnly = False
    chk = check_date(nullDate)
    testCheck('chk', 'False', str(chk.isValid), displayErrorsOnly)

    x = check_date('23-09-71')
    testCheck('x0', 'True', str(x.isValid), displayErrorsOnly)
    testCheck('x1', '1971-09-23', str(x.fullDate), displayErrorsOnly)
    testCheck('x2', '23', str(x.day), displayErrorsOnly)
    testCheck('x3', '23-Sep-1971', x.formattedDate)
    testCheck('x4', 'Feb-01-1960', str(x.formatDate('01/02/1960', '%b-%d-%Y')), displayErrorsOnly) # US formatted
    testCheck('x5', '1960-02-01', str(x.fullDate), displayErrorsOnly)      
    testCheck('x6', '1963 Sep 23', str(x.formatDate('1963-Sep-23', '%Y %b %d')), displayErrorsOnly)
    testCheck('x7', '1963-09-23', str(x.fullDate), displayErrorsOnly)
    x.expectedInputFormat = EF.Month_Day_Year
    testCheck('x8', '2022-Mar-01', x.formatDate('03/01/22', '%Y-%b-%d'), displayErrorsOnly)
    testCheck('x9', '2022-03-01', str(x.fullDate), displayErrorsOnly)      
    testCheck('x10', '2022-Mar-01', str(x.formattedDate), displayErrorsOnly)      
    testCheck('x11', 'Mar-02-2022', str(x.addDay(1,'%b-%d-%Y')), displayErrorsOnly)
    testCheck('x12', 'Apr-01-2022', str(x.addDay(30)), displayErrorsOnly)
    testCheck('x13', 'Apr-02-2022', str(x.addDay()), displayErrorsOnly)
    testCheck('x14', 'Dec-17-2022', str(x.formatDate('17 Dec 2022')), displayErrorsOnly)
    testCheck('x15', 'Jan-02-1960', x.dateCheck('01/02/1960'), displayErrorsOnly)
    x.allowShortCutKeys = True
    testCheck('x16', 'Jan-02-1960', x.dateCheck('.'), displayErrorsOnly)
    testCheck('x17', 'Jan-03-1960', x.dateCheck('..'), displayErrorsOnly)
    testCheck('x18', 'Jan-02-1960', x.dateCheck('--'), displayErrorsOnly)
    testCheck('x19', 'Sep-23-1963', x.dateCheck('092363'), displayErrorsOnly)
    testCheck('x20', 'Sep-23-1963', x.dateCheck('09/23'), displayErrorsOnly)
    testCheck('x21', 'Sep-23-1963', x.dateCheck('0923'), displayErrorsOnly)
    testCheck('x22', 'Apr-05-1963', x.dateCheck('4/5'), displayErrorsOnly)
    testCheck('x23', 'Apr-11-1963', x.dateCheck('11'), displayErrorsOnly)
    x.expectedInputFormat = EF.Day_Month_Year
    testCheck('x23', '03-Apr-1963', x.dateCheck('3'), displayErrorsOnly)
