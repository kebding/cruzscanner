# cruzscanner

This repository provides a system for Teaching Assistants to easily manage
large classes of students by automating the attendance check process. When
a student ID card's barcode is scanned, the system automatically logs the 
ID number in a database.

When scanning ID cards to confirm that students turned in their exams, it 
automatically sends the student an email confirming that their exam was 
received. 

When taking attendance in TA discussion sections, the system also records the
section number (e.g. 01B) as well as what week of the quarter/semester it is.
This proved useful to us (the creators) because the professor of our class 
gives extra credit for attending discussion sections regularly, but students 
can only get the extra credit for one attendance per week. Including the 
section number helps to handle duplicate entries, such as when a student
accidentally scans their card twice (or intentionally scans multiple times
hoping to rack up attendances for the extra credit). 

In order to facilitate sending emails to students confirming that their exam
was received, a class roster must first be uploaded to the server. Currently,
the system supports uploading a CSV file only. 

The server can be run locally or it can be hosted externally. The choice is up
to the users, but note that the database is always stored with the server.


DEPENDENCIES:
-Python libraries:
    -Flask
    -Pandas
    -sqlite3
    -email.mime.multipart
    -email.mime.text
    -smtplib
-SQLite3
