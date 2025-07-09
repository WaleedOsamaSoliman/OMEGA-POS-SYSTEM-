from django.shortcuts import render  , HttpResponse , redirect
from django.http import JsonResponse
from .funcs import check_auth , ajax , print_receipt , reconfig 
from django.views.decorators.csrf import csrf_exempt
from .models import  finishDay,  booking_bank, marakez_booking, marakez_names , marakez_receits ,  marakez_products,tarabeza_users, AmountAdjusting, gotOver ,Products , receits , FinishingHistory,  Shift_Finishing , Accounts , Employees  , deletedReceits , gavedMoney , inOutEmployeeHistory
import json
import datetime as dt

from django.utils import timezone 
# Create your views here.


def index(request) : 
    if check_auth.check(request)['state'] : 
        if check_auth.check(request)['type'] == "admin" : 
             return redirect("panel")
        else : 
            try : 
                
                r = Shift_Finishing.objects.all()[0]
                r.finishing = False 
                r.save()
            except Exception as ex :
                print("→ "   , ex) 
                
            return render(request , "index.html" , {})
    else : 
        # check_auth(request)
        return redirect("login")
    
def panel (request) : 
        
        if check_auth.check(request)['state'] : 
            if check_auth.check(request)['type'] == 'admin' : 
                return render(request , "panel.html" , {})
            else : 
                 return redirect("index")
        else : 
             return redirect("login")    

   
def login(request) : 

    if check_auth.check(request)['state'] : 
        if check_auth.check(request)['type'] == "admin" : 
            return redirect("panel")
            pass
        else : 

            r = Shift_Finishing.objects.all()[0]
            r.finishing = False 
            r.save()
            return redirect("index")
    else : 
        return render(request , "login.html" , {})


def logout(request) : 
    if request.session.get("username") != None and request.session.get("password") != None : 
        del request.session['username']
        del request.session['password']
        return redirect("login")
    else : 
        return redirect("login")

