from typing import Any, Dict, Type
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Tareas, Preventa

from .asignacion_tareas import crear_tareas_usuario

# Login

class MiLoginView(LoginView):
    template_name = 'tareas/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self) -> str:
        return reverse_lazy('tareas')

class Registrarse(FormView):
    template_name = 'tareas/registrarse.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tareas')
    
    def form_valid(self, form: Any) -> HttpResponse:
        user = form.save()
        if user is not None:
            login(self.request,user)
            crear_tareas_usuario(user)
        return super(Registrarse, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tareas')
        return super(Registrarse,self).get(*args,**kwargs)   

# Create your views here.

class ListaTareas(LoginRequiredMixin, ListView):
    model = Tareas
    context_object_name = 'tareas'
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['tareas'] = context['tareas'].filter(user=self.request.user)
        context['cantidad'] = context['tareas'].filter(completo=False).count()
        return context
    
class ListaTareasPreventa(LoginRequiredMixin, ListView):
    model = Tareas    
    template_name = 'tareas/tareas_list.html'
    context_object_name = "tareas"
    
    def get_queryset(self) -> QuerySet[Any]:
        return Tareas.objects.filter(pv_id=self.kwargs['pk']).all()
    
class DetalleTareas(LoginRequiredMixin, DetailView):
    model = Tareas
    context_object_name = 'tareas'
    template_name = 'tareas/tarea.html'
    
class CrearTarea(LoginRequiredMixin, CreateView):
    model = Tareas
    fields = ['titulo','descripcion','completo']
    success_url = reverse_lazy('tareas')
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.user = self.request.user
        return super(CrearTarea, self).form_valid(form)
        
    
class ActualizarTarea(LoginRequiredMixin, UpdateView):
    model = Tareas
    fields = ['titulo','descripcion','adjunto','completo']
    success_url = reverse_lazy('tareas')
    
class EliminarTarea(LoginRequiredMixin, DeleteView):
    model = Tareas
    context_object_name = 'tarea'
    success_url = reverse_lazy('tareas')
    
# Crear Preventas

class ListaPreventas(LoginRequiredMixin,ListView):
    model = Preventa
    context_object_name = "preventas"
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['preventas'] = context['preventas'].filter(user=self.request.user)
        context['cantidad'] = context['preventas'].filter().count()
        return context
    

class CrearPreventa(LoginRequiredMixin, CreateView):
    model = Preventa
    context_object_name = 'preventa'
    fields = '__all__'
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        pv = form.save()
        if pv is not None:
            if pv.tipo_venta == 'C':
                tarea = Tareas.objects.create(user=pv.user,titulo ='Contado',descripcion='dniaca',pv=pv)
                tarea.save()
            else:
                tarea = Tareas.objects.create(user=pv.user,titulo ='Financiado',descripcion='dniaca',pv=pv)
                tarea.save()
            return redirect('tareas')
    
    