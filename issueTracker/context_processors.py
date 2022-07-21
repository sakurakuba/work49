from issueTracker.forms import SearchForm


def search_processor(request):
    form = SearchForm(request.GET)
    return {"search_form": form}
