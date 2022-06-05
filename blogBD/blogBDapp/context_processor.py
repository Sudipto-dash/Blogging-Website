#send data/access globaly to any template
from matplotlib.style import context
from .models import Category
def getallcategories(request):
    categories = Category.objects.all()
    context = {
        "categories": categories
    }
    return context