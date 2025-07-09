
//python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 > dump.json
//python -Xutf8  manage.py dumpdata > output.json
var receit_products = [];
var intotal  = 0;



$(()=>{

    $.ajax({
        method:"POST",
        url:"requests",
        data : {"type" : `get.marakez.products`},
        success : (e)=>{

            $("div.classes > div.items-rect").html("")
            for (x of e.data) { 
                
                let item = ` <div uid = ${x.id} Pname = '${x.name}' price = ${x.price} class = 'item border-light'>
                                <span class = 'name'>${x.name}</span>
                                <span class = 'price'>${x.price}</span>
                            </div> `
                $("div.classes > div.items-rect").append(item) 
            }
        }
    })









    $("div.navbar > div.section > div#logout").on("click" , ()=>{
        console.log("Clicked !")
        alertBox({message : "هل أنت مـتأكد من أنك تريد الــخروج من الــبرنــامج ؟" ,redbtn : "لا"  , greenbtn : "نعم" , type  :"logout"})
    })



    // logout On Click 
    $("body").on("click" , "div.alert#logout > div.messageBox > div.btns > button.green" , ()=>{
        window.location.href = "/logout"
    })



    // Activate delete btnof  Selected Item from receit
    $("body").on("click" ,"div.sales-items > div.item" , (e)=>{
        e.stopPropagation()
        $("div.sales-items > div.item").removeClass("active")
        $(e.currentTarget).addClass("active")
        $("div.receit > div.item-ctrl > span.delete").removeClass("inactive")

    })


    $("body").on("click" , "div.sales-items " , ()=>{
        console.log("Clicked")
        $("div.sales-items > div.item").removeClass("active")
        $("div.receit > div.item-ctrl > span.delete").addClass("inactive")
    })

   



  
    // CHANGE Amount of the item in the queuing table >= <=
    $("body").on("click" , "div.sales-items > div.item > span.amount" , (e)=> { 
    //    $(e.currentTarget).attr("contenteditable" , "true");
        $(e.currentTarget).css({"background-color" : "green"})
        $(e.currentTarget).css({"color" : "white"})
        $(e.currentTarget).css({"padding" : "5px 10px"})
        $(e.currentTarget).css({"border-radius" : "10px"})
        $(e.currentTarget).css({"direction" : "ltr"})



       console.log("Clicked ...")
    })


    $("body").on("keypress" , "div.sales-items > div.item > span.amount" , (e)=> {
        let itemId = $(e.currentTarget).closest("div.item").attr("uid")
        console.log( "→", itemId)
        if (e.key == "Enter") { 
            console.log("Enter ...")
            let newValue = $(e.currentTarget).text()
            console.log(newValue)
            // $(e.currentTarget).removeAttr("contenteditable")
           
            try {
                newValue = parseInt(newValue)
            }catch  { 
                console.log("Wrong amount")
                return false
            }
            if (!Number.isInteger(newValue)) { 
                
                refresh_receit()
                return alertBox({message : "من فضلك قم بإدخــال كمية صحيحه !"})
                
            }

            for ([x,y] of receit_products.entries())  { 
                if (y['uid'] === itemId) { 
                  receit_products[x].amount = newValue
                }
            }
            console.log("Edited Successfully ...")
            refresh_receit()
        } else  { 
            console.log(e.key)
        }
    })


    // refresh receit form 

    function refresh_receit() { 
        let sales_items = ""
        for (x of receit_products) { 
            sales_items += `
                <div class="item" uid = '${x.uid}'>
                    <div class="details">
                        <span class="name">${x.name}</span>
                        <span class="price"> ${x.price} </span>
                    </div>
                    <span class="amount" contenteditable >${x.amount}</span>
                </div>
            `
        }


        $("div.sales-items").html(sales_items)

         let total = 0
        for (x of receit_products) { 
            let amount = x.amount 
            let price = x.price 
            total += amount*price
        }
        intotal = total
        $("div.receit > div.total > span.value").text(total)
    }


    
    // create_new_receit 

    function create_new_receit() { 
        receit_products = []
        intotal = 0
        refresh_receit()

    }


    // cancel the Booking 

    $("body").on("click" , "div.overlay > div.details > div.item > button.cancel" ,(e)=>{
        $("div.overlay").fadeOut(200 , (e)=>{
            $("div.overlay").remove()
        })
    })

    // show the totalMoney of the booking bank

    $("#total-money").on("click" , (e)=> { 
        $.ajax({
            method : "POST",
            url : "requests" ,
            data : {"type" : "booking.total.money"},
            success : (e)=>{
                alertBox({message : `النقود الموجوده حاليا ف خزنة الحجوزات هي :  <span style = 'color : green'>${e.intotal} جنيه </span>` })
            }
        })
    })

    // BACK TO CASHER 
    $("#back-to-casher").on("click" , ()=>{ 
        window.location.href = "/"
    })


    // close the query window 

    $("body").on("click" , "div.overlay > span.close" , (e)=>{
        $("div.overlay").fadeOut(200 , ()=> { 
            $("div.overlay").remove()
        })
    })
    // when Click on Booking Querying Button 
    $("#query").on("click" , (e)=>{
        $.ajax({
            method : "POST",
            url : "requests" , 
            data : {"type":"booking.query" },
            success : (e)=>{
                if (e.state === false) { 
                    return alertBox({message : "لا يوجد حجوزات حتي الأن !"})
                }
                if (e.state === true) { 
                    let htmx = ``
                    for (x of e.data) { 
                        console.log(x)
                        let remainingElement , stateElement

                        if (x.remaining == 0 ) { 
                            remainingElement = `<th disabled style = 'pointer-event:none;' class = 'pay-remain'><i class="fas fa-check-square fa-2x"></i></i></th>`
                        }else { 
                            remainingElement = `<th class = 'pay-remain'><i class="fas fa-check-square fa-2x"></i></i></th>`
                        }

                        if (x.state === false) { 
                            stateElement = `<th class = 'state red'><i class="fa-solid fa-circle-xmark "></i></th>`
                        }else { 
                            stateElement = `<th class = 'state green'><i class="fas fa-check-circle "></i></th>`
                        }
                        let item = `
                            <tr id = ${x.id}>
                                <th class = 'name'>${x.booker}</th>
                                <th class = 'products'>${x.products}</th>
                                <th class = 'paid'>${x.paid}</th>
                                <th class = 'required'>${x.required}</th>
                                <th class = 'remainning'>${x.remainning}</th>
                                ${remainingElement}
                                <th class = 'notes'>${x.notes}</th>
                                
                                <th class = 'date'>${x.date}</th>
                                <th class = 'time'>${x.time}</th>
                                ${stateElement}
                                <th class = 'save'><i class="fas fa-check-circle fa-2x"></i></th>
                                
                            </tr>
                        `
                        htmx += item

                        $("div.overlay").remove()

                        let overlay = `
                            <div class = 'overlay' type = 'query'>
                                <span class = 'close'><i class="fa-solid fa-xmark"></i></span>

                                <div class = 'table'>
                                    <div class = 'title'>
                                        <i class="fas fa-question fa-2x"></i>
                                        <span>الاستعلام عن الحجوزات</span>
                                    </div>
                        
                                    <div class = 'table-content'>
                                        <table>
                                            <tr>
                                                <th>اسم الجهه</th>
                                                <th>الأصناف</th>
                                                <th>المدفوع</th>
                                                <th>المطلوب</th>
                                                <th> متبقي</th>
                                                <th> سداد المتبقي</th>
                                                <th>ملحوظات</th>
                                                <th>تاريخ الحجز</th>
                                                <th>وقت الحجز</th>
                                                <th>جــاهز للاستلام</th>
                                                <th>تسليم الحجز</th>
                                                
                            
                                            </tr>
                            
                                            ${htmx}
                                        </table>
                                    </div>
                                </div>
                            </div> 
                        `
                        $("body").append(overlay)
                    }
                }
            }
        })
    })



    // when click on save button on booking table : 
    $("body").on("click" , "div.overlay > div.table > div.table-content > table > tbody > tr > th.save" , (e)=>{
        let confirming = confirm("هل أنت متأكد من انك تريد تسليم هذا الحجز ؟")
        if (!confirming) { 
            return false
        }
        console.log("Done")
        let id = $(e.currentTarget).closest("tr").attr('id')
        $.ajax({
            method : "POST",
            url  :"requests",
            data : {"type" : "save.booking" , "id" : id},
            success  :(e)=>{

                if (e.state === false ) { 
                    switch(e.reason) {
                        case "pay.remainning.first" :
                            alertBox({message : " عذرا يجب سداد مبلغ الحجز ب الكامل أولا لكي يتم تسليم الحجز !"})
                            break;
                        case "already.delivered" :
                            alertBox({message : "عذرا لقد قمت بتسليم هذا الحجز مسبقا !"})
                            break;
                        case "no.booking.found" :
                            alertBox({message : "عذرا هذا الحجز غير موجود برجاء المحاوله لاحقا !"} )
                            break;
                    } 
                }else { 
                    $("div.overlay").remove()
                    alertBox({message : `تم تسليم هذا الحجز بنجااح <br/>برجاء سحب النقود من الدرج  (${e.required})جنيه وتسليمها للشخص المسئول`})
                }
            }
        })
    })

    // when click on pay.remainning button on booking table : 
    $("body").on("click" , "div.overlay > div.table > div.table-content >  table > tbody > tr > th.pay-remain" , (e)=>{ 
        
        // check if the remainning money  == 0 : don't do anything 
        // ajax Request

        let confirming = confirm("هل أنت متأكد من انك تريد استلام المبلغ المتبقي من  هذا الحجز ؟")
        if (!confirming) { 
            return false
        }

        let id = $(e.currentTarget).closest("tr").attr('id')
        $.ajax({
            method :"POST",
            url : "requests", 
            data : {"type" : "booking.pay.remain" , "id" : id} , 
            success :(e)=>{
                console.log(e)
                if (e.state === true) { 
                    $("div.overlay").remove()
                    alertBox({message : `تم سداد مبلغ متبقي وقدره <span style = 'color:green'>${e.remainning} جنيه </span>  من فضلك قم بوضع هذه النقود ف الدرج `})
                }else {
                    if (e.reason === "no.remainning"){
                        alertBox({message : "لا يوجد مبلغ متبقي لهذا الحجز لكي يقوم بسداده "})
                    }
                }
            }
        })
        
    })


    // add product to the receit 

    $("body").on("click" , "div.items-rect > div.item" , (e)=> { 
        let id = $(e.currentTarget).attr("uid")
        let name = $(e.currentTarget).attr("Pname")
        let price = $(e.currentTarget).attr("price")
       
        if (receit_products.length !== 0) { 
            let ids = []
            for (x of receit_products) { 
                ids.push(x.uid)
            }
            if (ids.includes(id)) { 
                index = ids.indexOf(id)
                receit_products[index].amount += 1
            }else { 
                receit_products.push({"uid" : id , "name" : name , "price" : price , "amount" : 1})
            }

        
        }else { 
            receit_products.push({"uid" : id , "name" : name , "price" : price , "amount" :1})
        }

        refresh_receit()
 
    }) 





    // delete product from the receit

    $("body").on("click" , "div.item-ctrl > span.delete" , ()=>{
        console.log("Clicked ")
        let itemId = $("div.sales-items > div.item.active").attr('uid')
        console.log(itemId)
        let ids = []
        for (x of receit_products) { 
            ids.push(x.uid)

        }

        if (ids.includes(itemId)) { 
            receit_products[ids.indexOf(itemId)].amount -= 1

            if (receit_products[ids.indexOf(itemId)].amount <= 0 ) { 
                receit_products.splice(ids.indexOf(itemId) , 1)
            }
            refresh_receit()
        }
       
        
    })

    
    // delete the current receit
    $("div.receit >  div.btns > button.delete").on("click" , ()=>{
        if (intotal !== 0 ) { 
            alertBox({message : "هل أنت متأكد من أنك تريد حـذف الفــاتورة الـحاليه ؟" , type : 'delete.recent.receit' ,greenbtn : "نعم" , redbtn : "لا"})

        }
        
        
       
    }) 


    
    // confirm deleting the current receit
    $("body").on("click" , "div.alert[id = 'delete.recent.receit'] > div.messageBox > div.btns > button.green" , ()=> { 
        create_new_receit()
    })



    // when click on save button do this function
    
    function saveFun() { 
        if (intotal !== 0 ) { 
            alertBox({message : "هل أنت متأكد من أنك تريد حفظ الفــاتورة الـحاليه ؟" , type : 'save.recent.receit' ,greenbtn : "نعم" , redbtn : "لا"})

        }
    }



    // change the inputs of remaining when change the paid input 

    $("body").on("keyup" , "div.overlay > div.details > div.item[type = 'money.paid'] > input " , (e)=>{ 
        
        let remaining = intotal - $(e.currentTarget).val()
        
        $("body").find("div.overlay > div.details > div.item[type = 'money.remainning'] > input").attr("value" , remaining )
    })
    // save the current receit  
    $("div.receit >  div.btns > button.save").on("click" , ()=>{ 

        // check if the all amounts are valid of not !!

        let all_items = $("div.receit > div.items > div.sales-items > div.item")
        for (x of all_items) { 
            console.log($(x).find("span.amount").text() * 5)
            if (!Number.isInteger($(x).find("span.amount").text() * 5) ) { 

                refresh_receit()
                return alertBox({message : "من فضلك قم ب ادخــال كميات صحيحه !"})
            }
            var nv = Number.parseInt($(x).find("span.amount").text().trim(" "))
            
            if (!Number.isInteger(nv)){
            
                refresh_receit()
                return alertBox({message :"من فضلك قم بإدخــال كميات صحيحه أولا قبل حفظ الفاتوره !"})
            }

            let item_id = $(x).attr("uid")
            console.log("edititng...")
            for ([i,y ] of receit_products.entries()) { 
                if (y.uid == item_id) { 
                    receit_products[i].amount = $(x).find("span.amount").text()
                    refresh_receit()
                }
            }
        }

        if (intotal <= 0) { 
            return False
        }
      
  
            $.ajax({
                method :"POST",
                url : "requests" , 
                data : {"type" : "get.marakez.names"} , 
                success :(e)=>{ 
                    if (e.state)  {
                        marakez_names = e.data
                        let options = ``
                        console.log( "→", marakez_names)
                        for (i of marakez_names) {
                            options += `<option value  = ${i.id}>${i.name}</option>`

                            
                        }
                        let htmx = `
                                <div class = 'overlay'>
                                    <div class = 'details'>
                                            <span class = 'title'>تفــاصيل الحجز</span>
                                            <div class = 'item' type = 'dist'>
                                                <span>اسم الجهه : </span>
                                                <select>
                                                    <option disabled selected value = '0'>اختر الجهه التي تريد الحجز</option>
                                                    ${options}
                                                </select>
                                            </div>

                                            <div class = 'item' type = 'money.paid'>
                                                <span>المبلغ المدفوع : </span>
                                                <input  min = 0 type = 'number' placeholder = 'اكتب المبلغ المدفوووع'/>
                                            </div>

                                            <div class = 'item' type = 'money.total'>
                                                    <span class = 'value'>المبلغ المطلوب : </span>
                                                    <input min = 0  type = 'number' value = '${intotal}'/>
                                            </div>

                                            <div class = 'item' type = 'money.remainning'>
                                                <span class = 'value'>المبلغ المتبقي : </span>
                                                <input   type = 'number' value = '${intotal}'/>
                                            </div>

                                            <div class = 'item' type = 'notes'>
                                                <span class = 'value'>ملحوظــات : </span>
                                                <textarea placeholder = 'قم بتسجيل ملحوظات اذا اردت'></textarea>
                                            </div>

                                            <div class = 'item'>
                                                <button class = 'save'>حجز</button>
                                                <button class = 'cancel'>الغاء</button>
                                            </div>
                                    </div>
                                </div>
                            `

                        $("body").append(htmx)



                        
                    }else { 
                        return false
                    }
                }
            })
        
       

      

       
    })




    // when click on save the hagz fatora 


    $("body").on( "click", "div.overlay > .details > .item > button.save"  , (e)=> { 
        let dist = $("div.overlay > div.details > div.item[type = 'dist'] > select > option:selected").attr("value")
        let paid = $("div.overlay > div.details > div.item[type ='money.paid'] > input").val()
        let required = intotal
        let remainning = $("div.overlay > div.details > div.item[type ='money.remainning'] > input").val()
        let notes = $("div.overlay > div.details > div.item[type ='notes'] > textarea").val()


        if (dist == 0) { 
            return alertBox({message : "من فضلك قم ب اختيار الجهه التي تريد الحجز أولا"})
        }
        if (paid.trim(" ") === "")  { 
            return alertBox({message :"سجل النقود المدفوعه"})

        }
        if (paid > intotal)  { 
            return alertBox({message :"النقود المدفوعه اكثر من النقود المطلوبه "})

        }

        $.ajax({
            method:"POST",
            url : "requests",
            data : {"type" : "booking" , "dist" : dist , "paid" : paid , "required" :required , "remainning" : remainning , "notes" : notes ,"products" : JSON.stringify(receit_products)}, 
            success : (e)=>{
                console.log(e)
                if (e.state) { 
                    distName = $("div.overlay > div.details > div.item[type = 'dist'] > select > option:selected").text()

                    $("div.overlay").remove()
                    let info = `<span style ='font-size : 20px;'>تم الحجز بنجاح</span>`
                    for (x of receit_products) { 
                        productName = x.name 
                        productPrice = x.price
                        productAmount = x.amount
                        info += `<span style = 'color : #252525;'> تم حجز عدد (<span style ='color:green;'>${productAmount}</span>) <span style ='color:green;'>${productName}</span> بأجمالي <span style ='color:green;'>${productPrice * productAmount}</span> جنيه</span>`

                    }
                    info += `<span style = 'font-size : 17px;'>الجهه التي قامت ب الحجز : <span style = 'color : green ; font-size : 18px'>${distName}</span></span>`
                    info += "<span style ='color : #252525; font-size : 11px;font-style:italic'>تم التصميم بواسطة د . وليد أسامه</span>"
                    alertBox({message : info})
                    create_new_receit()
                }
            }
        })
    })
    


      // confirm saving the current receit
    $("body").on("click" , "div.alert[id = 'save.recent.receit'] > div.messageBox > div.btns > button.green" , ()=> { 

        $.ajax({
            method:"POST", 
            url :"requests" ,
            data : {"type" : "marakez.receit.save" , "data" : JSON.stringify({"receit_products" : receit_products, "total_money" : intotal})},
            success : (r)=>{
                console.log(r)
                let receitId = r.receitId
                $.ajax({
                    method : "POST" ,
                    url : "requests" , 
                    data : {"type" : "print.marakez.receipt"  , "receitId" : receitId} , 
                    success : (e)=> { 
                        console.log(e)
                    }
                })
                create_new_receit()


            }
        })
    })



    // ending the shift

    $("div.navbar >  div.section  > div.item[type = 'finish']").on("click" , ()=>{
        
       

            $("body").append(passwordPopUp)

        let htmx = `
            <div class = 'alert' type = 'finish.shift'>
                <div class = 'container'>
                    <span class = 'title'>تســليم الشيفت</span>
                    <div class = 'inputs'>
                        <div class = 'item ' id = 'existed_money'>
                            <i class="fa-solid fa-money-bill-transfer fa-2x"></i>
                            <input class = 'border-light' type = 'number' min = 0 step = '0.1' placeholder = 'النـقود الموجوده في الخزنه'/>
                        </div>

                        <div class = 'item' id = 'gived_money'>
                            <i class="fa-solid fa-handshake fa-2x"></i>
                            <input class = 'border-light' type = 'number' min = 0 step = '0.1' placeholder = 'التسليمــات'/>
                        </div>


                        <div class = 'item' id = 'password'>
                            <i class="fa-solid fa-lock fa-2x"></i>
                            <input class = 'border-light'  type = 'password' placeholder = 'أدخل كــلمة المرور الخاصه ب المدير لتأكيد التسليم'/>
                        </div>
                        
                    </div>

                    <div class = 'btns'>
                        <button id = 'finish' class = 'save border-light'>تســليم</button>
                        <button id = 'close'  class = 'cancel border-light'>إلغـــاء</button>
                    </div>
                </div>
            </div>
        `
        $("body").append(htmx)
    })


    // close the finishing shift page 
    $("body").on("click" , "div.alert[type = 'finish.shift'] > div.container > div.btns > button.cancel" , ()=>{
        $("div.alert").remove()
    })

     // refinishing shift page 
     $("body").on("click" , "div.wrapper > div.navbar > div.section > div.item[type = 'refinish']" , ()=>{
        if (!passwordConfirmed) { 
            $("body").append(passwordPopUp)
        }else { 
            $.ajax({
                                method : "POST"  ,
                                url : "requests" ,
                                data : {"type" : "reshifting"}  , 
                                success  : (e)=>{ 
                                    if (e.state === true )  {
                                        alertBox({message : "تم إعـادة التسليم بنجــاح <br />من فضلك قم ب التسليم مجددا"})
                                    }else { 
                                        alertBox({message : "لا يمكن إعــاده التسليم <br/> من فضلك قم ب تسليم الدرج أولا "})

                                    }
                                }
                    })
        }
      
        
       
    })



    // finishing the sift 
    $("body").on("click" , "div.alert[type = 'finish.shift'] > div.container > div.btns > button.save" , ()=>{
        let Existed_Money = $("div.alert[type = 'finish.shift'] > div.container > div.inputs > div#existed_money > input").val()
        let gived_Money = $("div.alert[type = 'finish.shift'] > div.container > div.inputs > div#gived_money > input").val()
        let password = $("div.alert[type = 'finish.shift'] > div.container > div.inputs > div#password > input").val()

        if (Existed_Money != false) { 

            

            $.ajax({
                method:"POST" ,
                url :"requests" ,
                data : {"type" : "shift.finishing" , "existedMoney" : Existed_Money , "givedMoney" : gived_Money , "password" : password},
                success  :(e)=>{

                    if (e.state === false && e.reason === "invalid.password") { 

                        return alertBox({message : "كلمة المــرور خاطئة , من فـضلك قم بالمــحاوله مجــددا ..." , stopPropagation : 'true'})
                    }else { 

                        setInterval(()=>{
                            window.location.href = "/logout"
                        } , 5000)
                        if(e.OutMoney !== "+") { 
                            alertBox({message  : `انت معجز <span style = 'color :green'>${e.OutMoney}</span> جنيه <br /><i style = 'text-align: center;position: relative;width: 100%;'class="fa-solid fa-face-frown fa-2x"></i></span>`})
                        }else { 
                            alertBox({message  : "مــبروك انت معجزتش إنهــارده فلوس </br><i style = 'text-align: center;position: relative;width: 100%;' class='fa-solid fa-face-grin-beam-sweat fa-2x'></i>"})
    
                        }

                    }
                   


                }
            })




        }
    })



    // restore Receit selled in the same shift 

    $("body").on("click" , "div.navbar > div.section > div#restore_receit" ,()=>{
        console.log("Restoring Receit ...")
    })



    // when click on new receit button on nav bar 

    $("div.wrapper > div.navbar > div.section > div.item[type = 'newReceit']").on("click" , ()=>{
        location.reload()
    })
 
})