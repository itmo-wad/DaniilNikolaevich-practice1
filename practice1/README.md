# Prectice №1

## Launch postgresql
```
cd postgresql
docker-compose up -d
```

## Create tables in database
```
python3 database_setup.py
```

## Launch Flask
```
python3 main.py
```

##What have been done?
- ✅ User can sign up at ‘/signup’ 
- ✅ Login page at ‘/auth’ .If success, return a secret page to user. If not, give user a flash message about the error. 
- ✅ Store username, password in database 
- ✅ Form to upload image at ‘/upload’ 
- ✅ Save uploaded image to folder ‘upload’ on server side, allow only specified extensions 
- ✅ Redirect to ‘/uploaded/<filename>’ which shows the uploaded image 
- ✅ Return user back to ‘upload’ with flash error message if there would be any error 
- ✅ Implement notebook at ‘/notebook’ 
- ✅ Page have a form for submitting new note (text only)
- ✅ Store submitted notes in database 
- ✅ Display all saved notes below the form 
- ✅ User can delete all notes 
- ❌ User can limit the number of notes to be displayed in page
- ✅ Implement chat bot at ‘/chatbot’ 
- ✅ Chat with bot without refreshing page 
- ✅ Bot answer by simple rules 
- ✅ Save chat history in database so refreshing page won’t delete it 
- ✅ Allow user to clear chat history