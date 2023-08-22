from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from pagos.models import Preventa, Pago, PagoForm
from django.db.models import Sum
from django.urls import reverse_lazy

#auth
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class ListaPreventas(LoginRequiredMixin,ListView):
    model = Preventa
    template_name = 'pagos/preventa_list.html'
    context_object_name = "preventas"
    
    def get_queryset(self):
        return Preventa.objects.filter(user = self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['preventas'] = context['preventas'].filter(user=self.request.user)
        # context['cantidad'] = context['preventas'].filter().count()
        return context

class ListaPagosPreventa(LoginRequiredMixin, ListView):
    model = Pago    
    template_name = 'pagos/pago_list.html'
    context_object_name = "pagos"
    
    def get_queryset(self):
        return Pago.objects.filter(preventa_id=self.kwargs['pk']).all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['monto_aprobado']= Pago.objects.filter(preventa_id=self.kwargs['pk']).exclude(estado="Rechazado").aggregate(Sum('monto'))['monto__sum']
        return context

class ActualizarPago(LoginRequiredMixin, UpdateView):
    model = Pago
    fields = '__all__'
    success_url = reverse_lazy('pagos_preventa')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pago_id'] = self.object.pk  # Pasar el ID de la preventa al contexto
        return context
    
class CrearPago(LoginRequiredMixin, CreateView):
    model = Pago
    form_class = PagoForm
    success_url = reverse_lazy('pagos_preventa')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CrearPago, self).form_valid(form)