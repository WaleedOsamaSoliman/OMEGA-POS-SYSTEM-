const add_user_htmx = `

        <span class = 'title' id = 'title'>
            <i class = 'fa-solid fa-user-plus'></i>
            <span>إضــافه مستخدم جديد </span>
        </span>

        <div class = 'content'>
        
            <div class = 'form'>

                <div class = 'username input'>
                    <i class="fa-solid fa-user"></i>
                    <input class = 'border-light' type ='text' placeholder = 'أدخل اسم المستخدم ....' />
                </div>


                <div class = 'password input'>
                    <i class="fa-solid fa-lock"></i>
                    <input class = 'border-light' type ='password' placeholder = 'أدخل كلمة المرور ....' />
                </div>

                <div class = 'nickname input'>
                    <i class="fa-solid fa-signature"></i>
                    <input class = 'border-light' type ='text' placeholder = 'أدخل الإسم المستعار ....' />
                </div>

                <div class = 'state input'>
                    <i class="fa-solid fa-star"></i>
                    <input class = 'border-light' type ='number' min = 0 max = 1  placeholder = 'أدخل درجة الثقه ....' />
                </div>

                <button class = 'border-light' id = 'add'>إضــافه</button>


            </div>
        </div>
`



const remove_user_htmx = `

        <span class = 'title' id = 'title'>
            <i class = 'fa-solid fa-user-minus'></i>
            <span>حذف مستخدم  </span>
        </span>

        <div class = 'content'>
        
            <div class = 'form'>

                <div class = 'users-list'>
                    <div class = 'option'>
                        <span>waleed</span>
                    </div>
                </div>
               
                <button class = 'border-light' id = 'remove'>حذف</button>

            </div>
        </div>
`

const add_product_htmx  = `
        <span class = 'title' id = 'title'>
                <i class="fa-solid fa-layer-group"></i>
                <span>أضافه صنف جديد </span>
    
        </span>
        <div class = 'content'>
            <div class = 'item' >
                <span>اسم الصنف</span>
                <input placeholder = ''></input>
            </div>
        </div>
        `

const products_htmx = `

        <span class = 'title' id = 'title'>
            <i class="fa-solid fa-layer-group"></i>
            <span>الأصــناف المتوفره</span>

        </span>

        <div class = 'content'>
           <div class = 'btns'>
           
                <div class = 'add-product'>
                        <i class="fa-solid fa-plus"></i>
                        <span>أضـافه صنف</span>
                </div>  

           </div>

            <table class = 'header'>
                <tr>
                    
                    <th type = 'id'>كود الصنف </th>
                    <th type = 'name'>اسم الصنف </th>
                    <th type = 'type'>القسم</th>
                    <th type = 'amount'>الرصيد</th>
                    <th type = 'price'>السعر</th>
                    
                    <th>إضـافه / خصم كميه</th>
                    <th>حفظ</th>
                    <th>حذف</th>
                </tr>



            </table>

            
        </div>
`



const overUser_htmx = `
        <span class = 'title' id = 'title'>
            <i class="fa-solid fa-hand-holding-dollar"></i>
            <span>استــلام الأووفر</span>
        </span>

        <div class  = 'content'> 
            <button class = 'details'>التفاصيل</button>
            <table>
                <tr>
                    <th name = 'username'>اسم المستخدم</th>
                    <th name = 'over-amount'>الأووفر</th>

                </tr>


            </table>

           <div class = 'got'>
                <button>استلام الأووفر</button>
           </div>
        </div>
`


