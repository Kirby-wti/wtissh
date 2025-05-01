# WTI SSH - Random command test

This is a "Hello World" Python on how to talk to WTI devices with an SSH session.

This `SSH script` Python script will work on any modern WTI device, the commands being used are universal on all WTI OOB and PDU type devices making it the perfect starting point to start learning and experimenting with the SSH CLI interface

# To Configure Python Script:

Required: 
paramiko is required, issue `pip install paramiko` if not done already

Have a text file in same directory as this program named  `terminal_devices.txt` with all devices to test, formatted like this:

192.168.0.1 username password  
192.168.0.2 username password


Run the program from CLI and select y to save the file, a log file will be saved in an outputs folder, created automatically in the current directory.

Program runs at a rate of about 10 seconds per address, changing that will likely result in failed output. 

For large groups of devices, ensure the readme is updating with data as the program runs. 


# To Run with Python:
`python wtissh.py`


# Contact US
If you have any questions, comments or suggestions you can email us at kirbyb@wti.com

# About Us
WTI - Western Telematic, Inc.
5 Sterling, Irvine, California 92618

Western Telematic Inc. was founded in 1964 and is an industry leader in designing and manufacturing power management and remote console management solutions for data centers and global network locations. 
Our extensive product line includes Intelligent PDUs for remote power distribution, metering, reporting and control, Serial Console Servers, RJ45 A/B Fallback Switches and Automatic Power Transfer Switches.


