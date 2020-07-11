from django.core import serializers
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Count
from .forms import GrupoForm, MusicoForm, AlbumForm
from .models import Grupo, Musico, Album

# Create your views here.

def index(request):
    context = {}
    return render(request,'práctica_05/index.html', context)

def test_template(request):
    context = {}   # Aquí van la las variables para la plantilla
    return render(request,'test.html', context)

def grupo_lista(request):
    return render(request, 'práctica_05/grupos.html')

def musico_lista(request):
    return render(request, 'práctica_05/musicos.html')

def album_lista(request):
    return render(request, 'práctica_05/albumes.html')

def grupo_datos(request):
    grupos = Grupo.objects.filter(creacion__lte=timezone.now()).order_by('creacion')
    paginator = Paginator(grupos, 3)

    pagina = request.GET.get('pagina')
    grupos = paginator.get_page(pagina)

    grupos_html = loader.render_to_string(
        'práctica_05/grupos_tabla.html',
        {'grupos': grupos}
    )
    datos = {
        'grupos_html':grupos_html,
        'has_next': grupos.has_next(),
        'has_previous': grupos.has_previous(),
        'page': grupos.number,
        'num_pages': paginator.num_pages,
    }

    return JsonResponse(datos)

def musico_datos(request):
    musicos = Musico.objects.filter(creacion__lte=timezone.now()).order_by('creacion')
    paginator = Paginator(musicos, 3)

    pagina = request.GET.get('pagina')
    musicos = paginator.get_page(pagina)

    musicos_html = loader.render_to_string(
        'práctica_05/musicos_tabla.html',
        {'musicos': musicos}
    )
    datos = {
        'musicos_html':musicos_html,
        'has_next': musicos.has_next(),
        'has_previous': musicos.has_previous(),
        'page': musicos.number,
        'num_pages': paginator.num_pages,
    }

    return JsonResponse(datos)

def album_datos(request):
    albumes = Album.objects.filter(creacion__lte=timezone.now()).order_by('creacion')
    paginator = Paginator(albumes, 3)

    pagina = request.GET.get('pagina')
    albumes = paginator.get_page(pagina)

    albumes_html = loader.render_to_string(
        'práctica_05/albumes_tabla.html',
        {'albumes': albumes}
    )
    datos = {
        'albumes_html':albumes_html,
        'has_next': albumes.has_next(),
        'has_previous': albumes.has_previous(),
        'page': albumes.number,
        'num_pages': paginator.num_pages,
    }

    return JsonResponse(datos)

def grupo_nuevo(request):
    if request.method == "POST":
        form = GrupoForm(request.POST)
        if form.is_valid():
            grupo = form.save(commit=False)
            grupo.save()
            return redirect('grupo_lista')
    else:
        form = GrupoForm()
    return render(request, 'práctica_05/nuevo.html', {'form': form})

def musico_nuevo(request):
    if request.method == "POST":
        form = MusicoForm(request.POST)
        if form.is_valid():
            musico = form.save(commit=False)
            musico.save()
            return redirect('musico_lista')
    else:
        form = MusicoForm()
    return render(request, 'práctica_05/nuevo.html', {'form': form})

def album_nuevo(request):
    if request.method == "POST":
        form = AlbumForm(request.POST)
        if form.is_valid():
            album = form.save(commit=False)
            album.save()
            return redirect('album_lista')
    else:
        form = AlbumForm()
    return render(request, 'práctica_05/nuevo.html', {'form': form})

def grupo_editar(request, pk):
    grupo = get_object_or_404(Grupo, pk=pk)
    if request.method == "POST":
        form = GrupoForm(request.POST, instance=grupo)
        if form.is_valid():
            grupo = form.save(commit=False)
            grupo.creacion = timezone.now()
            grupo.save()
            return redirect('grupo_lista')
    else:
        form = GrupoForm(instance=grupo)
    return render(request, 'práctica_05/editar.html', {'form': form})

def grupo_borrar(request, pk):
    grupo = get_object_or_404(Grupo, pk=pk)
    grupo.delete()
    return redirect('grupo_lista')

def musico_editar(request, pk):
    musico = get_object_or_404(Musico, pk=pk)
    if request.method == "POST":
        form = MusicoForm(request.POST, instance=musico)
        if form.is_valid():
            musico = form.save(commit=False)
            musico.creacion = timezone.now()
            musico.save()
            return redirect('musico_lista')
    else:
        form = MusicoForm(instance=musico)
    return render(request, 'práctica_05/editar.html', {'form': form})

def musico_borrar(request, pk):
    musico = get_object_or_404(Musico, pk=pk)
    musico.delete()
    return redirect('musico_lista')

def album_editar(request, pk):
    album = get_object_or_404(Album, pk=pk)
    if request.method == "POST":
        form = AlbumForm(request.POST, instance=album)
        if form.is_valid():
            album = form.save(commit=False)
            album.creacion = timezone.now()
            album.save()
            return redirect('album_lista')
    else:
        form = AlbumForm(instance=album)
    return render(request, 'práctica_05/editar.html', {'form': form})

def album_borrar(request, pk):
    album = get_object_or_404(Album, pk=pk)
    album.delete()
    return redirect('album_lista')

def estadisticas(request):
    sitios_grupos = Grupo.objects.values_list('nombre', 'origen', named=True)

    instrumentos = {
      v['instrumento']: v['instrumento__count']
      for v in
      Musico.objects.values('instrumento').annotate(Count('instrumento')).order_by('instrumento')
    }

    generos = {
      v['genero']: v['genero__count']
      for v in
      Grupo.objects.values('genero').annotate(Count('genero')).order_by('genero')
    }

    return render(request, 'práctica_05/estadisticas.html', {'sitios_grupos': sitios_grupos, 'instrumentos': instrumentos, 'generos': generos})