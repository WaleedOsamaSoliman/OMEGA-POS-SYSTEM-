
//python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 > dump.json
//python -Xutf8  manage.py dumpdata > output.json
var receit_products = [];
var intotal  = 0;
$(()=>{








    $("body").on("click"  , "div.item-ctrl > span.bonus", (e)=> { 
        $(e.currentTarget).toggleClass("active")
        if ($(e.currentTarget).hasClass("active")) { 
            $("div.skeleton > div.receit > div.items > span.title").html("فاتورة بيع (<span style ='color: limegreen;font-weight : bold'>مسحوبات أمناء الشرطه</span>)")
        }else { 
            $("div.skeleton > div.receit > div.items > span.title").html("فاتورة بيع") 
        }
    })

    $("div.navbar > div.section > div#logout").on("click" , ()=>{
        console.log("Clicked !")
        alertBox({message : "هل أنت مـتأكد من أنك تريد الــخروج من الــبرنــامج ؟" ,redbtn : "لا"  , greenbtn : "نعم" , type  :"logout"})
    })


    $("body").on("click" , "div.alert[type = 'confirm.end.day'] button#print" , (e)=>{

        // print($("body > div.alert[type ='confirm.end.day'] "))

        let data = []
        let items = $("body > div.alert[type='confirm.end.day'] > table tr:not(:nth-child(1))")
        let intotal  = $("body > div.alert[type='confirm.end.day'] > div.info  > div.sales  >span").text()
        for (x of items ) { 
            let name = $(x).children("th.name").text().trim()
            let amount = $(x).children("th.amount").text().trim()
            let price = $(x).children("th.price").text().trim()
            let total = $(x).children("th.total").text().trim()
            console.log(name , amount , price ,total)
            data.push({"name" : name , "amount" : amount , "price" : price , "total" : total})

        }
        console.log(data)
       $.ajax({
            method:"POST" , 
            url : "requests" ,  
            data : {"type" : "sales_print" , "data_" : JSON.stringify(data)   , "intotal" : intotal } , 
            success : (e)=>{
                console.log(e)
            }
       })
    })

    $("div.navbar > div.section > div#booking").on("click" , ()=>{
        window.location.href = "/marakez"

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

   



  
    // Get all products when click on any Category
  
    $("div.sub-classes > div.items > span.item").on("click" , (e)=>{
        if ($(e.currentTarget).hasClass("active")) { 
            return  false
        }else { 
            $("div.sub-classes > div.items > span.item").removeClass("active")
            $(e.currentTarget).addClass("active")
        }


        let id = $(e.currentTarget).attr('id')

        $.ajax({
            method:"POST",
            url:"requests",
            data : {"type" : `get.${id}.products`},
            success : (e)=>{

                $("div.classes > div.items-rect").html("")
                for (x of e.data) { 
                    
                    let item = ` <div uid = ${x.id} type = "${x.rtype}" Pname = '${x.name}' price = ${x.price} class = 'item border-light'>
                                    <span class = 'name'>${x.name}</span>
                                    <span class = 'price'>${x.price}</span>
                                </div> `
                    $("div.classes > div.items-rect").append(item) 
                }
            }
        })
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
                    <span class="amount">${x.amount}</span>
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
        $("div.item-ctrl > span.bonus").removeClass("active")
        $("div.skeleton >  div.receit > div.items > span.title ").html("فاتورة بيع")
        
        refresh_receit()

    }




    // add product to the receit 

    $("body").on("click" , "div.items-rect > div.item" , (e)=> { 
        let id = $(e.currentTarget).attr("uid")
        let name = $(e.currentTarget).attr("Pname")
        let price = $(e.currentTarget).attr("price")
        let rtype = $(e.currentTarget).attr("type")
       
        if (receit_products.length !== 0) { 
            let ids = []
            for (x of receit_products) { 
                ids.push(x.uid)
            }
            if (ids.includes(id)) { 
                index = ids.indexOf(id)
                receit_products[index].amount += 1
            }else { 
                receit_products.push({"uid" : id , "name" : name , "price" : price , "amount" : 1 , "rtype" : rtype})
            }

        
        }else { 
            receit_products.push({"uid" : id , "name" : name , "price" : price , "amount" :1 , "rtype" : rtype})
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

    // save the current receit 
    $("div.receit >  div.btns > button.save").on("click" , ()=>{ 
 
        saveFun()
    })

    // save the current receit if u click on Enter Button 

    $("body").on("keypress" , (e)=>{
        if (e.key === "Enter") { 
        //    saveFun()
        }
    })


    $("body").on("click" ,  "div.alert button#close" ,  (e)=>{
        $("div.alert").remove()
    })


      // confirm saving the current receit
    $("body").on("click" , "div.alert[id = 'save.recent.receit'] > div.messageBox > div.btns > button.green" , ()=> { 
        isbonus = $("div.item-ctrl > span.bonus.active").length
       
        $.ajax({
            method:"POST", 
            url :"requests" ,
            data : {"type" : "receit.save" , "data" : JSON.stringify({"receit_products" : receit_products, "total_money" : intotal , "isbonus" : isbonus})},
            success : (r)=>{
                console.log(r)
                let receitId = r.receitId
                let isbonus = r.isbonus
                $.ajax({
                    method : "POST" ,
                    url : "requests" , 
                    data : {"type" : "print.receipt"  , "receitId" : receitId , "isbonus" : isbonus} , 
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
                            if (Number(e.over) == 0)  { 
                                alertBox({message  : "مــبروك انت معجزتش إنهــارده فلوس </br><i style = 'text-align: center;position: relative;width: 100%;' class='fa-solid fa-face-grin-beam-sweat fa-2x'></i>"})

                            }else {
                                alertBox({message  : ` مــبروك انت معجزتش إنهــارده فلوس </br>[الأوفر هو '  <span style='color:green;'>${Number(e.over)}</span>  '] جنيه مصري </br><i style = 'text-align: center;position: relative;width: 100%;' class='fa-solid fa-face-grin-beam-sweat fa-2x'></i>`})

                            }
    
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


    $("body").on("click" , "div.alert[type = 'confirm.end.day'] > button#day-back" , ()=>{
        $.ajax({
            method:"POST",
            url : "requests" , 
            data : {"type" : "day.back"},
            success : (e)=>{
                if (e.state == "200") { 
                    $("body > div.alert[type='confirm.end.day'] > table  tr:not(:nth-child(1))").remove()
                    let rows = ""
                    for (x of e.products){
                        product_name = x.name 
                        product_price = x.price 
                        product_amount = x.amount 
                        total = x.total
                        // console.log(product_amount)
                        rows+=`
                        <tr>
                            <th>${product_name}</th>
                            <th>${product_amount}</th>
                            <th>${product_price}</th>
                            <th>${total}</th>

                        </tr>
                            `

                    }
                    $("body > div.alert[type = 'confirm.end.day'] > table").append(rows)
                    $("body > div.alert[type = 'confirm.end.day'] >  div.end").remove()
                    $("body > div.alert[type = 'confirm.end.day'] >  div.total").remove()
                    $("body > div.alert[type = 'confirm.end.day'] >  div.info > div.moneyBank > span").text(`كان${e.systemMoney}`)
                    $("body > div.alert[type = 'confirm.end.day'] >  div.info > div.sales > span").text(`كان${e.itemsTotal}`)
                    $("body > div.alert[type = 'confirm.end.day'] >  div.info > div.mymoney > span").text(`كان${e.initialMoney}`)
                    
                }
            }
        })
    })
    $("body").on("click"  , "div.alert[type = 'confirm.end.day'] > div.end > button#finish" , ()=>{ 
        let conf = confirm("هل أنت متأكد من أنك تريد بدأ يوم جديد ؟")
        if (conf) {
            console.log("starting new day ...")
            let totalSales = $("div.alert[type= 'confirm.end.day'] > div.info > div.sales > span").text()
            let bankMoney = $("div.alert[type= 'confirm.end.day'] > div.info > div.mymoney > span").text()



            $.ajax({
                method:"POST" ,
                url : "requests" ,
                data : {"type" : "new.day" , "totalSales" : totalSales , "mymoney" : bankMoney} , 
                success : (e)=>{
                    if (e.state === "400") { 
                        if (e.reason === "not.enough.money") { 
                            return alertBox({message : "النقود الحاليه غير كافيه لسداد مبيعات اليوم .. يجب دفع العجز أولا " })

                        }else if (e.reason === "no.sales") {
                            return alertBox({message : "تم ب الفعل تسليم الدرج ولا يوجد أي مبيعات  حــتي الأن"})

                        }
                    }else { 
                        
                        return alertBox({message : "تم تسليم اليوم بنجــاح وبدأ يوم جديد " })

                    }
                }
            })
        }
    })



    // when click on new receit button on nav bar 

    $("div.wrapper > div.navbar > div.section > div.item[type = 'newReceit']").on("click" , ()=>{
        location.reload()
    })
 

    $("div.wrapper > div.navbar > div.section > div.item[type='end.day']").on("click" , ()=>{
      
        if (!passwordConfirmed) { 
            $("body").append(passwordPopUp)

        }else { 
            let htmx = `
                <div class = 'alert' type = 'end.day'>
                    <div class = 'container'>
                        <span class="title">تســليم اليوم بالكامل</span>
                        <div class="inputs">
                            <div class="item " id="start-point" style = 'display:none;'>
                                <i class="fa-solid fa-money-bill-transfer fa-2x"></i>
                                <input class="border-light" type="number" min="0"  value = 0 placeholder="رقم أول فاتوره تم بيعها في اليوم">
                            </div>

                            <div class="item" id="intotal" style = 'display:none'>
                                <i class="fa-solid fa-handshake fa-2x"></i>
                                <input class="border-light" type="number" min="0" value = 1 step="0.1" placeholder="اجمالي النقود ف الدرج">
                            </div>


                          
                        </div>

                        <div class="btns">
                            <button id="finish" class="save border-light">تقفيل اليوم</button>
                            <button id="close" class="cancel border-light">إلغـــاء</button>
                        </div>
                    </div>
                </div>
            `
            $("body").append(htmx)
        }
        $("div.alert[type = 'end.day'] button#finish").on("click" , (e)=>{
            let startpoint = $(e.currentTarget).closest("div.alert").find("div#start-point").children("input").val() ?? "";
            let totalmoney = $(e.currentTarget).closest("div.alert").find("div#intotal").children("input").val() ?? "";
            if (startpoint == "" || totalmoney == "") { 
                alert("مشكلة في المدخلات برجاء ادخال قيم صحيحه")
                return false
            }
            $.ajax({
                method:"POST" , 
                url:"requests",
                data : {"type" : "end.day" , "startpoint" : startpoint , "totalmoney" : totalmoney } , 
                success : (e)=>{
                    $("div.alert").remove()
                    rows = ""
                    if (e.products.length == 0 ) { 
                        rows = `<tr style ="height: 100%;
                                            font-weight: bold;
                                            font-size: 2.5rem;
                                            background: radial-gradient(#00ffd9, #00ff13);">
                            <th>لا</th>
                            <th>يوجد</th>
                            <th>مبيعات</th>
                            <th>اليوم</th>
                        </tr>`
                    }else { 
                        for (x of e.products){
                            product_name = x.name 
                            product_price = x.price 
                            product_amount = x.amount 
                            total = x.total
                            // console.log(product_amount)
                            rows+=`
                            <tr>
                                <th class = 'name'>${product_name}</th>
                                <th class = 'amount'>${product_amount}</th>
                                <th class = 'price'>${product_price}</th>
                                <th class = 'total'>${total}</th>
    
                            </tr>
                                `
    
                        }
    
                    }
              
                    // for (x of e.products){
                    //     product_name = x.name 
                    //     product_price = x.price 
                    //     product_amount = x.amount 
                    //     total = x.total
                    //     // console.log(product_amount)
                    //     rows+=`
                    //     <tr>
                    //         <th>${product_name}</th>
                    //         <th>${product_amount}</th>
                    //         <th>${product_price}</th>
                    //         <th>${total}</th>

                    //     </tr>
                    //         `

                    // }
                    let htmx = `
                        <div class  = 'alert' type = 'confirm.end.day'>
                            <button id = 'close'><i class = 'fa-solid fa-xmark fa-2x'></i></button>
                            <button id = 'day-back'>يومية اليوم السابق</button>


                            <div class = 'total'>إجمــالي : ${e.itemsTotal} جنيه </div>
                            <table>
                                <tr>
                                    <th>اسم الصنف </th>
                                    <th>عدد القطع </th>
                                    <th>سعر القطعه</th>
                                    <th>اجمالي المبيعات</th>
                                </tr>
                                    ${rows}
                            </table>
                            <div class = 'info'>
                                <div class = 'moneyBank'>اجمالي النقدية علي السيتسم <span>${e.bank_money} </span></div>
                                <div class = 'sales'>اجمالي مبيعات اليوم <span>${e.itemsTotal}</span></div>

                                <div class = 'mymoney'>الرصيد الإفتتاحي سيصبح  <span>${e.totalMoney - e.itemsTotal}</span></div>



                            </div>

                            <div class = 'end'>
                                <button id  = 'finish'>بدأ يوم جديد</button>
                                <button id  = 'print'>طباعه</button>
                            </div>
                        </div>
                    `
                    $("body").append(htmx)
                    console.log(e)
                }
            })
        })
    })
})