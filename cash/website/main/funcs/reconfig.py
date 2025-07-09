from ..models import FinishingHistory , Accounts , receits , deletedReceits , Employees , Shift_Finishing , Products , gavedMoney ,inOutEmployeeHistory


def reset(finishing_history = True , amounts  = True , accounts  = True , products = True , receites  = True , givenMoney = True  , deletedReceites = True , inOutEmployee = True  , finishing = True)  : 
    if amounts  :
        r = Products.objects.all()
        for x in r  : 
            x.amount = 0
            x.save()
        del r
        
    if receites : 
        # delete all receits on the Database 

        r = receits.objects.all()
        r.delete()
        del r
  
    if deletedReceites  : 
        
        # delete all deleted receits on the database 

        r = deletedReceits.objects.all()
        r.delete()
        del r


    if products : 
        # delete all products on the database

        r = Products.objects.all()
        r.delete()
        del r

    if givenMoney : 
        # delete all gaved Money in the database 
    
        r = gavedMoney.objects.all()
        r.delete()
        del r 
    
    
    if inOutEmployee  :
        # delete all inOutEmployeeHistory in the database 
    
        r = inOutEmployeeHistory.objects.all()
        r.delete()
        del r 
    
    
    
    if accounts : 
        
        # delete all Employees in the database

        r = Employees.objects.all()
        r.delete()
        del r

        # delete all Accounts in the database 

        r = Accounts.objects.all()
        r.delete()
        del r
        
        # create default super user
        
        r  = Accounts(username  = "0" , password = "yasminsabry" , state = 1 , Nickname  = "وليد")
        r.save()
        del r 
        r = Employees(nickname = "وليد" , username = "0")
        r.save()
        del r
    



    if finishing : 
           # delete all Records in Finishing table in the database 

            r = Shift_Finishing.objects.all()
            r.delete()
            del r
            # create zero record in the finishing table
            r= Shift_Finishing(totalMoney = 0 , password = 'yasminsabry')
            r.save()
            del r
    
    
    if finishing_history : 
        # delete all Records in Finishing History table in the database 
        r = FinishingHistory.objects.all()
        r.delete()
        del r     
    
