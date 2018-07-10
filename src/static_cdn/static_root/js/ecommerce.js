$(document).ready(function(){
    //Contact form handling

    var contactForm=$(".contact-form")
    var contactFormMethod=contactForm.attr("method")
    var contactFormEndpoint=contactForm.attr("action")
   
    function displaySubmitting(submitBtn,defaultTxt,doSubmit){
      if(doSubmit)
      {
          submitBtn.addClass("disabled")
          submitBtn.html("<i class='fa fa-spin fa-spinner'></i>Sending.........")
      }
      else
      {
          submitBtn.removeClass("disabled")
          submitBtn.html(defaultTxt)
      }
    }




    contactForm.submit(function(event){
       event.preventDefault()
       var contactFormData=contactForm.serialize()
       var contactFormSubmitBtn=contactForm.find("[type='submit']")
       var contactFormSubmitBtnTxt=contactFormSubmitBtn.text()
       displaySubmitting(contactFormSubmitBtn,contactFormSubmitBtnTxt,true)
       $.ajax({
          method:contactFormMethod,
          url:contactFormEndpoint,
          data:contactFormData,
          success:function(data)
          {
            contactForm[0].reset()
            $.alert({
            title:"success",
            content:data.message,
            theme:"modern",
            })

            setTimeout(function(){
              displaySubmitting(contactFormSubmitBtn,contactFormSubmitBtnTxt,false)
            },2000)
          },
          error:function(error)
          {
            console.log(error.responseJSON)
            var jsonData=error.responseJSON
            var msg=""
            $.each(jsonData,function(key,value){
              msg+=key+":"+value[0].message+"<br/>"
            })
            $.alert({
            title:"oops!!",
            content:msg,
            theme:"modern",
          })
          setTimeout(function(){
              displaySubmitting(contactFormSubmitBtn,contactFormSubmitBtnTxt,false)
            },2000)

          }
          
       })
    })




   //Searching Automatically
   var searchForm=$(".search-form")
   var searchInput=searchForm.find("[name='q']")
   var typingTimer;
   var typingInterval=500
   var searchBtn=searchForm.find("[type='submit']")
   searchInput.keyup(function(event){

     //Key Released
     clearTimeout(typingTimer)
     typingTimer=setTimeout(performSearch,typingInterval)
   })
   
   searchInput.keydown(function(event){
     clearTimeout(typingTimer)
   })

   function doSearch()
   {
     searchBtn.addClass("disabled")
     searchBtn.html("<i class='fa fa-spin fa-spinner'></i>Searching.....")
   }

   function performSearch(){
     doSearch()
     var query=searchInput.val()
     setTimeout(function(){
       window.location.href='/search/?q=' +query
     },1000)
     
   }
   
   
   
   //Related To Cart Ajax Refresh
    var productForm=$(".form-product-ajax")
    productForm.submit(function(event){

      event.preventDefault();
      var thisForm=$(this)
      //var actionEndpoint=thisForm.attr("action");
      var actionEndpoint=thisForm.attr("action");
      var httpMethod=thisForm.attr("method");
      var formData=thisForm.serialize();

      $.ajax({
        url:actionEndpoint,
        method:httpMethod,
        data:formData,
        success:function(data){
           console.log("Added",data.added)
           console.log("Removed",data.removed)
           var submitSpan=thisForm.find(".submit-span")
           
           if(data.added)
             {
               submitSpan.html("<Button type='submit' class='btn btn-danger'>Remove from Cart</Button>")
             }
           else
             {
               submitSpan.html("<Button type='submit' class='btn btn-success'>Add To Cart</Button>")
             }
             var navbarCount=$(".navbar-cart-count")
             navbarCount.text(data.cartItemCount)
             currentPath=window.location.href
             if(currentPath.indexOf("cart")!=-1)
             {
               refreshCart()
             }
           },
        error:function(errorData){
          $.alert({
            title:"oops!!",
            content:"An error Occurred",
            theme:"modern",
          })
        }
      })

    })

    function refreshCart(){
         console.log("In current cart")
         var cartTable=$(".cart-table")
         var cartBody=cartTable.find(".cart-body")
         //cartBody.html("<h1>Changed</h1>")
         var productRows=cartBody.find(".cart-product")
         var currentUrl=window.location.href
         
         var refreshCartUrl='/api/cart/'
         var refreshCartMethod="GET";
         var data={};
         $.ajax({
           url:refreshCartUrl,
           method:refreshCartMethod,
           data:data,
           success:function(data)
           {
             var hiddenCartItemRemoveForm=$(".cart-item-remove-form")
            
             if(data.products.length>0)
             {
             productRows.html("")
             i=data.products.length
             $.each(data.products,function(index,value){
               var newCartItemRemove=hiddenCartItemRemoveForm.clone()
               newCartItemRemove.css("display","block")
               newCartItemRemove.find(".cart-item-product-id").val(value.id)
               cartBody.prepend("<tr><th scope=\"row\">"+i+"</th><td><a href='"+value.url+"'><img  src='"+value.image+"' width='"+80+"' height='"+80+"' alt='"+value.name+"' logo'></a></td><td><a href='"+value.url+"'>"+value.name+"</a>"+newCartItemRemove.html()+"</td><td>"+value.price+"</td><td>")
               i--                 
             })
             cartBody.find(".cart-subtotal").text(data.subtotal)
             cartBody.find(".cart-total").text(data.total)
             }
             else
             {
               window.location.href=currentUrl
             }
           },
           error:function(errorData){
             $.alert({
            title:"oops!!",
            content:"An error Occurred",
            theme:"modern",
          })

           }
         })

    }
 })
