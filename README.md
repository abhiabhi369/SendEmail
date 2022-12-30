When you run SendEmail.py it asks for csv file path,
Give path of file to the input
ReadCsv is the function which takes path as input, reads the file by each row
ReadCsv use dateFormate function which formate the date as required
Now ReadCsv will checks for the Schedule On date and if the date is not in future then it wil valid the email first from "is_valid" function
If the email is valid then ReadCsv triggers "sendEmail" function along with email and text as parameters.
If the email is not valid then it writes into test.txt and trigger "sendText" function
sendText function will uses txtbox api to trigger SMS to the given Phone number 
sendText function will also validates the time if the current time is in between 10am to 5pm then only it will trigger SMS and writes the status of sms to the test.txt
sendEmail function will send the message to the given email by using smtp server.
Note: sendEmail uses email id of admin and app password of admin email, not regular login password
If email sent failed then it writes into test.txt file
If got success then it writes success of that email into test.txt.
