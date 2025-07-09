// window.onbeforeunload = function() 
// {
//    return "هل أنت متأكد من الخــروج ؟";
// }


var restored_receit = 0
var passwordConfirmed = false

const passwordPopUp = `
                    <div class= 'alert' style = 'z-index:99999'>
                        <div class ='popupBox border-light' type = 'password-input'>
                            <span class = 'close'><i class="fa-solid fa-xmark"></i></span>
                            <i class="fa-solid fa-lock fa-2x "></i>
                            <input type ='password' placeholder = 'أدخـل كلمة المرور ...' />
                            <i class="login border-light fa-solid fa-chevron-left "></i>
                        </div>
                    </div>
`
function alertBox({ type = "", message = "hola" , redbtn = false , greenbtn = false , title = "تنبيـــه" , stopPropagation = 'false'}) { 
 

    let btns = `
        <div class ='btns'>
            <button class = 'green'>نعم</button>
            <button class = 'red'>لا</button>
        </div>
    `


    if (redbtn == false && greenbtn == false ) {
        btns = ""
     }else { 
        if (redbtn != false && greenbtn != false ) { 
         
             btns = `
                 <div class ='btns'>
                     <button class = 'green'>${greenbtn}</button>
                     <button class = 'red'>${redbtn}</button>
                 </div>
                 ` 
         }else if(redbtn != false ) { 
             btns = `
             <div class ='btns'>
                 
                 <button class = 'red'>${redbtn}</button>
             </div>
             ` 
         }else if (greenbtn !=false ) { 
             btns = `
             <div class ='btns'>
                 
                 <button class = 'green'>${greenbtn}</button>
             </div>
             `  
         }
     }


    
    let htmx = `
        <div id = '${type}' class = 'alert' stopPropagation = '${stopPropagation}'>
            <div class = 'messageBox border-2px'>
                <span class = 'close'><i class="fa-solid fa-rectangle-xmark fa-2x"></i></span>
                <span class = 'title'>${title}</span>
                <span class = 'msg'>${message}</span>
                ${btns}
        
            </div>
        </div>
    `
    


    $("body").remove("div.alert").append(htmx)
    
  
   
}


