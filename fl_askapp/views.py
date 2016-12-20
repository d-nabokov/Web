from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from fl_askapp import models
from fl_askapp import paginator_foo
import random



questions = []
answers = []
tags = []
for i in range (1,4):
	tags.append({
		"tag" : "SomeTag"})
for i in range (1,300):
	questions.append({
		"title" : "Question Title",
		"text" : "Lorem Ipsum is simply dummy text of the printing and typesetting industry.\
			Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,\
			when an unknown printer took a galley of type and scrambled it to make a type\
			specimen book. It has survived not only five centuries, but also the leap into\
			electronic typesetting, remaining essentially unchanged. It was popularised in\
			the 1960s with the release of Letraset sheets containing Lorem Ipsum passages,\
			and more recently with desktop publishing software like Aldus PageMaker\
			including versions of Lorem Ipsum.",
		"id" : i,
		"user_rating" : random.randint(-100,100),
		"user_name" : "SomeUser",
		"question_rating" : random.randint(-100,100),
		"tags" : tags
		})
	answers.append({
		"text" : "Lorem, ipsum orci nam diam porta justo porttitor ornare massa - elementum,\
			sit a at. Sem, ligula sem pellentesque leo, sodales sed fusce molestie massa a\
			 commodo ligula tempus  ipsum, in sapien amet ornare rutrum amet tempus ligula\
			 curabitur - pellentesque. Justo ut arcu adipiscing eros vitae, diam, sit gravida,\
			 massa a ornare rutrum sem eget duis quisque vivamus. Nec pellentesque ligula, nibh\
			 ipsum quisque sit leo duis sapien ut. Eros leo sit diam eros quam massa diam congue\
			 lectus eros. Maecenas lorem nulla integer risus mattis odio sodales sem congue magna\
			 at duis sem sit mauris, justo, nam lorem lectus. ",
		"user_name" : "AnotherUser",
		"user_rating" : random.randint(-100,100),
		"answer_rating" : random.randint(-100,100)
		})

		


def index(request, page = '1'):
	user = { "user_is_logged" : False}	
	question_list = paginator_foo.pagination(questions, 5, page)
	question_list.paginator.baseurl = "/"
	return render(request, 'index.html', {"questions": question_list, "user" : user}, )

def hot_questions(request, page = '1'):
	user = { "user_is_logged" : True}
	question_list = paginator_foo.pagination(questions, 5, page)
	question_list.paginator.baseurl = "/hot/"
	return render(request, 'hot_questions.html', {"questions": question_list, "user" : user}, )

def profile(request, user_name, page = '1'):
	user = ({ 
		"user_is_logged" : True,
		"info" : "Lorem, ipsum orci nam diam porta justo porttitor ornare massa - elementum,\
			sit a at. Sem, ligula sem pellentesque leo, sodales sed fusce molestie massa a\
			 commodo ligula tempus  ipsum",
		"name" : user_name,	
		"rating" : random.randint(-100,100)
		})
	question_list = paginator_foo.pagination(questions, 5, page)
	question_list.paginator.baseurl = "/profile/" + user["name"] + "/"
	return render(request, 'profile.html', {"questions": question_list, "user" : user}, )

def tag(request, tag, page = '1'):	
	user = { "user_is_logged" : True}
	question_list = paginator_foo.pagination(questions, 5, page)
	question_list.paginator.baseurl = "/tag/" + tag + "/"				
	return render(request, 'tag.html', {"questions": question_list, "user" : user, "tag" : tag}, )

def single_question(request, id, page = '1'):
	user = { "user_is_logged" : True}	
	answer_list = paginator_foo.pagination(answers, 4, page)
	answer_list.paginator.baseurl = "/question/id" + id + "/"
	return render(request, 'question.html', {"question": questions[0], "answers" : answer_list, "user" : user},)

def developing(request):
	user = { "user_is_logged" : True}	
	return render(request, 'developing.html', {"user" : user},)

def ask_question(request):
	user = { "user_is_logged" : True}	
	return render(request, 'ask.html', {"user" : user},)

def login(request):
	user = { "user_is_logged" : False}
	return render(request, 'login.html', {"user" : user},)

def signup(request):
	user = { "user_is_logged" : False}
	return render(request, 'signup.html', {"user" : user},)

@csrf_exempt
def get_prms(request):
    response = "<p> GET/POST </p>" \
               "<form method='POST'>"\
               "<p><input type='text' name='text'></p>" \
               "<p><input type='submit' value='Send!'></p>" \
               "</form>"
    if request.method == 'GET':
        if request.GET:
            response += "<h3> <p> Get data: </p> </h3>"
            for key,value in request.GET.iteritems():
                if len(value) == 1:
                    response += "%s = %s <br>" % (key, value[0])
                else:
                    response += "%s = %s <br>" % (key, value)
    elif request.method == 'POST':
        response += "<h3> <p> Post data: </p> </h3>"
        response += "Value = %s <br>" % (request.POST.get('text'))
    return HttpResponse(response, content_type="text/html", status=200)
