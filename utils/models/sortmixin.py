# coding: utf-8
from django.views.generic import ListView

class SortMixin(ListView):
    """
    View mixin which provides sorting for ListView.
    """
    default_sort_params = None
    allowed_sort_params = None

    def sort_queryset(self, qs, sort_by=False, order=False):
        if not sort_by or not order:
            sort_by,order = self.get_sort_params()
        qs = qs.order_by(sort_by)
        if order == 'desc':
            qs = qs.reverse()
        return qs

    def get_default_sort_params(self):
        if self.default_sort_params is None:
            raise ImproperlyConfigured(
                "'SortMixin' requires the 'default_sort_params' attribute "
                "to be set.")
        return self.default_sort_params

    def get_sort_params(self):
        default_sort_by, default_order = self.get_default_sort_params()
        sort_by = self.request.GET.get('sort_by', default_sort_by)
        order = self.request.GET.get('order', default_order)
        if self.allowed_sort_params is not None and not sort_by in self.allowed_sort_params:
            return (default_sort_by, order)
        return (sort_by, order)

    def get_queryset(self):
        return self.sort_queryset(
            super(SortMixin, self).get_queryset(),
            *self.get_sort_params())

    def get_context_data(self, *args, **kwargs):
        context = super(SortMixin, self).get_context_data(*args, **kwargs)
        sort_by, order = self.get_sort_params()
        context.update({
            'sort_by': sort_by,
            'order': order,
        })
        return context