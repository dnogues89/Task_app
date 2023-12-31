from typing import Any, Dict, Type
import os
from django.http import HttpRequest, HttpResponse
from django.conf import settings

from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login

from .models import Tareas, Preventa, User

from . import asignacion_tareas

from django.views.decorators.csrf import csrf_exempt

#Descargar archivos
def download_file(request, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, 'archivos_para_descargar', file_name)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
    else:
        return HttpResponse('Archivo no encontrado.', status=404)

# Login

class MiLoginView(LoginView):
    template_name = 'tareas/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def form_valid(self, form: AuthenticationForm) -> HttpResponse:
        user = User.objects.get(username = form.data['username'])
        self.last_login = user.last_login
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        if self.last_login == None:
            return reverse_lazy('password')
        return reverse_lazy('home')

class MiPasswordResetView(PasswordResetView):
    template_name = 'tareas/password_reset_form.html'

class MiPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'tareas/password_reset_done.html'
    
class MiPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'tareas/password_reset_confirm.html'

class MiPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'tareas/password_reset_complete.html'

class Registrarse(FormView):
    template_name = 'tareas/registrarse.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')
    
    def form_valid(self, form: Any) -> HttpResponse:
        user = form.save()
        if user is not None:
            login(self.request,user)
            asignacion_tareas.crear_tareas_usuario(user)
        return super(Registrarse, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
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

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['tareas'] = context['tareas'].filter(user=self.request.user)
        context['cantidad'] = context['tareas'].filter(completo=False).count()
        return context
    
class DetalleTareas(LoginRequiredMixin, DetailView):
    model = Tareas
    context_object_name = 'tareas'
    template_name = 'tareas/tarea.html'
    
class CrearTarea(LoginRequiredMixin, CreateView):
    model = Tareas
    fields = ('titulo','descripcion','completo','descarga','adjunto',)
    success_url = reverse_lazy('home')
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.user = self.request.user
        return super(CrearTarea, self).form_valid(form)
        
    
class ActualizarTarea(LoginRequiredMixin, UpdateView):
    model = Tareas
    success_url = reverse_lazy('tareas')
    context_object_name = 'tarea'
    fields = '__all__'
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context =super().get_context_data(**kwargs)
        context['numero_preventa'] = context['tarea'].pv
        try:
            context['link'] = str(context['tarea'].descarga).split('/')[-1]
        except:
            context['link']= 'sin link'

        return context
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        return super().form_valid(form)
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        print(form.data)
        print(form.errors.items())
        return super().form_invalid(form)
    

    
class EliminarTarea(LoginRequiredMixin, DeleteView):
    model = Tareas
    context_object_name = 'tarea'
    success_url = reverse_lazy('home')
    
    
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
    
class ActualizarPreventa(LoginRequiredMixin, UpdateView):
    model = Preventa
    success_url = reverse_lazy('home')
    fields = '__all__'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['preventa_id'] = self.object.pk  # Pasar el ID de la preventa al contexto
        # context['numero_preventa'] = context['prev'].preventa
        return context


