from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2

from django.shortcuts import redirect, render

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    # Get the content of the encyclopedia entry
    entry_content = util.get_entry(title)
    
    if entry_content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })
    
    # Convert Markdown to HTML
    entry_html = markdown2.markdown(entry_content)
    
    # Render the entry page with the converted HTML content
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": entry_html
    })

def search(request):
    query = request.GET.get('q', '')
    entries = util.list_entries()

    if query in entries:
        # If the exact match is found, redirect to that entry's page
        return redirect('encyclopedia:entry', title=query)

    # If no exact match, find all entries that contain the query as a substring
    matching_entries = [entry for entry in entries if query.lower() in entry.lower()]

    # Render the search results page
    return render(request, "encyclopedia/search_results.html", {
        "query": query,
        "entries": matching_entries
    })

def create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        # Check if an entry with the same title already exists
        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/create.html", {
                "error": "An encyclopedia entry with this title already exists.",
                "title": title,
                "content": content
            })

        # Save the new entry
        util.save_entry(title, content)
        
        # Redirect to the new entry page
        return redirect('encyclopedia:entry', title=title)

    return render(request, "encyclopedia/create.html")

def edit(request, title):
    # Get the current content of the entry
    entry_content = util.get_entry(title)
    
    if request.method == "POST":
        content = request.POST.get("content")

        # Save the edited entry
        util.save_entry(title, content)
        
        # Redirect to the entry page after saving
        return redirect("encyclopedia:entry", title=title)

    # Render the edit page with pre-populated content
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": entry_content
    })