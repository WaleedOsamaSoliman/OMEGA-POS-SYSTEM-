$(()=>{

    function login() { 
        let username = $("input#username").val()
        let password = $("input#password").val()
        username  = username.trim()
        password = password.trim()
        $.ajax({
            method : "POST" , 
            url : "requests" , 
            data : {'type' : "login" , "username" : username , "password"  : password} , 
            success : (e)=>{
                console.log(e)
                if (e.state === true) { 
                    window.location.href = "/"
                }else { 
                    if (e.reason === "finishing.problem") { 
                        alertBox({message : "المــستخدم السابق لم يقم بتسليم الدرج "  , type  : "finishing-error"})
                    }else { 
                        alertBox({message : "اسم المستــخدم او كلمة المــرور خــاطئه"  , type  : "login-error"})
                    }  
                }
            },error : (err)=>{ 

            }
        })
    }

    // Check login Function !!

    $("body").on("click" , "button#login" , (e)=>{
         login()
    })


    // end Check login Function !



    // login when click on enter key

    $("body").on("keypress"  , "div.login-form" , (e)=>{
        if (e.key === "Enter") { 
            if($("div.alert").length !== 0) { 
                $("div.alert").remove()
            }else { 
                login()
            }
        }
    })



})