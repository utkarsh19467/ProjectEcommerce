from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,DetailView,View
from .models import Product,ProductFile
from analytics.mixins import ObjectViewedMixin
from carts.models import Cart
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404,HttpResponse
from mimetypes import guess_type
from wsgiref.util import FileWrapper
from django.conf import settings
from django.contrib import messages
from orders.models import ProductPurchase
import os
# Create your views here.

class ProductFeaturedListView(ListView):
    template_name="products/list.html"

    def get_queryset(self,*args,**kwargs):
        request=self.request
        return Product.objects.featured()

class ProductFeaturedDetailView(ObjectViewedMixin,DetailView):
    queryset=Product.objects.featured()
    template_name="products/featured-detail.html"

    #def get_queryset(self,*args,**kwargs):
        #request=self.request
        #return Product.objects.all()


class UserProductHistoryView(LoginRequiredMixin,ListView):
    queryset=Product.objects.all()
    template_name="products/user-history-product.html"

    def get_context_data(self,*args,**kwargs):
        context=super(UserProductHistoryView,self).get_context_data(*args,**kwargs)
        cart_obj,new_obj=Cart.objects.new_or_get(self.request)
        context['cart']=cart_obj
        return context

    #def get_context_data(self,*args,**kwargs):
        #context=super(ProductListView,self).get_context_data(*args,**kwargs)
        #return context
    
    def get_queryset(self,*args,**kwargs):
        request=self.request
        views=request.user.objectviewed_set.by_model(Product)
        #viewed_ids=[x.object_id for x in views]
        #Product.objects.filter(pk__in=viewed_ids) one way to do
        return views



class ProductListView(ListView):
    queryset=Product.objects.all()
    template_name="products/list.html"

    def get_context_data(self,*args,**kwargs):
        context=super(ProductListView,self).get_context_data(*args,**kwargs)
        request=self.request
        cart_obj,new_obj=Cart.objects.new_or_get(request)
        context['cart']=cart_obj
        return context

    #def get_context_data(self,*args,**kwargs):
        #context=super(ProductListView,self).get_context_data(*args,**kwargs)
        #return context
    
    def get_queryset(self,*args,**kwargs):
        request=self.request
        return Product.objects.all()

def product_list_view(request):
    queryset=Product.objects.all()
    context={
        'object_list':queryset
    }
    return render(request,"products/list.html",context)

class ProductDownloadView(View):
    def get(self,*args,**kwargs):
        slug=kwargs.get("slug")
        pk=kwargs.get("pk")
        download_qs=ProductFile.objects.filter(pk=pk,product__slug=slug)
        if download_qs.count()!=1:
            raise Http404("Download Not Found")
        download_obj=download_qs.first()
        
        can_download=False
        user_ready=True
        if download_obj.user_required:
            if not self.request.user.is_authenticated():
                user_ready=True

        purchased_product=ProductPurchase.objects.none()
        if download_obj.free:
            can_download=True
        else:
            purchased_product=ProductPurchase.objects.products_by_request(self.request)
            if download_obj.product in purchased_product:
                can_download=True

        if not can_download or not user_ready:
            messages.error(self.request,"You can not Download this item")
            return redirect(download_obj.get_default_url())                    



        file_root=settings.PROTECTED_ROOT
        filepath=download_obj.file.path
        final_filepath=os.path.join(file_root,filepath)
        with open(final_filepath,'rb') as f:
            wrapper=FileWrapper(f)
            mimetype='application/force-download'
            guessed_mimetype=guess_type(filepath)[0]
            if guessed_mimetype:
                mimetype=guessed_mimetype
            response=HttpResponse(wrapper,content_type=mimetype)
            response['content-disposition']="attachment;filename=%s" %(download_obj.name)
            response["X-SendFile"]=str(download_obj.name)
            return response    
           

class ProductDetailSlugView(ObjectViewedMixin,DetailView):
    queryset=Product.objects.all()
    template_name="products/detail.html"
    
    def get_context_data(self,*args,**kwargs):
        context=super(ProductDetailSlugView,self).get_context_data(*args,**kwargs)
        request=self.request
        cart_obj,new_obj=Cart.objects.new_or_get(request)
        context['cart']=cart_obj
        return context

    def get_object(self,*args,**kwargs):
        request=self.request
        slug=self.kwargs.get('slug')
        #instance=get_object_or_404(Product,slug=slug,active=True)
        #if instance is None:
           #raise Http404("Product Doesn't exist")
        try:
            instance=Product.objects.get(slug=slug,active=True)
        except Product.DoesNotExist:
            raise Http404("Not found...")
        except Product.MultipleObjectsReturned:
            qs=Product.objects.filter(slug=slug,active=True)
            instance=qs.first()
        except:
            raise Http404("Not")        
        #object_viewed_signal.send(instance.__class__,instance=instance,request=request)
        return instance
    




class ProductDetailView(ObjectViewedMixin,DetailView):
    #queryset=Product.objects.all()
    template_name="products/detail.html"


    #def get_context_data(self,*args,**kwargs):
        #context=super(ProductDetailView,self).get_context_data(*args,**kwargs)
        #return context
    
    
    def get_object(self,*args,**kwargs):
        request=self.request
        pk=self.kwargs.get('pk')
        instance=Product.objects.get_by_id(pk)
        if instance is None:
           raise Http404("Product Doesn't exist")
        return instance
    
    #def get_queryset(self,*args,**kwargs):
        #request=self.request
        #pk=self.kwargs.get('pk')
        #return Product.objects.filter(pk=pk)


def product_detail_view(request,pk=None,*args,**kwargs):
    #instance=Product.objects.get(pk=pk)
    #instance=get_object_or_404(Product,pk=pk)
    #try:
        #instance=Product.objects.get(id=pk)
    #except:
        #print("no product here")
        #raise Http404("Product Doesn't exist")
    #except:
        #print("huh")  
    


    instance=Product.objects.get_by_id(pk)
    if instance is None:
        raise Http404("Product Doesn't exist")
  
  
  
  
   # qs=Product.objects.filter(id=pk)
    #if qs.exists() and qs.count()==1:
     #   instance=qs.first()
    #else:
        #raise Http404("Product Doesn't exist")              
   
   
    context={
        "object":instance
    }    
    return render(request,"products/detail.html",context)