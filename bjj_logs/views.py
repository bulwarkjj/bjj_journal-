from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy



def index(request):
    """The home page for bjj logs."""
    return render(request, 'bjj_logs/index.html')


@login_required
def topics(request):
    """Show all topics"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'bjj_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    """Show a single topic and all it's entries"""
    topic = get_object_or_404(Topic, id=topic_id)
    # Makes sure the topic belongs to the current user
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'bjj_logs/topic.html', context)


@login_required
def new_topic(request):
    """user adds a new topic"""
    if request.method != 'POST':
        # no data submitted; create a blank form
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            # associating new topic with current user
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect("bjj_logs:topics")

    # Display a blank or invaild form.
    context = {'form': form}
    return render(request, "bjj_logs/new_topic.html", context)


@login_required
def new_entry(request, topic_id):
    """user adds a new entry for a set topic"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # no data submitted; create a blank form
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect("bjj_logs:topic", topic_id=topic_id)

    # Display a blank or invaild form.
    context = {'topic': topic, 'form': form}
    return render(request, "bjj_logs/new_entry.html", context)


@login_required
def edit_entry(request, entry_id):
    """user edits an existing entry for a set topic"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    # protecting editing page from lateral topic URL access
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # no data submitted; create a blank form
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("bjj_logs:topic", topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, "bjj_logs/edit_entry.html", context)


@login_required
def delete_entry(request, entry_id):
  """Delete an existing entry"""
  entry = get_object_or_404(Entry, id=entry_id)  # getting the entry object the user wants to delete
    # topic=entry.topic
  entry.delete()  # Delete the entry
  context = {'entry': entry}  # I don't even think we need to pass this but I just want to be safe and pass something
  return render(request, 'bjj_logs/delete_entry.html', context)


@login_required
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    topic.delete()
    context = {'topic': topic}
    return render(request, 'bjj_logs/delete_topic.html', context)
