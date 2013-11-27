from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from models import *

# Home section
def home_page(request):
    return render_to_response('index.html')

# About section
def venue_page(request):
    return render_to_response('venue.html')

def reaching_venue_page(request):
    return render_to_response('reaching_venue.html')

def contact_page(request):
    return render_to_response('contact.html')

# Call for papers
def call_for_papers_page(request):
    status = ''
    if 'status' in request.GET:
        status = request.GET['status']

    if request.user.is_anonymous():
        current_user = "anonymous"
    else:
        current_user = request.user

    context = {
      'status': status,
      'current_user': current_user
    }
    return render_to_response('papers.html', context)

# Conference Section
def schedule_page(request):
    return render_to_response('schedule.html')

def invited_speakers_page(request):
    return render_to_response('invited_speakers.html')

def list_of_abstracts(request):
    context = {}
    papers = Paper.objects.all()
    context['papers'] = papers
    return render_to_response('list_abstracts.html', context)
    
def abstract_details(request, paper_id=None):
    user = request.user
    reviewers = ['jaidevd', 'prabhu', 'jarrod']
    context = {}
    paper = Paper.objects.get(id=paper_id)
    comments = Comment.objects.filter(paper=paper)
    if(len(str(paper.attachments))<=0):
        attachment = False
    else:
        attachment = True
    if user.username in reviewers:
        context['reviewer'] = True
    context['paper'] = paper
    context['comments'] = comments
    context['attachment'] = attachment
    context['current_user'] = user
    context.update(csrf(request))
    if request.method == 'POST':
        user_comment = request.POST['comment']
        new_comment = Comment()
        new_comment.paper = paper
        new_comment.comment_by = user
        new_comment.comment = user_comment.replace('\n', '<br>')
        new_comment.save()
        return HttpResponseRedirect('/2013/abstract-details/'+paper_id, context)
    else:
        return render_to_response('abstract_details.html', context)


def accepted_abstracts_page(request):
    return render_to_response('accepted_abstracts.html')

# Register
def register_page(request):
    return render_to_response('register_2013.html')

# Sponsors
def sponsors_page(request):
    return render_to_response('sponsors.html')
