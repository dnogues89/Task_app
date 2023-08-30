from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from pagos.models import Preventa, Pago, PagoForm
from django.db.models import Sum
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

#auth
from django.contrib.auth.mixins import LoginRequiredMixin

# def home(request):
#     return render(request,'pagos/home.html')

# Create your views here.
class ListaPreventas(LoginRequiredMixin,ListView):
    model = Preventa
    template_name = 'pagos/preventa_list.html'
    context_object_name = "preventas"
    
    def get_queryset(self):
        return Preventa.objects.filter(user = self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['preventas'] = context['preventas'].filter(user=self.request.user)
        context['cantidad'] = context['preventas'].filter().count()
        return context

class ListaPagosPreventa(LoginRequiredMixin, ListView):
    model = Pago    
    template_name = 'pagos/pago_list.html'
    context_object_name = "pagos"
    
    def get_queryset(self):
        return Pago.objects.filter(preventa_id=self.kwargs['pk']).all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pagos']= Pago.objects.filter(preventa_id=self.kwargs['pk'])
        context['monto_aprobado']= context['pagos'].filter(estado='2Aprobado').aggregate(Sum('monto'))['monto__sum']
        context['monto_pendiente']= context['pagos'].filter(estado='1Pendiente').aggregate(Sum('monto'))['monto__sum']
        context['monto_rechazado']= context['pagos'].filter(estado='3Rechazado').aggregate(Sum('monto'))['monto__sum']
        
        search = self.request.GET.get('search-area') or ''
        context['pagos'] = context['pagos'].filter(numero_comprobante__icontains=search)
        
        return context

# class ActualizarPago(LoginRequiredMixin, UpdateView):
#     model = Pago
#     fields = '__all__'
#     success_url = reverse_lazy('pagos_preventa')
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['pago_id'] = self.object.pk  # Pasar el ID de la preventa al contexto
#         # context['numero_preventa'] = 
#         print(context)
#         return context
    
class CrearPago(LoginRequiredMixin, CreateView):
    model = Pago
    form_class = PagoForm
    success_url = reverse_lazy('pagos_preventa')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Obtener el usuario actual
        user = self.request.user
        # Filtrar las preventas asignadas al usuario actual
        form.fields['preventa'].queryset = Preventa.objects.filter(user=user)
        return form
    
    def form_valid(self, form):
        user = self.request.user
        pago = form.save(commit=False)
        pago.user = user
        pago.save()
        return HttpResponseRedirect(self.success_url)
    
class ActualizarPago(LoginRequiredMixin, UpdateView):
    model = Pago
    form_class= PagoForm
    success_url = reverse_lazy('pagos_preventa')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['numero_preventa'] = context['pago'].preventa
        return context
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Obtener el usuario actual
        user = self.request.user
        # Filtrar las preventas asignadas al usuario actual
        form.fields['preventa'].queryset = Preventa.objects.filter(user=user)
        return form
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        pago = form.save(commit=False)
        if pago.estado == '3Rechazado':    
            pago.estado = '1Pendiente'
        pago.save()
        return super().form_valid(form)