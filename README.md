# Python_Api_Project

Python project takes exchange rates of the different currencies from web api thru users input, compares them with yesterday rate, prints them out and stores them into postgres database.
Api-key is beiing obtained from text file.
If the current rate is high than the previous day the output and data stored in the database will be printed green, otherwise in case of lower rate the data will be printed RED.
Scpript will prompt the user to input currencies until he types 'quit' which will close the app, or 'history' which will print out the whole postgres database.
In case of wrong input, app will print out 'Wrong input' and will prompt the user for input again.
