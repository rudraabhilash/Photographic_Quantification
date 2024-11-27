![image](https://github.com/user-attachments/assets/cb69620c-d93e-4adc-891f-75c0afe05314)


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


