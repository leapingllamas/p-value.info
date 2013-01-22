#Description

A simple joke generator in python using homonyms. 

It works as follows:

* Downloaded honomym list from [http://www.cooper.com/alan/homonym_list.html](http://www.cooper.com/alan/homonym_list.html) and saved as homonym_list.html
* Parse HTML with ***python extract_homonyms.py > processed_homonyms.txt*** to extract plain text file
* run ***python generate_jokes.py > jokes.txt*** to generate jokes
