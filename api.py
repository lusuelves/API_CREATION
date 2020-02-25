from flask import Flask,request,render_template
from createUser import createUser, recommend
from conversations import createChat, add_user, add_message, get_sentiments_from_chat, get_conversation,exist_user        
from html_templates import profile, conversation
app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('homepage.html')

@app.route('/user/create')
def index():
    return render_template('test.html')

@app.route('/user/login')
def login():
        return render_template('login.html')

@app.route('/chat/<chat_title>/sentiment')
def getSentimentsFromChat(chat_title):
    return get_sentiments_from_chat(chat_title)

@app.route('/user/<username>/recommend')
def getRecommendation(username):
    return recommend(username)

@app.route('/who', methods=['POST'] )
def who():
    first_name = request.form['first_name']
    if createUser(first_name):
        return render_template('homepage.html')
    elif exist_user(first_name):
        return  profile(first_name)
    else:
        return '<h2>Username already exists</h2>'
    
@app.route('/user/<username>/chat/<chat_title>', methods=['POST','GET'])
def print_chats(username,chat_title):
    messages = get_conversation(chat_title)
    message = ''
    for mess in messages[-10:]:
        message += '<li style="list-style:none">'+mess +'</li>'
    if request.form:
        try:
            new_message = request.form['new_message']
            add_message(chat_title,username, new_message)
        except:
            new_user = request.form['new_user']
            add_user(chat_title, new_user)

    return conversation(message, username, chat_title)


@app.route('/<username>/newchat', methods=['POST'] )
def newchat(username):
    chat_title = request.form['chat_title']
    return createChat(chat_title,username)

app.run("0.0.0.0", 5000, debug=True)