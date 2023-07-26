from typing import Any, Dict, Type
import os
from django.http import HttpResponse
from django.conf import settings

from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Tareas, Preventa, TareasForm, PreventaForm

from .asignacion_tareas import AsignacionTareas

#Descargar archivos
def download_file(request, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, 'archivos_para_descargar' ,file_name)
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
            AsignacionTareas.crear_tareas_usuario(user)
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
    success_url = reverse_lazy('tareas')
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.user = self.request.user
        return super(CrearTarea, self).form_valid(form)
        
    
class ActualizarTarea(LoginRequiredMixin, UpdateView):
    model = Tareas
    form_class = TareasForm
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
            if pv.tipo_venta == 'Contado':
                AsignacionTareas.crear_tareas_preventa_contado(pv.user,pv)
            else:
                AsignacionTareas.crear_tareas_preventa_financiado(pv.user,pv)
            if pv.tipo_cliente == "Persona Fisica":
                AsignacionTareas.crear_tareas_preventa_persona_fisica(pv.user,pv)
            else:
                AsignacionTareas.crear_tareas_preventa_persona_juridica(pv.user,pv)
            return redirect('tareas')
        

class ActualizarPreventa(LoginRequiredMixin, UpdateView):
    model = Preventa
    form_class=PreventaForm
    success_url = reverse_lazy('preventa')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['preventa_id'] = self.object.pk  # Pasar el ID de la preventa al contexto
        return context
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        pv = form.save()
        if pv is not None:
            if pv.retira_unidad == 'Transportista':
                AsignacionTareas.crear_tareas_retiro_transporte(pv.user,pv)
            if pv.retira_unidad == 'Individuo':
                AsignacionTareas.crear_tareas_retiro_individuo(pv.user,pv)
            if pv.retira_unidad == 'Titular':
                AsignacionTareas.crear_tarea_retira_cliente_final(pv.user,pv)
            if pv.cedulas_azules != 0 and pv.cedulas_azules is not None and pv.cedulas_azules != "":
                azules_actuales = Tareas.objects.filter(pv=pv,titulo='Cedula azul DNI FRENTE').count()
                for i in range(0,pv.cedulas_azules-azules_actuales):
                    AsignacionTareas.crear_cedula_azul(pv.user,pv)
            if pv.socios != 0 and pv.socios is not None and pv.socios != "":
                socios_actuales = Tareas.objects.filter(pv=pv,titulo='Socio DNI FRENTE').count()
                for i in range(0,pv.socios-socios_actuales):
                    AsignacionTareas.crear_socio_persona_fisica(pv.user,pv)

        return redirect('preventas')

