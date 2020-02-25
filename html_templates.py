from conversations import get_chat_title,exist_user

def profile(username):
    chats = [get_chat_title(chat_id) for chat_id in exist_user(username)['chats']]
    buttons = ""
    for chat in chats:
        buttons += """<form action="/user/{username}/chat/{chat}">
        <input type="submit" value={chat}  style="background-color:#6495ED;padding:10px;margin:5px"/>
        </form>""".format(chat=chat, username=username)
    return """
            <html style="height:100%">
                <body style="text-align: center; border:solid; height:80%;margin:50px;">
                    <div style="margin:5%;vertical-align:middle">
                        <h1>Welcome back {username}</h1>
                        <form action="/{username}/newchat" method="post">
                                    Chat name: <input type="text" name="chat_title">
                                    <input type="submit" name= "form" value="Create" style="background-color:pink;padding:10px"/>
                        </form>
                        <form action="/user/{username}/recommend">
                            <input type="submit" value='Get recommendation' style="background-color:#D8BFD8;padding:10px" />
                        </form>
                        <p style = "font:bold">
                            Your conversations:
                        <div style = "display:flex; justify-content:center">
                            {buttons}
                        </div>
                        </p>
                        <form action="/">
                            <input type="submit" value="Home" style = "background-color:pink;padding:10px;margin:5px"/>
                        </form>
                    </div>
                </body>
            </html>
            """.format(username=username, buttons=buttons )

def conversation(message, username, chat_title):
    return """
        <html style="height:100%">
                <body style="text-align: center; border:solid; height:80%;margin:50px;">
                    <div style="margin:5%;vertical-align:top">
                        <h2>{chat}</h2>
                        <ul style="padding:0px">{messages}</ul>
                        <form action="/user/{username}/chat/{chat}" method="post">
                                        New message: <input type="text" name="new_message">
                                        <input type="submit" name= "form" value="Send" style = "background-color:pink;padding:10px"/>
                        </form>
                        <form action="/user/{username}/chat/{chat}" method="post">
                                        Add user: <input type="text" name="new_user">
                                        <input type="submit" name= "form" value="Invite" style = "background-color:pink;padding:10px"/>
                        </form>
                        <form action="/chat/{chat}/sentiment">
                            <input type="submit" value="Get sentiment" style = "background-color:pink;padding:10px"/>
                        </form>
                        <form action="/">
                            <input type="submit" value="Home" style = "background-color:pink;padding:10px"/>
                        </form>
                    </div>
                </body>
        </html>
        
    """.format(messages=message,username=username,chat=chat_title)