@csrf_exempt
def requests(request) : 

    if request.method == "POST" : 

        # add product request

        if request.POST.get("type") == "add.product"  : 
            name = request.POST.get("name") or "??"
            price = request.POST.get("price") or "??"
            type_ = request.POST.get("type_") or "??"


            if name == "??"  :
                return JsonResponse({"state" : "400" , "reason" : "no.name"})
            if price == "??" :
                return JsonResponse({"state" : "400" , "reason" : "no.price"})
            if type_ == "??" : 
                return JsonResponse({"state" : "400" , "reason" : "no.type"})
            
            # check if the product is Exists :
            all_products = Products.objects.all()
            for x in all_products : 
                if x.name.strip(" ") == name : 
                     return JsonResponse({"state" : "400" , "reason" : "name.exists"})
            try :
                price = int(price) 
            except ValueError : 
                return JsonResponse({"state" : "400" , "reason" : "invalid.price"})
            
            if type_ not in ["1" , "2" , "3" , "4"] : 

                return JsonResponse({"state" : "400" , "reason" : "invalid.type"})
            
            match type_ : 
                case "1" : 
                    type_ = "manfz"
                    
                case "2" : 
                    type_  = "foram"
                case "3" : 
                    type_ = "offers" 
                case "4" : 
                    type_ = "others"
                
            # add the Product 
            r = Products(name = name , price = price , amount = 0 , type = type_)
            r.save()
            return JsonResponse({"state" : "200" })


        # marakez Requests Start 

        elif request.POST.get("type") == "get.marakez.names" : 
            products = []
            for x in  marakez_names.objects.all().order_by("id") : 
                products.append({"name" : x.name , "id" : x.id })

            return JsonResponse({ "state" : True, "data" : products})

        if request.POST.get("type") == "get.marakez.products" : 
            products = []
            for x in  marakez_products.objects.all().order_by("name") : 
                products.append({"name" : x.name , "price" : x.price , "id" :x.id})

            return JsonResponse({"data" : products})
        


        if request.POST.get("type") == "booking" : 
            
            dist = (request.POST.get("dist"))
            paid = float(request.POST.get("paid"))
            remainning = float(request.POST.get("remainning"))
            required = float(request.POST.get("required"))
            notes = request.POST.get("notes")
            products = json.loads(request.POST.get("products"))
         
            products_list = []
            prices_list = []
            amounts_list = []
            for x in (products): 
                products_list.append(str(x['uid']))
                prices_list.append(str(x['price']))
                amounts_list.append(str(x['amount']))
            

            products_list = ",".join(products_list)
            prices_list = ",".join(prices_list)
            amounts_list = ",".join(amounts_list)
            if paid == required : 
                state = True
            else : 
                state = False
            r = marakez_booking(BookerName = marakez_names.objects.all().filter(id = dist)[0].name ,
                                intotal = required ,
                                paid = paid ,
                                remainning = remainning,
                                amounts = amounts_list , 
                                products = products_list, 
                                prices = prices_list ,
                                seller = Accounts.objects.all().filter(username = request.session.get("username"))[0].Nickname,
                                state = state,
                                notes = notes
                                
                                  )
            
            r.save()
            del r
            # add money to the booking bank table : 

            r = booking_bank.objects.all()
            if r.count() == 0 : 
                i = booking_bank(intotal = 0)
                i.save()
                del i
            
            r = r[0]
            r.intotal += paid 
            r.save()
            del r


            return JsonResponse({"state" : True })
        


        # booking   Query and fetch all booking from db
        if request.POST.get("type") == "booking.query" : 
            r = marakez_booking.objects.all().order_by('id').filter(delivered = False)
            if r.count() ==  0 : 

                return JsonResponse({"state" : False , "reason" : "no.booking"})
            data = []
            for x in r : 
                products = x.products.split(",")
                names = []
                amounts = []
            
                for u,j in enumerate(products) : 
                    a =  marakez_products.objects.all().filter(id = j)[0].name  + " " + f"[{x.amounts.split(",")[u]}]"
                    names.append(a)


                print("→" , names)
                names = " + ".join(names)
            

                
                data.append({ "id" : x.id , "booker"  : x.BookerName ,  "products" : names , "paid" : x.paid , "required" : x.intotal , "remainning" : x.remainning , "notes" : x.notes , "state" : x.state ,"date" : x.Date ,  "time" : x.time })
           
            return JsonResponse({"state" : True , "data" : data})
            pass


        # pay.remain money of booking 

        if request.POST.get("type") == "booking.pay.remain" : 
            id = request.POST.get("id")
            r = marakez_booking.objects.all().filter(id = id)
            if r.count() == 0 : 
                return JsonResponse({"state" : False , "reason" : "no.booking.found"})
            remainning = r[0].remainning
            if remainning == float(0) : 
                return JsonResponse({"state": False , "reason" : "no.remainning"})
            else : 
                i = booking_bank.objects.all()[0]
                i.intotal = i.intotal + remainning
                i.save()
                del i 
                

                r.update(remainning = 0 , state = True , paid = r[0].paid  + remainning)
                r[0].save()
                del r 
                return JsonResponse({"state" : True , "remainning" : remainning})
            
        # save booking item (deliver item)
        if request.POST.get("type") == "save.booking" : 


            id = request.POST.get("id")
            r = marakez_booking.objects.all().filter(id = id)
            if r[0].remainning != 0 : 
                return JsonResponse({"state" : False , "reason" : "pay.remainning.first"})
            if r.count() == 0 : 
                return JsonResponse({"state" : False , "reason":"no.booking.found"})
            if r[0].delivered == True : 
                return JsonResponse({"state" : False , "reason" : "already.delivered"})
            r.update(delivered = True)
            r[0].save()
            intotal = r[0].intotal
            del r 
            # minus the money from the bank
            r = booking_bank.objects.all()[0]
            r.intotal -= intotal
            r.save()
            del r
            return JsonResponse({"state" : True , "required" : intotal})

        if request.POST.get("type") == "booking.total.money" : 
            r = booking_bank.objects.all()[0]
            return JsonResponse({"state" : True , "intotal" : r.intotal})
        if request.POST.get("type") == "marakez.receit.save" : 
                data= request.POST.get("data")
                data = json.loads(data)
                receit_products = data['receit_products']
                total_money = data['total_money']
                products = []
                amounts = []
                prices = []
                for x in receit_products : 
                    products.append(x['uid'])
                    amounts.append(str(x['amount']))
                    prices.append(str(x['price']))
                    item = Products.objects.all().filter(id = x['uid'])

                
                products = ",".join(products)
                amounts = ",".join(amounts)
                prices = ",".join(prices)
                seller = Accounts.objects.all().filter(username = request.session.get("username"))[0].Nickname
                r = marakez_receits(products = products , amounts = amounts , prices = prices , intotal = total_money , seller = seller)
                r.save()
                receitId = r.id
                
                return JsonResponse({"state" : True , "receitId" : receitId})






        # marakez Requests End 



      
        if request.POST.get("type") == "login" : 
            username = request.POST.get("username") 
            password = request.POST.get("password")
            if ajax.login(username, password , request)['state'] == True : 
                # print(request.session.items())
                request.session['username'] = username 
                request.session['password'] = password 
                request.session['state'] = ajax.login(username, password , request)['accountType']


                return JsonResponse({"state" : True})
            else : 
                if ajax.login(username , password , request)['reason'] == "finishing.problem" : 
                    return JsonResponse({"state" : False  , 'reason' : "finishing.problem"})
                else :
                    return JsonResponse({"state" : False })
        
        # get all prodcuts from the database
        elif  request.POST.get("type") == "get.all.products" : 
                products = []
                for x in  Products.objects.all().order_by("name") : 
                    products.append({"name" : x.name , "price" : x.price , "id" :x.id , "rtype" :x.type})

                return JsonResponse({"data" : products})
        elif request.POST.get("type") == "get.offers.products" : 
                products = []
                for x in  Products.objects.all().filter(type = "offers").order_by("name") : 
                    products.append({"name" : x.name , "price" : x.price , "id" :x.id , "rtype" : x.type})

                return JsonResponse({"data" : products})
        
        # get only products with type 'foram' from the database
        elif  request.POST.get("type") == "get.foram.products" : 
                products = []
                for x in  Products.objects.all().filter(type = "foram").order_by("name") : 
                    products.append({"name" : x.name , "price" : x.price , "id" :x.id , "rtype" : x.type})

                return JsonResponse({"data" : products})
        

        # get only products with type 'manfaz' from the database
        elif  request.POST.get("type") == "get.manfaz.products" : 
                products = []
                for x in  Products.objects.all().filter(type = 'manfz').order_by("name") : 
                    products.append({"name" : x.name , "price" : x.price , "id" :x.id , "rtype" : x.type})

                return JsonResponse({"data" : products})
        

        elif request.POST.get("type") == "receit.save" : 
             
                data= request.POST.get("data")
                data = json.loads(data)
                receit_products = data['receit_products']
                total_money = data['total_money']
                isbonus = data['isbonus'] or 0 
                products = []
                amounts = []
                prices = []
                rtypes = []
                for x in receit_products : 
                    products.append(x['uid'])
                    amounts.append(str(x['amount']))
                    prices.append(str(x['price']))
                    rtypes.append(str(x['rtype']))
                    item = Products.objects.all().filter(id = x['uid'])
                    currentAmount = item[0].amount - x['amount']
                    item.update(amount = currentAmount)

                
                products = ",".join(products)
                amounts = ",".join(amounts)
                prices = ",".join(prices)
                rtypes = ",".join(rtypes)
                
                seller = Accounts.objects.all().filter(username = request.session.get("username"))[0].Nickname
                r = receits(products = products , amounts = amounts , prices = prices ,rtype = rtypes, intotal = total_money , seller = seller , isbonus = isbonus)
                r.save()
                receitId = r.id
                

                # ADD the total Money to finishing shift table 
            
                ft = Shift_Finishing.objects.all().filter()
                # add the receit Total Money to the Shift total Money 
                tm = ft[0].totalMoney
                tm += total_money
                ft.update(totalMoney = tm)

                # Increase the receits Number by 1 
                nr = ft[0].ReceitsCount
                nr += 1
                ft.update(ReceitsCount = nr)
                del ft 
                del nr 
                del r 
                # ft.update(totalMoney += total_money)


                # increment the Number of receites saled by person by 1
                r = Employees.objects.all().filter(username = request.session.get("username"))[0]
                r.receitsCount += 1
                r.save()
                del r 


                # change the current user in the finishing shift table

                r = Shift_Finishing.objects.all()[0]
                r.user = Accounts.objects.all().filter(username = request.session.get("username"))[0].Nickname
                r.save()
                del r


                            
                return JsonResponse({"state" : True , "receitId" : receitId , "isbonus" : isbonus})
        
        elif request.POST.get("type") == "shift.finishing" : 


            existedMoney = request.POST.get("existedMoney")
            givedMoney = request.POST.get("givedMoney")
            password = request.POST.get("password")

            
            if password != Shift_Finishing.objects.all()[0].password :  
                 return JsonResponse({"state" : False , "reason" : "invalid.password"})

            #  get the all money of the shift
            AllMoney = Shift_Finishing.objects.all()[0].totalMoney
            AllMinusMoney = 0
            if existedMoney == "" : 
                 existedMoney = 0
            if givedMoney == "" : 
                 givedMoney = 0
            inOutMoney = (float(existedMoney) + float(givedMoney) - float(AllMinusMoney)) - float(AllMoney) 
          
          
            # record the inOut to the refinishing Histroy 
            r = FinishingHistory(user = request.session.get("username") , existedMoney = AllMoney  , gavedMoney = givedMoney, inOutUser = inOutMoney  )
            r.save()
            del r
            
            
            # add the finishing details to the db

            user = request.session.get("username")


            r = Employees.objects.all().filter(username = user)[0]
          
            
            if inOutMoney >= 0 : 
                r.MoneyPlus += inOutMoney
                r.save()
            else : 
                r.MoneyMinus += inOutMoney
                r.save()

           

            r = Shift_Finishing.objects.all()[0]
            r.totalMoney += inOutMoney
            r.totalMoney -= float(givedMoney) #minus the money u gaved  also 
            r.save()
            del r
            # r = Shift_Finishing.objects.all()[0]
            # r.finishing = True
            # r.save()
            # del r

            r = Shift_Finishing.objects.all()[0]
            r.ReceitsCount = 0
            r.save()
            del r

            user = Accounts.objects.all().filter(username = request.session.get('username'))[0].Nickname
            r = Shift_Finishing.objects.all()[0]
            r.user = user 
            r.save()
            del r 

            if int(givedMoney) != 0  : 
                 
                user = Accounts.objects.all().filter(username = request.session.get("username"))[0].Nickname
                r = gavedMoney(intotal = float(givedMoney) , gaver =  user )
                r.save()
                del r 
                del user


            # record the inOut History in the database 
            r = inOutEmployeeHistory(seller = Accounts.objects.all().filter(username = request.session.get("username"))[0].Nickname , inOutMoney  = inOutMoney , existedMoney = existedMoney , totalMoney = AllMoney , givenMoney = givedMoney )
            r.save()
            del r
            
           


            if (inOutMoney < 0) :
                
                 inOutMoney = abs(inOutMoney)
                 return JsonResponse({"state" : True , "OutMoney" : inOutMoney})
            else : 
                return JsonResponse({"state" : True , "OutMoney" : "+" , "over":inOutMoney })



        elif request.POST.get("type") == "day.back" :


            yesterdayDetails = finishDay.objects.all().order_by("-id")[0]
            initialMoney= float(yesterdayDetails.initialMoney)
            systemMoney = float(yesterdayDetails.systemMoney)

            all_receits = receits.objects.filter(state = True).order_by("-id")
            breakPoint = all_receits[0].id
            startPoint = all_receits[1].id


            startpointcheck = receits.objects.filter(id = startPoint)
               
            if len(startpointcheck) != 1 : 
                return JsonResponse({"state" : "400" , "reason" : "invalid.startpoint" }) 

        
            
            # timeofstartpoint = timeofstartpoint[0].Date
            # print((now - timeofstartpoint).total_seconds())

            # get all receits starting from the startpoint 
            print("collecting ")
            all_receites = receits.objects.filter(id__gte = int(startPoint)).filter(id__lte = int(breakPoint)).filter(state =False).order_by("rtype")

        



            total = 0
            for x in all_receites : 
                total += x.intotal
                print(x)

            items_id  = []
            items_amount = []
            names = []

            for x in all_receites  : 
                subitems = x.products
                subitems = subitems.split(",")
                subamounts = x.amounts 
                subamounts = subamounts.split(",")

                for y,j in enumerate(subitems)  : 
                    if j in items_id : 
                        index = items_id.index(j)
                        subamountsIndex = subitems.index(j)

                        items_amount[index] += int(subamounts[subamountsIndex])
                    else : 
                        items_id.append(j)
                        
                        items_amount.append(int(subamounts[y]))


            for x in items_id : 
                names.append(Products.objects.filter(id = int(x))[0].name)


            bankMoney = Shift_Finishing.objects.all()[0].totalMoney

            products_ = []
                
            items_prices = []
            for x,y in enumerate(items_id) : 
                itemId = int(y) 
                itemPrice  = Products.objects.filter(id = itemId)[0].price
                itemAmount = items_amount[x] 
                itemName = Products.objects.filter(id = itemId)[0].name

                products_.append({"name" : itemName , "amount" : itemAmount , "price" : itemPrice , "total" : int(itemAmount) * float(itemPrice)} )





            # print(breakPoint , startPoint)
            return JsonResponse({"state" : "200"  , "products" : products_ ,  "systemMoney" : systemMoney  , "initialMoney" : initialMoney , "itemsTotal":total} ) 

            # return JsonResponse({"state" : "200"})
        elif request.POST.get("type") == "end.day" :
                startpoint = int(request.POST.get("startpoint"))
                totalmoney_ = int(request.POST.get("totalmoney"))


                startpoint = int(receits.objects.all().filter(state = True).order_by("-id")[0].id)
                totalmoney_ = float(Shift_Finishing.objects.all()[0].totalMoney)

                # now = timezone.now().strftime("%Y%m%d")
                startpointcheck = receits.objects.filter(id = startpoint)
               
                if len(startpointcheck) != 1 : 
                    return JsonResponse({"state" : "400" , "reason" : "invalid.startpoint" }) 

               
                
                # timeofstartpoint = timeofstartpoint[0].Date
                # print((now - timeofstartpoint).total_seconds())

                # get all receits starting from the startpoint 
                print("collecting ")
                all_receites = receits.objects.filter(id__gte = int(startpoint)).filter(state =False).order_by("rtype")

               



                total = 0
                for x in all_receites : 
                    total += x.intotal
                    print(x)

                items_id  = []
                items_amount = []
                names = []

                for x in all_receites  : 
                    subitems = x.products
                    subitems = subitems.split(",")
                    subamounts = x.amounts 
                    subamounts = subamounts.split(",")

                    for y,j in enumerate(subitems)  : 
                        if j in items_id : 
                            index = items_id.index(j)
                            subamountsIndex = subitems.index(j)

                            items_amount[index] += int(subamounts[subamountsIndex])
                        else : 
                            items_id.append(j)
                            try : 

                                items_amount.append(int(subamounts[y]))
                            except Exception as ex :
                                items_amount.append(0)
                                print("[!] Fetal Error : " ,  ex)


                print("[INFO] : items_id --> " , str(items_id))
                for x in items_id : 
                    try : 
                        x = int(x)
                    except Exception as ex  : 
                        x = 0

                    # CHECK FIRST IF THE ITEM IS EXISTS 
                    print("[INFO] item id : " ,x )
                    if Products.objects.filter(id=int(x)).first() :
                        names.append(Products.objects.filter(id = int(x))[0].name)

                    else : 
                        names.append("صنف محذوف ")


                bankMoney = Shift_Finishing.objects.all()[0].totalMoney

                over = 0
                if float(totalmoney_) == float(bankMoney) : 
                    over = 0
                elif float(totalmoney_) > bankMoney :
                    over  = float(totalmoney_) - float(bankMoney)
                else : 
                    print("Something Wrong !")
                    over = float(totalmoney_) - float(bankMoney)

                    
                products_ = []
                    
                items_prices = []
                for x,y in enumerate(items_id) : 
                    try : 
                        y = int(y)
                    except Exception as ex : 
                        y = 0 
                        print("[!][INFo] --> " , ex)
                    itemId = int(y) 

                    itemCheck = Products.objects.filter(id = itemId).first()
                    if itemCheck : 

                        itemPrice  = Products.objects.filter(id = itemId)[0].price
                        itemAmount = items_amount[x]  
                        itemName = Products.objects.filter(id = itemId)[0].name 
                    else : 
                        itemPrice  = 0
                        itemAmount = 0
                        itemName = "صنف غير معروف"

                    products_.append({"name" : itemName , "amount" : itemAmount , "price" : itemPrice , "total" : int(itemAmount) * float(itemPrice)} )

                return JsonResponse({"state" : "200"  , "products" : products_ ,  "bank_money" : bankMoney , "over" : over , "totalMoney" : totalmoney_ , "itemsTotal":total} ) 
 
        elif request.POST.get("type") == "restore.receit" : 
             
            receit_Number = request.POST.get("receitNumber")
            state = request.session.get("state")
            if receit_Number == "" or receit_Number == None : 
                return JsonResponse({"state" : False , "reason" : "no.receit.number"})

            r = receits.objects.all().filter(id = int(receit_Number))   
            if r.count() == 0 : 
                  return JsonResponse({"state" : False , "reason" : "not.found"})
            
          
            if state == 0 : 
                 pass
                #if dt.date.today() != r[0].Date : 
                    #return JsonResponse({"state" : False , "reason" : "out.of.date"})
                
            products = r[0].products.split(",")
            prices = r[0].prices.split(",")
            amounts = r[0].amounts.split(",")
            total_money = r[0].intotal
            names = []
            for x in products : 
                names.append(Products.objects.all().filter(id = x)[0].name)
            

            return JsonResponse({"state" : True , "products" : products  , "names" : names , "amounts" : amounts , "prices" :prices , 'intotal' : total_money })
            
        elif  request.POST.get("type") == "receit.delete" : 


             receitNumber = int(request.POST.get("receitNumber"))
             seller = request.session.get("username")
             seller = Accounts.objects.all().filter(username = seller )[0].Nickname
            #  r = receits.objects.all().filter(id = receitNumber)[0]

             r = receits.objects.all().filter(id = receitNumber)
             if r.count() == 0 : 
                  return JsonResponse({'state' : False , "reason" : "not.found"})
             del r
             r = receits.objects.all().filter(id = receitNumber)[0]

             if r.seller != seller : 
                  return JsonResponse({"state" : False , "reason" : "not.seller"})
             else : 

                receitPrice = receits.objects.all().filter(id = receitNumber)[0].intotal
                intotal = Shift_Finishing.objects.all()[0].totalMoney

                if intotal - receitPrice < 0 : 
                     return JsonResponse({"state" : False , "reason" : "not.enough.money.to.restore"})
                
                del receitPrice
                del intotal



                r = receits.objects.all().filter(id = receitNumber)[0]
                
                r = deletedReceits(uid = receitNumber , seller = seller , products = r.products , amounts = r.amounts , prices = r.prices , intotal = r.intotal)
                r.save()
                del r
                
                receit_total_money = receits.objects.all().filter(id = receitNumber)[0].intotal
                r = Shift_Finishing.objects.all()[0]
                r.totalMoney -= receit_total_money
                r.save()

                del  r
                del receit_total_money

                

                # Adjust amounts of restored Products

                r = receits.objects.all().filter(id = receitNumber)[0]
                products = r.products.split(",")
                amounts = r.amounts.split(",")

                for x,y in zip(products , amounts)  :
                    # print("☼" , x , y)
                    j = Products.objects.all().filter(id = x)[0]
                    j.amount += int(y) 
                    j.save()
                del products
                del amounts
                del r 

                # Final step --> Deleting the receit 
                r = receits.objects.all().filter(id = receitNumber)[0]
                r.delete()
                del r


                
                return JsonResponse({"state" : True })
            #  #########

        elif request.POST.get("type") == "confirm.password.root" : 
            password = request.POST.get("password") 
            if password == Shift_Finishing.objects.all()[0].password : 
                return JsonResponse({"state" : True})
            else : 
                return JsonResponse({"state" : False}) 
        elif request.POST.get("type") == "print.receipt" : 
            receitId = request.POST.get("receitId")
            isbonus = request.POST.get("isbonus") or 0
            receipt = receits.objects.all().filter(id = receitId)[0]
            
            products = receipt.products.split(",")
            amounts = receipt.amounts.split(",")
            seller =  receipt.seller 
            prices = receipt.prices.split(",")
            rtypes = receipt.rtype.split(",")
            total = receipt.intotal

          
            data =[]
            for x,y in enumerate(products) : 
                data.append({"name" : Products.objects.all().filter(id = y)[0].name , "amount" : amounts[x] , "price" : prices[x]})
           
            print("→ " , data)
            print_receipt.receipt(id_ = receitId , seller = Accounts.objects.all().filter(username = request.session.get("username"))[0].Nickname , data_ = data , intotal = total , isbonus = isbonus)
            #check if this receipt is foram type and Print Receit to it !!! ::::
            
            foramProducts = []
            for x  , y in enumerate(rtypes) : 
                if y == "foram" : 
                    # print("Catch 1 foram Product ...")
                    foramProducts.append({"name" : Products.objects.all().filter(id = products[x])[0].name ,"amount" : amounts[x] })
                    # print(foramProducts)
            
            if len(foramProducts) != 0 :          
                print_receipt.copy_receipt(id_ = receitId , seller =  Accounts.objects.all().filter(username = request.session.get("username"))[0].Nickname , data_ = foramProducts)
           
                
                         
                
                
                
            
           
            return JsonResponse({"state" : True})
        
        elif request.POST.get("type") == "new.day" : 

            breakpoint_ = receits.objects.all().order_by("-id")[0].state 
            if  breakpoint_ : 
                return JsonResponse({"state" :"400" , "reason" : "no.sales"}) 


            myMoney = float(request.POST.get("mymoney"))
            systemMoney = float(Shift_Finishing.objects.all()[0].totalMoney)
            salesMoney = float(request.POST.get("totalSales"))

            if salesMoney > systemMoney :
                return JsonResponse({"state" : "400" , "reason" : "not.enough.money"})
            
            else :
                over = salesMoney - systemMoney 
                # add break point 

                i = receits(state = True )
                i.save()
                # dump the money of sales 
                r= Shift_Finishing.objects.all()
                if r.count() == 1 : 
                    # print(f"Editetd Emoney to → {eMoney}")
                    r[0].delete()
                    del r 
                    r = Shift_Finishing(totalMoney = systemMoney-salesMoney , user = Accounts.objects.all().filter(username = request.session.get("username"))[0].Nickname)
                    r.save()
                    del r 

                    # save some details  in finish day table 
                    print("my breakpoint is : " , breakpoint_)
                    r = finishDay(totalSales = salesMoney , systemMoney = systemMoney , initialMoney = float(systemMoney - salesMoney) , breakPoint = receits.objects.all().order_by("-id")[0].id)
                    r.save()
                    return JsonResponse({"state" : "200" })
                    

            # print(myMoney , systemMoney , salesMoney)
            return JsonResponse({"state" : "200" })
        

        elif request.POST.get("type") == "sales_print" : 
                    d =json.loads(request.POST.get("data_"))
                    print(d)
                    print_receipt.print_total_day_sales(seller = "waleed"  , data_ = d , intotal = request.POST.get("intotal"))
                    return JsonResponse({"state" : "200"})
        elif request.POST.get("type") == "reshifting"  : 
            
            try : 
                #remove the added money to the user
                r = FinishingHistory.objects.latest("id")
            
                if request.session.get("username") == r.user : 
                    # gMoney = r.gavedMoney 
                    eMoney = r.existedMoney
                    inOutMoney  = r.inOutUser
                    # print("Existed Money > > "  + str(eMoney))
                    r.delete()
                    del r
                    r= Shift_Finishing.objects.all()
                    if r.count() == 1 : 
                        # print(f"Editetd Emoney to → {eMoney}")
                        r[0].delete()
                        del r 
                        r = Shift_Finishing(totalMoney = eMoney , user = Accounts.objects.all().filter(username = request.session.get("username"))[0].Nickname)
                        r.save()
                        del r 
                        # remove the gaved money from the table 
                        r = gavedMoney.objects.latest("id")
                        if r.gaver == Accounts.objects.all().filter(username = request.session.get("username"))[0].Nickname : 
                            r.delete()
                        
                            print("Deleting the Previous Gaved Money ")
                        del r     
                        # remove the IN OUT FROM THE Employee
                        print(f"Removing money : {inOutMoney} from the Employee ")
                        r= Employees.objects.all().filter(username = request.session.get("username"))[0]
                        if inOutMoney > 0 : 
                            r.MoneyPlus -= inOutMoney 
                        else : 
                            r.MoneyMinus -= inOutMoney
                        r.save()
                        del r 
                        
                        # remove record from inOutEmployeeHistory
                        r = inOutEmployeeHistory.objects.latest("id")
                        if r.seller == Accounts.objects.all().filter(username = request.session.get("username"))[0].Nickname  : 
                            r.delete()
                        return JsonResponse({"state" : True})
                    else : 
                        print("NO shift finishing table Existed to be edited in refinishing table !")
                        return JsonResponse({"state" : False})
                    
                else : 
                    print("Not youuuuuuuuu !")
                    return JsonResponse({"state" : False})
            except Exception as ex : 
                print(f"→ Error : {ex}")
                return JsonResponse({"state" : False})

                
            return JsonResponse({"state" : True})
            pass
   
        else : 
            return JsonResponse({"" : ""})
        
    
        
    else : 
        if request.GET.get("type") == "calculate" : 
            fromValue = request.GET.get("from") or "??"
            toValue = request.GET.get("to")or "??"
            if fromValue == "??" or toValue == "??" : 
                return JsonResponse({"state" : "400" , "reason" :"missing parameeter"})
            
            all_receits  = receits.objects.filter(id__gte = fromValue).filter(id__lte = toValue)
            total = 0
            for x in all_receits : 
                total += x.intotal

            print(f"total money from {fromValue} to {toValue } is {total}")
        
        elif request.GET.get("type") == "classes" : 
            fromValue = request.GET.get("from") 
            toValue = request.GET.get("to")
            all_receits  = receits.objects.filter(id__gte = fromValue).filter(id__lte = toValue).filter(state = False)
            items_id  = []
            items_amount = []

            for x in all_receits  : 
                subitems = x.products
                subitems = subitems.split(",")
                subamounts = x.amounts 
                subamounts = subamounts.split(",")

                for y,j in enumerate(subitems)  : 
                    if j in items_id : 
                        index = items_id.index(j)
                        subamountsIndex = subitems.index(j)

                        items_amount[index] += int(subamounts[subamountsIndex])
                    else : 
                        items_id.append(j)
                        
                        items_amount.append(int(subamounts[y]))

                names = []

                print(items_amount)
                # for x in items_id : 
                   
                #     itemName = Products.objects.filter(id = int(x))[0].name
                #     itemPrice = Products.objects.filter(id = int(x))[0].price
                #     theindex = items_id.index(x)
                #     itemAmount = items_amount.index(int(theindex))
                #     print(f"{itemName} selled {itemAmount} by {int(itemPrice)*int(itemAmount)}")

                #     names.append(itemName) 
                # print(names)


            return HttpResponse(f"all items : {items_id} , all_amounts : {items_amount} , items Names : {names}")

                


        
        return JsonResponse({"" : ""})
    

