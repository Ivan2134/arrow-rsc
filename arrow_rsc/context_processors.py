# myapp/context_processors.py

from info_pages.models import LegalDocument

def legal_docs(request):
    legals = LegalDocument.objects.all()
    return {'legals': legals}
