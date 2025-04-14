![image](https://github.com/user-attachments/assets/d134424e-51d5-4f01-a4b1-d7b5f82a3f20)![image](https://github.com/user-attachments/assets/27929e59-6f02-406b-b1af-a198b9f4ad64)






![image](https://github.com/user-attachments/assets/8d5192aa-7a60-4f0b-9e34-ef117039430b)






![image](https://github.com/user-attachments/assets/cb69620c-d93e-4adc-891f-75c0afe05314)





![image](https://github.com/user-attachments/assets/3206d8c1-e52a-4ed7-9f97-f6349d7ffe7d)





![image](https://github.com/user-attachments/assets/1d5a69f9-b40e-46cd-b747-e9008ad22c18)




![image](https://github.com/user-attachments/assets/e68cb387-06d9-4163-9915-7f4bcf608746)




![image](https://github.com/user-attachments/assets/a275814f-a53e-48dc-b2ec-6f0099f0d657)




![image](https://github.com/user-attachments/assets/c779a562-7d70-4cab-859b-f03e2f4d565c)




![image](https://github.com/user-attachments/assets/0d93b598-33ca-4390-82ab-3a7e3a90778f)
















# Photographic_Quantification

We are using Django build a web application



Commands for project - 
1. Inside this Photographic_Quantification git project, create virtual environment and activate it.
2. **Instat Django library by command -> py -m pip install Django**
3. **Create Django project by command, it will create Django project folder named as my_tennis_club -> django-admin startproject my_tennis_club**
4. **py manage.py runserver -> it will start the Django server(DO NOT enter inside default app but enter inside Django project folder)**
5. **py manage.py startapp users -> it will create 'users' application.**
6. Create views.py and urls.py
7. **default app url(administrative office) -> specific app url(dept. office) -> corresponding views -> html**
8. All the app names should be registered in settings.py file inside default app and whenever you are changing this settings.py file then run command -> py manage.py migrate
9. Database - create models.py file inside an app and run these two commands at shell(py manage.py shell) to create table! Two commands are as follows- i) py manage.py makemigrations users, ii) py manage.py migrate NOTE - Whenever you change models.py file, you have to run these two commands.
10. If you want to see sqlstatement of particular migration then please run this command at shell(py manage.py shell) - py manage.py sqlmigrate users 0001
11. We can do CRUD operation from python shell(py manage.py shell) itself.
12. Install sqlite extension to do CRUD operation from extension in a very beautiful way.
13. Now do read operation via view function.
14. Now do write operation via view function.

15. Deployment steps -
	a. py -m pip freeze > requirements.txt

	b. Create .ebextensions folder and django.config file inside this folder.
	      option_settings:aws:elasticbeanstalk:container:python:
	      WSGIPath:hospital_project.wsgi:application

 
	c. Change allowed hosts to ['*'] in default settings.py file in default app

 	d. Make zip file of all apps including default app and manage.py and requirements.txt file
	
 	e. Use AWS elastic beanstalk - 
	            Application name - hospital_project
    
	            Platform - Python

	            Application code - Upload your code

                    Source code origin - Local file

    	            Click on create application(Do change GP3 first! This is Oct24 change by aws team. It is there inside Configuration option of environment and    inside "Instance traffic and scaling" option, you have to select Root volume type - general purpose 3(SSD))


DSA - 

https://github.com/dipjul/Grokking-the-Coding-Interview-Patterns-for-Coding-Questions

https://www.educative.io/blog/array-interview-questions - Array

https://www.educative.io/courses/grokking-coding-interview/solution-generate-parentheses - DP

https://gist.github.com/tykurtz/3548a31f673588c05c89f9ca42067bc4

https://github.com/navidre/new_grokking_to_leetcode

https://leetcode.com/discuss/post/3972722/top-greedy-questions-helpful-for-oa-and-17zbd/ - greedy

https://realpython.com/tutorials/django/ - Django 



System design - 
https://github.com/ByteByteGoHq/system-design-101?tab=readme-ov-file

https://github.com/karanpratapsingh/system-design?tab=readme-ov-file#whatsapp

https://github.com/topics/system-design-interview

https://medium.com/javarevisited/10-best-github-repositories-to-prepare-for-system-design-interviews-6cc9d37d50f6


AI, ML - 

https://www.w3schools.com/python/python_ml_getting_started.asp

https://www.kaggle.com/code/kanncaa1/machine-learning-tutorial-for-beginners/notebook

https://www.kaggle.com/code/kanncaa1/data-sciencetutorial-for-beginners

https://www.kaggle.com/code/kanncaa1/machine-learning-tutorial-for-beginners/notebook

https://www.kaggle.com/code/kanncaa1/statistical-learning-tutorial-for-beginners?scriptVersionId=5598734

https://www.kaggle.com/code/kanncaa1/deep-learning-tutorial-for-beginners

https://www.kaggle.com/learn

https://www.kaggle.com/learn/intro-to-machine-learning

https://www.kaggle.com/learn-guide/5-day-genai

http://neuralnetworksanddeeplearning.com/index.html

https://www.3blue1brown.com/topics/neural-networks

https://github.com/donnemartin/data-science-ipython-notebooks/blob/master/kaggle/titanic.ipynb

https://github.com/browser-use/browser-use

https://huggingface.co/vasista22/whisper-hindi-small

https://medium.com/@kharatmoljagdish/using-openai-whisper-python-library-for-speech-to-text-dda4f558fccc

https://www.kaggle.com/code/harshgupta2003/openai-whisper-automated-speech-recognition-hindi

https://www.datacamp.com/blog/top-ai-frameworks-and-libraries

https://www.youtube.com/watch?v=wjZofJX0v4M&list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi&index=10

https://huggingface.co/learn

https://huggingface.co/learn/audio-course/chapter0/introduction

https://huggingface.co/blog?p=0

https://www.youtube.com/live/iLVyYDbdSmM

https://www.datacamp.com/tutorial/mistral-7b-tutorial

https://www.datacamp.com/blog/best-open-source-text-to-speech-tts-engines







