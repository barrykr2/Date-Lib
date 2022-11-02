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
