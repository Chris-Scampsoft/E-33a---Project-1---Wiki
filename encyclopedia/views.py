from django.shortcuts import render, redirect
from . import util
import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": markdown2.markdown(content)  # This converts the Markdown to HTML
        })
    else:
        return render(request, "encyclopedia/error.html", {"message": "Page not found."})

def search(request):
    query = request.GET.get("q", "").strip().lower()
    entries = util.list_entries()

    for entry in entries:
        if entry.lower() == query:
            return redirect("entry", title=entry)  # Redirect to the exact entry page

    # Find partial matches
    results = [entry for entry in entries if query in entry.lower()]

    return render(request, "encyclopedia/search_results.html", {
        "results": results,
        "query": query
    })