@csrf_exempt

def marakez(request) : 
    return render(request , "marakez.html" , {})
@csrf_exempt
def admin_requests(request) : 
    if request.method != "POST" : 
          return JsonResponse({"" :""})
     
    rtype = request.POST.get("type")
#   #########################################
                # Add new User #
#   #########################################
    if rtype == "add.user" : 


        username = request.POST.get("username")
        password = request.POST.get("password")
        state = request.POST.get("state")
        nickname = request.POST.get("nickname")

        if username == None or password == None or nickname == None or state == None : 
            return JsonResponse({"state" : False , "reason" : "incomplete.data"})   
         

       
        if int(state) != 1 : 
             state = 0

        if Accounts.objects.all().filter(username = username ).count() != 0 : 
            return JsonResponse({"state" : False , "reason" : "username.exists"})   
         
        if Accounts.objects.all().filter(Nickname = nickname).count() != 0 : 
            return JsonResponse({"state" : False , "reason" : "nickname.exists"})    
         
        nickname = nickname.lower()
        username = username.lower()
        # add to Accounts table 

        r = Accounts(username = username , password = password  , state = state , Nickname = nickname)
        r.save()
        del r 
        r = Employees(username = username , nickname = nickname  )
        r.save()
        del r
        return JsonResponse({"state" : True })

    elif rtype == "over.users" : 
        print("Getting OvER .USERS ")
        r = Accounts.objects.all().filter(state = 0 )
        if r.count() != 0  :
        
            totalOver = float(0)
            details = []
            for x in r : 
               
                uid = x.username 
                i  = Employees.objects.all().filter(username = uid)[0]
                moneyPlus = i.MoneyPlus
                nickname = i.nickname
                if float(moneyPlus) > 0 : 
                    totalOver += float(moneyPlus)
                    details.append({"name" : nickname , "moneyPlus" : moneyPlus })
            
            if totalOver > 0 : 
                return JsonResponse({"state" : True , "details" : details , "intotal" : totalOver})
            else : 
                return JsonResponse({"state" : False , "reason" : "no.over"})
        print("nO ...")
        return JsonResponse({"state" : False , "reason" : ""} )
    elif rtype == "dump.over" : 
        users = Accounts.objects.all().filter(state = 0)
        intotal  = float(0)
        for x in users : 
            i = Employees.objects.all().filter(nickname = x.Nickname)[0]
            intotal += i.MoneyPlus 
            i.MoneyPlus = float(0) 
            i.save()
        r = Shift_Finishing.objects.all()
        r.update(totalMoney = r[0].totalMoney - intotal)
        r[0].save()
        
        # add over to the history table
        
        del r 
        r  = gotOver(user = Accounts.objects.all().filter(username = request.session.get('username'))[0].Nickname , over = intotal)
        r.save()
        
        return JsonResponse({"state" : True , "over"  : intotal })
        
    elif rtype == "get.all.products" : 
      
        products = []
        orderby = request.POST.get("orderby")

        if orderby not in  [x.name for x in Products._meta.get_fields()] : 
             orderby = "name"


        if orderby == "type" : 
            allP = Products.objects.all().order_by('type')
        elif orderby == "name" : 
            allP = Products.objects.all().order_by('name')
        elif orderby == "id" : 
            allP = Products.objects.all().order_by('id')
        elif orderby == "price" : 
           allP = Products.objects.all().order_by('price')  
        elif orderby == "amount" : 
            allP = Products.objects.all().order_by('amount')

       
       
        if allP.count() == 0 : 
             return JsonResponse({"state" : False , "reason" : "no.products.exists"})
        
        for x in allP : 
            products.append({"name" : x.name , "price" :x.price , "amount" : x.amount , "id" :x.id , "type" :x.type})

        return JsonResponse({"state" : True , "products" : products})
        
    elif rtype == "modify.product" : 
        try : 
            productId = request.POST.get("id")
            productAmount = int(request.POST.get("amount"))
            productModifiedAmount = int(request.POST.get("modifiedAmount"))
            productName = request.POST.get("name")
            productPrice = request.POST.get("price")
        except : 
            return JsonResponse({"state" :False , "reason" : "invalid.amounts.or.prices"})

        if bool(productName) == False or bool(productPrice) == False : 
            return JsonResponse({"state" : False , "reason" : "no.name.or.price"})
        
        r = Products.objects.all().filter(id = productId)[0]
        
        r.amount = productAmount
        r.amount += productModifiedAmount
        r.name = productName
        r.price = productPrice
        r.save()
        del r
        
        
        # save the changes in adjust table in the db 
        r = AmountAdjusting(product = Products.objects.all().filter(id = productId)[0].name, user = Accounts.objects.all().filter(username = request.session.get("username"))[0].Nickname , amount = productAmount , adjustedAmount = productModifiedAmount  ,  )
        r.save()
        return JsonResponse({"state" : True })

    elif rtype == "delete.product" : 
        try : 
            uid = int(request.POST.get("id"))
        except : 
            return JsonResponse({"state" : False , "reason" :"invalid.id"})
        r = Products.objects.all().filter(id = uid)
       
        if r.count() != 1 : 
            return JsonResponse({"state" : False , "reason" : "no.product.found"})
        r[0].delete()
        del r
        return JsonResponse({"state" : True })
    
    elif rtype == "reset.default" : 
        reconfig.reset(products = False ,  accounts = False)
        print("Resetting to default ....")
        return JsonResponse({"state" : True})
    
    elif rtype == 'minus.users' : 
        userClass = request.POST.get("usersClass")
        if userClass == None : 
            return JsonResponse({"state" : False , "reason" : "unknown.users.Class"})     
        
        data  = []
        if userClass == "casher" : 
            r = Employees.objects.all().filter(MoneyMinus__lt = 0).values()
            if len(r) == 0 : 
                return JsonResponse({"state" : False  , "reason" : "no.users.minus"})      

            for x in r : 
                data.append({ "id" :  x['id'] , "user" : x['nickname'] ,  "money" : abs(x['MoneyMinus'])})
            pass 
        if userClass == "tarabeza" : 
            r = tarabeza_users.objects.all().filter(inOutUser__gt = 0).values()
            if len(r) == 0 : 
                return JsonResponse({"state" : False  , "reason" : "no.users.minus"})      

            for x in r : 
                data.append({ "id" :  x['id'] , "user" : x['user'] ,  "money" : x['inOutUser']})
            # print( "→", data)
            pass
        return JsonResponse({"state" : True  , "data" : data})      
    
    elif rtype == "show.existed.money" : 
        money = Shift_Finishing.objects.all()[0].totalMoney
        return JsonResponse({"state" : True  , "money" : money})      

    elif rtype == "pay.minus" :
        userType = request.POST.get("usertype")
        userId = request.POST.get("userId")
        paidValue = float(request.POST.get('paidValue'))
        print(userType)
        if userType == "casher" : 
            r = Employees.objects.all().filter(id = userId)[0]
          
            r.MoneyMinus += paidValue
            r.save()
            del r 
            r = Shift_Finishing.objects.all()[0]
            r.totalMoney += paidValue
            r.save()
            pass 
        elif userType == "tarabeza" : 
            r = tarabeza_users.objects.all().filter(id = userId)[0]
            r.inOutUser -= paidValue
            r.save()
            del r 
            r = Shift_Finishing.objects.all()[0]
            r.totalMoney += paidValue
            r.save()
            pass
        

        return JsonResponse({"state" : True})

    else : 
         return JsonResponse({"state" : False , "reason" : "unknown.request"})      