from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime

class Chat:
    def __init__(self):
        self.messages = []
    def add(self,message):
        self.messages.append(message)
    def get_last_100_messages(self):
        self.messages.sort(key=lambda x: x.timestamp, reverse=True)
        return self.messages[:99]
    def get_messages_of_page(self, n):
        self.messages.sort(key=lambda x: x.timestamp, reverse=True)
        return self.messages[5*n:5*(n+1)]

class Message:
    def __init__(self, body, author):
        self.body = body
        self.timestamp = datetime.now()
        self.author = author
chat = Chat()

# for i in range(120):
#     message1 = Message("blablabalbal", "pancho{}".format(i))
#     chat.add(message1)


# Create your views here.
def index(request):
    if request.method == "GET":
        if not request.session.get("alias"):
            # No Alias
            return render(request, "input_alias.html")
        else:
            return redirect('send_message')
    elif request.method == "POST":
        print(request.POST.get("alias",""))
        alias = request.POST.get("alias","")
        request.session["alias"] = alias
        return redirect('send_message')

def send_message(request):
    alias = request.session.get("alias")
    if not alias:
        return redirect("") # Back to home
    else:
        if request.method == "GET":
            data = {"alias": alias}
            return render(request, "send_message.html",data)

        elif request.method == "POST":
            body = request.POST.get("body","")
            author = alias
            message = Message(body, author)
            chat.add(message)
            return redirect("messages",0)

def messages(request, page):
    alias = request.session.get("alias")
    if not alias:
        return redirect("") # Back to home
    else:
        if request.method == "GET":
            if page < min(19,(len(chat.get_last_100_messages())-1)//5):
                next_page_num = page + 1
            else:
                next_page_num = min(19,(len(chat.get_last_100_messages())-1)//5)
            if page <= 0:
                prev_page_num = 0
            else:
                prev_page_num = page - 1


            data = {"alias": alias,
                    "messages": chat.get_messages_of_page(page),
                    "next_page_num": next_page_num,
                    "prev_page_num": prev_page_num,
                    }
                    ### Meter current page
            return render(request, "messages.html",data)
