from django.shortcuts import render, redirect , get_object_or_404
from .forms import GifForm, CategoryForm
from .models import Gif, Category

def homepage(request):
    gifs = Gif.objects.all()
    return render(request, 'homepage.html', {'gifs': gifs})

def add_gif(request):
    if request.method == 'POST':
        form = GifForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = GifForm()
    return render(request, 'add_gif.html', {'form': form})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = CategoryForm()
    return render(request, 'add_category.html', {'form': form})

def category(request, category_id):
    category = Category.objects.get(id=category_id)
    gifs = Gif.objects.filter(categories=category)
    return render(request, 'category.html', {'category': category, 'gifs': gifs})

def categories(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})

def gif(request, gif_id):
    gif = Gif.objects.get(id=gif_id)
    return render(request, 'gif.html', {'gif': gif})