const minusUser_htmx = `
        <span class = 'title' id = 'title'>
        <i class="fa-solid fa-filter-circle-dollar" ></i>
        <span>تعـجيزات المستخدمين</span>
        </span>

        <div class = 'content'>
            <div class = 'type'>
                <span type = 'add.money'>+</span>
                <span type = 'tarabeza'>ترابيزه</span>
                <span type = 'casher'>كاشير</span>
            </div>

           
        </div>


`
$(()=>{


    //when Click on add-product btn >> add new product 

        
    $("body").on("click" , "div.wrapper > div.control-panel > div.content > div.btns > div.add-product"  , (e)=> { 
        
        let name = prompt("أدخل إسم المنتج : ")
        let price = prompt("ادخل سعر المنتج : ")
        let type = prompt(`
            نوع المنتج 

                1 ← منفذ
                2 ← فورم 
                3 ← عروض
                4 ← نوع أخر
        `)

        name = name.trim(" ") ?? "??"
        price = price.trim(" ") ?? "??" 
        type = type.trim(" ") ?? "??" 

        $.ajax({
            method:"POST"  , 
            url :"requests",
            data : {"type" : "add.product" , "name" : name , "price" : price , "type_" : type} , 
            success : (e)=>{
                if (e.state == "200") { 
                    alertBox({message :"تم إضافه الصنف بنجــاح"})
                }else { 
                    if (e.reason == "no.name") { 
                        alertBox({message :"من فضلك قم بإدخــال اسم الصنف"})
                    }else if (e.reason == "no.price") { 
                        alertBox({message :"من فضلك قم بإدخــال سعر الصنف"})
                    }else if (e.reason == "no.type") { 
                        alertBox({message :"من فضلك قم بإدخــال نوع الصنف"})

                    }else if (e.reason == "name.exists")  { 
                        alertBox({message :"هذا الصنف موجود ب الفعل !"})

                    }else if (e.reason == "invalid.price")  {
                        alertBox({message :"سعر الصنف غير صحيح !    "})

                    }else if (e.reason == "invalid.type") {
                        alertBox({message :"نوع الصنف غير صحيح !    "})
                    }
                }
            }
        })
    })


    // when Click on minus Users div show tables

    $("body").on("click" , "div.wrapper > div.navbar > div.settings > div.item > div#minus-user" , (e)=> { 
        $("div.wrapper > div.control-panel").attr("type" , "minus.user").html(minusUser_htmx)

       
    })


    // when click on span of casher or tarabeza to see the minuses
    $("body").on("click" , "div.wrapper > div.control-panel[type ='minus.user'] > div.content > div.type > span" , (e)=>{ 
        $("div.wrapper > div.control-panel[type ='minus.user'] > div.content > div.type > span").removeClass("active")
        $(e.currentTarget).addClass("active")

        let selected = $("div.wrapper > div.control-panel[type ='minus.user'] > div.content > div.type > span.active")
        if (selected.length === 0 ) { 
            return alert("قم ب اختيار القسم الذي تريد ان تري تعجيزات أولا")
        }
        let type = $(selected).attr("type")
        $.ajax({
            method : "POST" , 
            url:"admin-requests", 
            data : {"type" : "minus.users" , "usersClass" : type},
            success : (e)=>{
                if (e.state === true ) { 
                    data = e.data 
                    $("div.wrapper > div.control-panel[type ='minus.user'] > div.content > table").remove()
                    let htmx = `
                        <table>
                            <tr>
                                <th type = 'user'>اسم المستخدم</th>
                                <th type = 'amount'>قيمة العجز</th>
                                <th type = 'edit'>دفع مبلغ</th>
                                <th type = 'save'>حفظ</th>
                            </tr>


                    
                    `
                    for (x of data ) { 
                        htmx += `
                            <tr id = ${x.id}>
                                <th type = 'user'>${x.user}</th>
                                <th type = 'amount'>${x.money}</th>
                                <th type = 'edit'> <input value = 0 min = 0 max = 1000 type = 'number'> </th>
                                <th type = 'save'><i class="fa-solid fa-circle-check fa-2x"></i></th>
                            </tr>
                        `
                    }

                    htmx += "</table>"
                    $("div.wrapper > div.control-panel[type ='minus.user'] > div.content").append(htmx)
                }else { 
                    if (e.reason === "no.users.minus") { 
                        alertBox({message : "لا يوجد ديون علي أي من المستخدمين الحالين"})
                        $("div.wrapper > div.control-panel[type ='minus.user'] > div.content > table").remove()
                    }
                }
            }
        })
        
    })




    // when click on show money button 

    $("body").on("click" , "div.wrapper > div.navbar > div.settings > div.item > div#existed-money " , (e)=> { 
        $.ajax({
            method :"POST",
            url : "admin-requests" , 
            data : {"type" : "show.existed.money"} ,
            success : (e)=>{
                if (e.state === true)  { 
                   alertBox({"message" : `النقود الموجود حاليا ف الدرج : <span style = 'color : green'>${e.money}</span> جنيه`})
                }
            }

        })
    })

    // when click on got the over button do func 


    $("body").on("click" , "div.wrapper  > div.control-panel[type = 'over.user'] >  div.content > div.got > button  " , (e)=> { 
        $.ajax({
            method : "POST" , 
            url : "admin-requests",
            data : {"type" : "dump.over"} , 
            success : (e)=>{ 
                console.log(e)
                if (e.state === true)  {
                    alertBox({message : `من فضلك اسحب مبلغ قدره : <span style = 'color : green'>${e.over}</span>  جنيه من الدرج `})
                    $("div.wrapper  > div.control-panel[type = 'over.user']").html("")
                }
            }
        })
    })
    // display add user page when click on add user span
    $("div.wrapper > div.navbar > div.settings > div.item > div#add-user").on("click" , ()=>{
        $("div.wrapper > div.control-panel").attr("type" , "add.user").html(add_user_htmx)
    })

     // display OverUser page when click on add overuser span
     $("div.wrapper > div.navbar > div.settings > div.item > div#over-user").on("click" , ()=>{
        
        $.ajax({
            method:"POST" , 
            url : "admin-requests" , 
            data : {"type" : "over.users"},
            success : (e)=>{
                if (e.state === true)  {
                    let htmx = ""
                    for (x of e.details) { 
                        htmx += `<tr>
                            <th name = 'username'>${x.name}</th>
                            <th name = 'over-amount'>${x.moneyPlus}</th>
                        </tr>
                        `
                    }
                    htmx += `
                    <tr class = 'total'>
                        <th>الإجمــالي</th>
                        <th name = 'over-amount'>${e.intotal}</th>
                    </tr>
                    `
                    $("div.wrapper > div.control-panel").attr("type" , "over.user").html(overUser_htmx)
                  
                    $("div.wrapper > div.control-panel[type = 'over.user'] >  div.content > table > tbody").append(htmx)
                }else{ 
                    // if (e.reason === "no.over") {
                    alertBox({message : "عذرا لا يوجد أووفر  لكي تقوم بسحبه .. حاول لاحقـا "})
                    // }
                }

               
            }
        })
    })

    // display remove user page when click on remove user span
    $("div.wrapper > div.navbar > div.settings > div.item > div#remove-user").on("click" , ()=>{
        $("div.wrapper > div.control-panel").attr("type" , "remove.user").html(remove_user_htmx)
    })
    


    // pay the minus money when click on check symbol 

    $("body").on("click","div.wrapper > div.control-panel[type = 'minus.user'] > div.content > table tr >th[type = 'save']" , (e)=> { 
        let userType = $(e.currentTarget).closest("table").parent().children("div.type").children("span.active").attr("type")
        let userId = $(e.currentTarget).parent().attr("id")
        let paidValue = $(e.currentTarget).parent().children("th[type = 'edit']").children("input").val()
        if (paidValue <= 0) { 
            return alertBox({message : "القيمة المدفوعه لا ينبغي ان تكون اقل من او تســاوي صفر"})
        }
        let confirming = confirm("هل أنت متأكد من انك تريد حفظ هذه التعديلات ؟؟")
        if (confirming) { 
            $.ajax({
                method : "POST",
                url : "admin-requests" , 
                data : {"type" : "pay.minus" , "usertype" : userType , "userId" : userId , paidValue} , 
                success : (e)=>{
                    console.log(e)
                    if (e.state === true )  { 
                        $("div.wrapper > div.control-panel[type ='minus.user']").html("")
                        alertBox({message : ` تم خصم المبلغ من قيمة العجز لدي المستخدم بنجاح <br />من فضلك قم بوضع هذه النقود ف الدرج (<span style = 'color:green;font-weight:bold;'>${paidValue}</span>) جنيه`})
                    }
                }
            })
        }
        
    })
    
    // function to get all products ordered by specific column
    function getProducts({orderby = "type"}) { 
        $("div.wrapper > div.control-panel").attr("type" , "report.products").html(products_htmx)
        $.ajax({
            method :"POST" ,
            url :"admin-requests" ,
            data : {"type" : "get.all.products", "orderby" : orderby},
            success : (r)=>{
                console.log(r)
                if (r.state === true) { 
                    for (x of r.products ) {
                        if (x.type === 'foram'){
                            x.type ='فورم'
                        }else if(x.type === "manfz") {
                            x.type ="منفذ"
                        }
                        
                        let item = `
                        <tr uid = '${x.id}'>
                            
                            <th type = 'id'>${x.id}</th>
                            <th type = 'name' contenteditable>${x.name} </th>
                            <th type ='type'>${x.type}</th>
                            <th type = 'amount'><input type = 'number' disabled value = ${x.amount}></th>
                            <th type = 'price'><input type = 'number' disabled value = ${x.price}></th>
                            
                            <th type ='modifyAmount'><input type = 'number'  value = 0> </th>
                            <th type = 'save'><i class="fa-solid fa-square-check"></i></th>
                            <th type = 'delete'><i class="fa-solid fa-rectangle-xmark"></i></th>
                        </tr>
                        `

                        $("div.wrapper > div.control-panel[type = 'report.products'] >  div.content > table.header > tbody").append(item)

                    }
                
                    console.log(r.products)
                }
            }
        })
       
        
    }
    
    // display Prodicts  page when click on report produrts  span
    $("div.wrapper > div.navbar > div.settings > div.item > div#report-products").on("click" , ()=>{
        getProducts({orderby : "type"})
    })


    $("body").on("click" , "div.wrapper > div.control-panel[type='report.products'] > div.content > table.header > tbody > tr:nth-child(1) > th" , (e)=>{
        let orderby = $(e.currentTarget).attr("type")
        getProducts({orderby : orderby})

      
        
    })
    
    

    // add new user when click on add Button on add user page ....
    $("body").on("click" ,("div.wrapper > div.control-panel[type = 'add.user'] > div.content > div.form > button ") , (e)=>{

        let username = $(e.currentTarget).parent().children("div.username").children("input").val()
        let password = $(e.currentTarget).parent().children("div.password").children("input").val()
        let nickname = $(e.currentTarget).parent().children("div.nickname").children("input").val()
        let state = $(e.currentTarget).parent().children("div.state").children("input").val()

        if(username.trim(" ") === "" || password.trim(" ") === ""  || nickname.trim(" ") === "" || state.trim(" ") === "") { 
            alertBox({message : "من فضلك قم بإكمال جميع الحقول السابقه أولا !"})
            return false
        }

       
        if (parseInt(state) !== 1) { 
            state = 0
        }

        console.log(state)
        $.ajax({
            method : "POST" ,
            url : "admin-requests",
            data : {"type" : "add.user" , "username" :username , "password" :password , "nickname" :nickname , "state" :state} , 
            success : (r)=>{
                if (r.state === true ) { 
                    alertBox({message : "تم إنشــاء مستخدم جديد بنجاح "})
                    setInterval(()=>{
                        window.location.reload()
                    }, 3000)
                }else { 
                    switch(r.reason) { 
                        case "username.exists":
                            alertBox({message :"اسم المستخدم موجود ب الفعل , قم بإختيـار اسم اخر"})
                            break;
                        case "nickname.exists" :
                            alertBox({message :"أحدهم يستخدم نفس الإسم المستـعار , قم بإختيار اسم اخر"})
                            break;
                    }
                }
            }
        })
        
    })



    // save any changes on specific  row
    
    $("body").on("click"  , "div.wrapper > div.control-panel[type='report.products'] > div.content > table.header > tbody > tr:not(:nth-child(1)) > th[type ='save']" , (e)=>{
        let id = $(e.currentTarget).closest("tr").attr("uid")
        let modifyAmount = $(e.currentTarget).closest("tr").children("th[type = 'modifyAmount']").children("input").val()
        let amount = $(e.currentTarget).closest("tr").children("th[type = 'amount']").children("input").val()
        let price = $(e.currentTarget).closest("tr").children("th[type = 'price']").children("input").val()
        let name = $(e.currentTarget).closest("tr").children("th[type = 'name']").text()
        if (!confirm("هل تود حفظ التعديلات ؟")) { 
            return false
            
        }

        $.ajax({
            method:"POST", 
            url : "admin-requests",
            data : {"type" : "modify.product" , "id" : id , "modifiedAmount" : modifyAmount , "amount" : amount , "price" :price , "name" : name},
            success : (r)=>{
                if(r.state)  {
                    alert("تم تعــديل الصنف بنجــاح")
                    $("div.wrapper > div.navbar > div.settings > div.item > div#report-products").trigger("click")
                }
                console.log(r)
            }
        })
    })



    // enable amount and price input when i double click on it 

    $("body").on("dblclick" , "div.wrapper > div.control-panel[type='report.products'] > div.content > table.header > tbody > tr:not(:nth-child(1)) > th[type ='price']  ,div.wrapper > div.control-panel[type='report.products'] > div.content > table.header > tbody > tr:not(:nth-child(1)) > th[type ='amount'] " , (e)=> { 

        $(e.currentTarget).children("input").removeAttr("disabled").css("background-color" , "green").css("color" , "#fff")
    })


    $("body").on("click" , "div.wrapper > div.control-panel[type='report.products'] > div.content > table.header > tbody > tr:not(:nth-child(1)) > th[type ='delete']"  ,(e)=>{
        if (confirm("هل أنت متأكد من حذف هذا المنتج ؟")) { 
            let id = $(e.currentTarget).closest("tr").attr("uid")
            $.ajax({
                method :"POST",
                url : "admin-requests",
                data : {"type" : "delete.product" , "id" :id},
                success : (e)=>{
                    if (e.state === true) { 
                        alert("تم حذف هذا المنتج بنجــاح")
                        $("div.wrapper > div.navbar > div.settings > div.item > div#report-products").trigger("click")

                    }
                    console.log(e)
                }
            })
        }
    })



    // logout button 

    $("div.wrapper > div.navbar > div.settings > div.item#logout ").on("click" , (e)=>{
        window.location.href = "/logout"

    })
    // reset the Application to the default 
    $("div.wrapper > div.navbar > div.settings > div.item[type='config'] > div#reset").on("click" , ()=>{
       if(!passwordConfirmed) { 
            $("body").append(passwordPopUp)
       }else { 
        $.ajax({
            method :"POST" ,
            url : "admin-requests",
            data  :{"type" : "reset.default"},
            success : (e)=>{
                alert("تم إعــادة ظبط المصنع بنجــاح ")
                setTimeout(()=>{
                    window.location.href = "/logout"
                } , 3000)
            }
        })
       }

    })
    
})