from ..models import Accounts  , Shift_Finishing


def login(  username , password , request   ) : 
    if username or password != None : 
        user = Accounts.objects.all().filter(username = username ,password = password)
        if user.count() == 1 : 
            state = user[0].state
            if state != 1 : 
                
                # if Shift_Finishing.objects.all()[0].finishing == False and  Accounts.objects.all()[0].username != username  : 
                #     return {"state" : False , "reason" : "finishing.problem"}
                pass
            return {"state" : True ,  "accountType" : state}
        else : 
            return {"state" : False , "reason" :"" }
      
    