$(()=> {


    
    // close the PopupBox ....

    $("body").on("click"  , "div.alert > div.popupBox > span.close" , ()=> { 
        $("div.alert").remove()
      
            location.reload()
      
    })


    
    // login into popupBox

        $("body").on("click"  , "div.alert > div.popupBox > i.login" , (r)=> { 
            let password = $("div.alert > div.popupBox > input").val()
            $.ajax({
                url : "requests",
                method :"POST" ,
                data :{"type" : "confirm.password.root" , "password" : password} , 
                success : (e)=>{
                    if (e.state === true ) { 
                        passwordConfirmed = true
                        $(r.currentTarget).closest("div.alert").remove()
                    }else { 
                        alert("كلمه المرور خاطـــئه !")
                    }
                }
            })
        })


    // Alert box close btn   , 
    //  ALERT box green btn hide after click ↓


    $("body").on("click" , "div.alert > div.messageBox > span.close , div.alert > div.messageBox > div.btns > button.red , div.alert > div.messageBox > div.btns > button.green " , (e)=>{
        currentTarget = $(e.currentTarget).closest("div.alert")

        

        if($(currentTarget).attr("stopPropagation") === 'true') { 
                $(currentTarget).fadeOut(100 , ()=>{
                $(currentTarget).remove()
            })
        }else { 

            $("div.alert").fadeOut(100 , ()=>{
                $("div.alert").remove()
            })
        }
       
    })  

   

    // restore the receit 


    $("body").on("click" , "div.navbar > div.section > div#restore_receit" , (e)=>{ 

        // check the root password ....
        
        if(!passwordConfirmed) { 
            $("body").append(passwordPopUp)
        }
        



        if($(e.currentTarget).hasClass("active")) { 
            return false
        }
        restored_receit = 0
        $(e.currentTarget).addClass("active")
        $("div.skeleton > div.classes").css("display" , "none")        
        $("div.wrapper > div.skeleton > div.receit").css("display"  , "none")

        
        let htmx = `
        
                <div class = 'receit border-light' type = 'restore'>
                        <div class = 'item-ctrl'>
                            <span id = 'close' class ='item amount border-light'>إلــغاء</span>
                        </div>

                        <div class = 'item-ctrl search-bar' >
                            <i class="fa-solid fa-magnifying-glass"></i>
                            <input id = 'receit_number' class = 'border-light' type = 'number' step = '1' min = '1' placeholder = 'أدخــل رقم الفـاتوره '/>
                            <span class = 'search item border-light'>بحث</span>
                        </div>

                        <div class = 'items '>
                            <span class = 'title'>فــاتوره مرتــجـع</span>

                            <div class = 'sales-items'>
                            
                            </div>
                        </div>

                        <div class= 'total'>
                            <span class = 'title'>الإجــمـالي</span>
                            <span class = 'value'>0</span>
                        </div>


                        <div class = 'btns'>
                            <button class = 'delete border-light'>استــرجاع الفاتوره بالكــامل<i class="fa-solid fa-xmark"></i></button>

                            

                        </div>
                </div>
        `
        $("div.wrapper > div.skeleton ").append(htmx)
    })


    // when click on search span to view all receit details 

    $("body").on("click" , "div.wrapper > div.skeleton > div.receit[type='restore'] > div.item-ctrl.search-bar > span.search " , (e)=>{
        
        $("div.wrapper > div.skeleton > div.receit[type = 'restore'] > div.items > div.sales-items").html("")
        $("div.wrapper > div.skeleton > div.receit[type = 'restore'] > div.total > span.value").text("0")
        let ReceitNumber = $(e.currentTarget).parent().children("input#receit_number").val()
        restored_receit = ReceitNumber
        
        $.ajax({
            method : "POST",
            url : "requests" , 
            data : {"type" : "restore.receit" , "receitNumber" : ReceitNumber},
            success : (e)=>{
                console.log(e)
                if (e.state === false) { 
                    switch(e.reason) { 
                        case "not.found" : 
                            alertBox({message : "عذرا , لا توجـد فاتوره بهـذا الرقم"})
                            break;
                        case "no.receit.number" : 
                            alertBox({message : "من فضلك قم بإدخال رقـم الفـاتوره المراد استــرجاعها أولا "})
                            break;
                        case "out.of.date" : 
                            alertBox({message : "عذرا ,  هذه الفاتروه قديمه ولا يمكن استـرجاعها الا بواسطه المــدير فقط"})
                            break;
                    }
                    return false
                }
                let item = ``
                len = e.products.length
                j= 0
                for (x of e.products) { 

                    let i   = `
                        <div class="item" uid="${e.products[j]}">
                            <div class="details">
                                <span class="name">${e.names[j]}</span>
                                <span class="price"> ${e.prices[j]} </span>
                            </div>
                            <span class="amount">${e.amounts[j]}</span>
                        </div>
                    `
                    j++
                    item += i
                }

                $("div.wrapper > div.skeleton > div.receit[type='restore'] > div.items >  div.sales-items").html(item)
                $("div.wrapper > div.skeleton > div.receit[type='restore'] > div.total >  span.value").text(e.intotal)

            }
        })
    })

    // when click on the delete button to delete the receit
    $("body").on("click" , "div.wrapper > div.skeleton > div.receit[type='restore'] > div.btns > button.delete " , (e)=>{
        if($("div.wrapper > div.skeleton > div.receit[type='restore'] > div.items > div.sales-items > div.item").length === 0 ) { 
            return false
        }
        if (restored_receit !== 0 ) { 
            alertBox({message : `هل أنت متأكد من انك تريد حذف  الفاتوره رقم (<span style = 'color : green'> ${restored_receit} </span>) ب الكامل ؟` , redbtn : "لا" , greenbtn : "نـعم"  , type  : "confirm_restore" , stopPropagation : "true"})
        }
  
    })



    // when Confirming delteing of the receit
    $("body").on("click" , "div.alert#confirm_restore > div.messageBox > div.btns > button.green" , ()=>{
        $.ajax({
            method:"POST",
            url:"requests",
            data : {"type" : "receit.delete" , "receitNumber" : restored_receit } ,
            success : (e)=>{

                    if (e.state === true ) { 
                        alertBox({message : "تـم إستــرجـاع الفاتورة بنجــاح "})
                        $("div.navbar > div.section > div#restore_receit").trigger('click')
                        restored_receit = 0
                    }else { 
                        switch(e.reason) { 
                            case "not.seller" : 
                                alertBox({message : "عــذرا , لست أنت من قام ببيع هذه الفــاتورة"})
                                break ;
                            case "not.enough.money.to.restore" :
                                alertBox({message : "عــذرا , الخزنه لا تحتوي علي النقود الكــافيه لإرجـاع هذه الفـاتوره"})
                                break ;
                            case "not.found" : 
                                alertBox({message : "عذرا , هذه الفـاتوره غير موجوده بالفعل "})
                                break;    
                        }
                    }
            }
        })
    })


    // canceling deleteing a receit when i click on cancel button 

    $("body").on("click" , "div.wrapper > div.skeleton > div.receit[type='restore'] > div.item-ctrl > span#close " , (e)=>{

        $("div.navbar > div.section > div#restore_receit").removeClass("active")
        $("div.wrapper > div.skeleton > div.receit[type='restore']").remove()
        $("div.wrapper > div.skeleton > div.receit").css("display" , "flex")
        $("div.wrapper > div.skeleton > div.classes").css("display" , "flex")


    })

})
