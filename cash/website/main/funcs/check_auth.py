from ..models import Accounts  
def check(request) : 
    username = request.session.get("username")
    password = request.session.get("password")
    if username == None or password == None : 
        print(username , password)
        return {"state" : False}
    
    else : 
        checking = Accounts.objects.all().filter(username = username , password = password)
        count = checking.count()

        if count : 
            if (checking[0].state == 1) :
                return {"state" : True , "type" : "admin"}
            else : 
                return {"state" : True , "type" : "normal"}
        else : 
            return {"state"  : False}
        