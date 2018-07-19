
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.http import is_safe_url
from django.views.generic import CreateView,FormView,View,DetailView,UpdateView
from .models import GuestEmail,EmailActivation
from django.contrib import messages
from .forms import LoginForm,RegistrationForm,GuestForm,ReactivateEmailForm,UserDetailChangeForm
from django.views.generic.edit import FormMixin
from django.contrib.auth import authenticate,login,get_user_model
from .signals import user_logged_in
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from ecommerce.mixins import NextUrlMixin,RequestFormAttachMixin
# @login_required
# def account_home_view(request):
#     return render(request,"accounts/home.html",{})


class AccountEmailActivationView(FormMixin,View):
    success_url='/login/'
    form_class=ReactivateEmailForm
    key=None
    def get(self,request,key=None,*args,**kwargs):
        self.key=key
        if key is not None:
            qs=EmailActivation.objects.filter(key__iexact=key)
            confirm_qs=qs.confirmable()

            if confirm_qs.count()==1:
                obj=confirm_qs.first()
                obj.activate()
                messages.success(request,"Your email has been activated now you can login")
                return redirect("login")
            else:
                activated_qs=qs.filter(key__iexact=key,activated=True)
                if qs.exists():
                    reset_link=reverse("password_reset")
                    msg="""Your email has already been confirmed
                        Do you need to <a href="{link}">reset your password</a>?
                    """.format(link=reset_link)
                    messages.success(request,mark_safe(msg))
                    return redirect("login") 
        context={'form':self.get_form(),"key":key}        
        return render(request,'registration/activation-error.html',context)


    def post(self,request,*args,**kwargs):
        form=self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)



    def form_valid(self,form):
        msg="""
        Activation Link Sent On Your email You can Now Activate        
        """        
        request=self.request
        messages.success(request,msg)
        email=form.cleaned_data.get("email")
        obj=EmailActivation.objects.email_exists(email).first()
        user=obj.user
        new_activation=EmailActivation.objects.create(user=user,email=email)
        new_activation.send_activation()
        return super(AccountEmailActivationView,self).form_valid(form)
    def form_invalid(self,form):
        context={'form':form,"key":self.key}
        return render(self.request,'registration/activation-error.html',context)



class AccountHomeView(LoginRequiredMixin,DetailView):
    template_name='accounts/home.html'
    def get_object(self):
        return self.request.user    

class GuestRegisterView(NextUrlMixin,RequestFormAttachMixin,CreateView):
    form_class=GuestForm
    default_next='/register/'

    def get_success_url(self):
        return self.get_next_url()

    def form_invalid(self,form):
        return redirect(self.default_next)

  
class RegistrationView(CreateView):
    form_class=RegistrationForm
    template_name='accounts/register.html'
    success_url='/login/'

class LoginView(RequestFormAttachMixin,NextUrlMixin,FormView):
    form_class=LoginForm
    success_url='/'
    template_name='accounts/login.html'
    default_next='/'
   
    def form_valid(self,form):
       next_path=self.get_next_url()   
       return redirect(next_path)



class UserDetailUpdateView(LoginRequiredMixin,UpdateView):
    form_class=UserDetailChangeForm
    template_name='accounts/detail-update-view.html'
    def get_object(self):
        return self.request.user


    def get_context_data(self,*args,**kwargs):
        context=super(UserDetailUpdateView,self).get_context_data(*args,**kwargs)
        context['title']='Change Your Account Details'
        return context

    def get_success_url(self):
        return reverse("account:home")    



#User=get_user_model()
#def register_page(request):
    #form=RegistrationForm(request.POST or None)
    #context={
        #"form":form
    #}
    #if form.is_valid():
        #form.save()
        
    #return render(request,"accounts/register.html",context)        


def login_page(request):
    form=LoginForm(request.POST or None)
    context={
        "form":form
    }
    next_=request.GET.get('next')
    next_post=request.POST.get('next')
    redirect_path=next_ or next_post or None

    if form.is_valid():
        username=form.cleaned_data.get("username")
        password=form.cleaned_data.get("password")
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path,request.get_host()):
                return redirect(redirect_path)
            else:    
                return redirect("/")
        else:
            print("Error")

    return render(request,"accounts/login.html",context)

