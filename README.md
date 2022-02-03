# PyBuster

Welcome to PyBuster 1.0 -- More features to come, initial release.

PyBuster is a directory busting tool that allows not only a word list to be specified but whole extension list too.

It will check every given word in a word list to every given extension in an extension list. For example:

wordlist > 

Hello

goodbye

howdy

extensionlist >

.exe

.html

.php

Will run: 

http://givenhost:givenport/Hello.exe

http://givenhost:givenport/Hello.html

http://givenhost:givenport/Hello.php

http://givenhost:givenport/goodbye.exe

http://givenhost:givenport/goodbye.html

http://givenhost:givenport/goodbye.php

http://givenhost:givenport/howdy.exe

http://givenhost:givenport/howdy.html

http://givenhost:givenport/howdy.php

It also returns http codes along side found URLs.

Use of paths should be in the format "/dir/dir/wordlist.txt" for Linux and "dir\dir\dir\wordlist.txt" for Windows users.

Put word lists and extension lists in lib\lists folder for ease of use.

###Created by Tyses96###
