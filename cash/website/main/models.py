from django.db import models
import datetime
from django.utils import timezone   
from django import forms

# Create your models here.
def date_now() : 
    return datetime.datetime.now()
    


class Accounts(models.Model) : 
    id = models.AutoField(primary_key= True , verbose_name = "id")
    username = models.CharField(max_length = 50 , verbose_name = "Username")
    password = models.CharField(max_length = 50 , verbose_name = "Password" )
    state = models.IntegerField(verbose_name = "State" ,  default = 0)
    Nickname = models.CharField(max_length = 50 , verbose_name = "Nickname"  , default = "user" )

    class Meta :

        verbose_name_plural = "Accounts"
        # widgets = {"password" , forms.PasswordInput()}


class Products(models.Model) : 

    id = models.AutoField(primary_key= True , verbose_name= "id")
    #id = models.IntegerField( verbose_name= "id")س
    name = models.CharField(max_length = 50 , verbose_name = "Product Name" , unique = True)
    price = models.FloatField(verbose_name = "Price" )
    amount = models.IntegerField(verbose_name = "amount" )
    type = models.CharField(max_length=9,choices=( ("manfz", "Manfaz" ),("foram", "Foram" ) , ("offers" , "offers") , ("others" , "others") ),default="manfz")

    class Meta: 
        verbose_name_plural = "Products" 


class receits(models.Model) : 
    id = models.AutoField(primary_key= True , verbose_name = "id")
    products = models.CharField(max_length = 50 , verbose_name = "Products")
    amounts = models.CharField(max_length = 50 , verbose_name = "Amounts")
    prices =  models.CharField(max_length = 50 , verbose_name = "Prices")
    rtype = models.CharField(max_length= 150 , verbose_name = "Types" , default = '--')
    intotal = models.FloatField(verbose_name = "Total Money" , default = 0)
    seller = models.CharField(verbose_name = "Seller" , max_length = 50 , default = 'unknwon')
    Date = models.DateField(verbose_name = 'Date' ,  default = date_now())
    time = models.TimeField(verbose_name = "Time"  , default = timezone.now())
    dateTime = models.DateTimeField(verbose_name = "DateTime" , default = timezone.now())
    isbonus = models.BooleanField(verbose_name="Bonus" , default = False)
    state = models.BooleanField(verbose_name = "Starting Point" ,default = False)
    
    
    
    class Meta :
        verbose_name_plural = "Receits"


class Shift_Finishing(models.Model) : 

    id = models.AutoField(primary_key= True , verbose_name = "id")
    totalMoney = models.FloatField( verbose_name = "Total Money" , default = 0)
    user = models.CharField(max_length = 50 , verbose_name = "Current User" , default = 'default')
    ReceitsCount = models.IntegerField(verbose_name = "No of Receits "  , default = 0)
    finishing = models.BooleanField(verbose_name = 'Finishing State' , default = False )
    password = models.CharField(verbose_name= "Password" ,  max_length= 50, default = "parrot" )

    class Meta :
        verbose_name_plural = "Shift Finishing"
        # widgets = {"password" : forms.PasswordInput()}


class Employees(models.Model)  : 
    
    id = models.AutoField(primary_key= True , verbose_name = "id")
    username = models.CharField(verbose_name = "Username" , max_length = 50 , default = '', unique = True)
    nickname = models.CharField( verbose_name = "Nickname", max_length = 50 , default = '' , unique = True)
    MoneyPlus = models.FloatField( verbose_name = "Money (+)" , default = 0)
    MoneyMinus = models.FloatField( verbose_name = "Money (-)" , default = 0)

    receitsCount = models.IntegerField(verbose_name = "No of Receits " , default = 0)
    class Meta :
        verbose_name_plural = "Employees"

class deletedReceits(models.Model)  : 
    
    id = models.AutoField(primary_key= True , verbose_name = "id")
    uid = models.IntegerField(verbose_name = "UID" , unique = True)
    products = models.CharField(max_length = 50 , verbose_name = "Products" , default = "")
    amounts = models.CharField(max_length = 50 , verbose_name = "Amounts" , default= "")
    prices =  models.CharField(max_length = 50 , verbose_name = "Prices" , default = "")
    intotal = models.FloatField(verbose_name = "Total Money" , default = 0)
    Date = models.DateField(verbose_name = 'Date' ,  default = date_now())
    time = models.TimeField(verbose_name = "Time"  , default = timezone.now())
    seller = models.CharField(verbose_name = "Seller" , max_length = 50 , default = 'unknwon')

    class Meta :
        verbose_name_plural = "Deleted Receits"




class gavedMoney(models.Model)  : 
    
    id = models.AutoField(primary_key= True , verbose_name = "id")
    intotal = models.FloatField(verbose_name = "Money" , default = 0)
    Date = models.DateField(verbose_name = 'Date' ,  default = date_now())
    time = models.TimeField(verbose_name = "Time"  , default = timezone.now())
    gaver = models.CharField(verbose_name = "Gaver" , max_length = 50 , default = 'default')

    class Meta :
        verbose_name_plural = "Gaved Money"


class inOutEmployeeHistory(models.Model)  : 
    
    id = models.AutoField(primary_key= True , verbose_name = "id")
    
    inOutMoney = models.FloatField(verbose_name = "IN / OUT Money" , default = 0)
    Date = models.DateField(verbose_name = 'Date' ,  default = date_now())
    existedMoney = models.FloatField(verbose_name = "Bank Money" , default = 0 )
    totalMoney =  models.FloatField(verbose_name = "Device Money" , default = 0)
    givenMoney = models.FloatField(verbose_name = "Given Money"  , default = 0)
    time = models.TimeField(verbose_name = "Time"  , default = timezone.now())
    seller = models.CharField(verbose_name = "Seller" , max_length = 50 , default = 'default')

    class Meta :
        verbose_name_plural = "IN/OUT Employee History"


class FinishingHistory(models.Model)  : 
    id = models.AutoField(verbose_name  = "ID" , primary_key= True )
    user = models.CharField(verbose_name= "Casher Name" , max_length=45 , default = "default")
    Date = models.DateField(verbose_name = 'Date' ,  default = date_now())
    time = models.TimeField(verbose_name = "Time"  , default = timezone.now())
    existedMoney = models.FloatField(verbose_name = "Existed Money" , default = 0)
    gavedMoney = models.FloatField(verbose_name = "Gaved Money" , default = 0)
    inOutUser = models.FloatField(verbose_name = "IN / OUT Money" , default = 0)
    

    class Meta :
        verbose_name_plural = "End Shifting History"




class tarabeza_users(models.Model)  : 
    id = models.AutoField(verbose_name  = "ID" , primary_key= True )
    user = models.CharField(verbose_name= "Tarbeza User" , max_length=45 , default = "default")
    inOutUser = models.FloatField(verbose_name = "IN / OUT Money" , default = 0)
    

    class Meta :
        verbose_name_plural = "Tarbeeza Users"






class gotOver(models.Model)  : 
    id = models.AutoField(verbose_name  = "ID" , primary_key= True )
    user = models.CharField(verbose_name= "Tarbeza User" , max_length=45 , default = "default")
    over = models.FloatField(verbose_name = "Over Money" , default = 0)
    Date = models.DateField(verbose_name = 'Date' ,  default = date_now())
    time = models.TimeField(verbose_name = "Time"  , default = timezone.now())
    
    class Meta :
        verbose_name_plural = "Over Hitsory"
        
        
class AmountAdjusting(models.Model) : 
    id = models.AutoField(verbose_name  = "ID" , primary_key= True )
    user = models.CharField(verbose_name= "Supervisor" , max_length=45 , default = "default")
    product = models.CharField(verbose_name= "Product Name" , max_length=45 , default = "default")
    amount = models.IntegerField(verbose_name = "Current amount")
    adjustedAmount = models.IntegerField(verbose_name = "Adjusted amount")
    Date = models.DateField(verbose_name = 'Date' ,  default =date_now() )
    time = models.TimeField(verbose_name = "Time"  , default = timezone.now())
    
    class Meta :
        verbose_name_plural = "Amount Adjusting"
        
        
# ###################################################

class marakez_products(models.Model) : 
    id = models.AutoField(primary_key= True , verbose_name= "id")
    name = models.CharField(max_length = 50 , verbose_name = "Product Name" , unique = True)
    price = models.FloatField(verbose_name = "Price" )
    amount = models.IntegerField(verbose_name = "amount" )
   

    class Meta: 
        verbose_name_plural = "Markez Products" 



class marakez_receits(models.Model) : 
    id = models.AutoField(primary_key= True , verbose_name = "id")
    products = models.CharField(max_length = 50 , verbose_name = "Products")
    amounts = models.CharField(max_length = 50 , verbose_name = "Amounts")
    prices =  models.CharField(max_length = 50 , verbose_name = "Prices")
    intotal = models.FloatField(verbose_name = "Total Money" , default = 0)
    seller = models.CharField(verbose_name = "Seller" , max_length = 50 , default = 'unknwon')
    Date = models.DateField(verbose_name = 'Date' ,  default = date_now())
    time = models.TimeField(verbose_name = "Time"  , default = timezone.now())
    
    
    class Meta :
        verbose_name_plural = "Marakez Receits"



class marakez_names(models.Model) : 
    id = models.AutoField(primary_key= True , verbose_name = "id")
    name = models.CharField(max_length = 50 , verbose_name = "Products")
    
    
    
    class Meta :
        verbose_name_plural = "Marakez Names"



class marakez_booking(models.Model) : 
    id = models.AutoField(primary_key= True , verbose_name = "id")
    BookerName = models.CharField(max_length = 50 , verbose_name = "Booker Name")
    products = models.CharField(max_length = 50 , verbose_name = "Products")
    amounts = models.CharField(max_length = 50 , verbose_name = "Amounts")
    prices =  models.CharField(max_length = 50 , verbose_name = "Prices")
    intotal = models.FloatField(verbose_name = "Total Money" , default = 0)
    seller = models.CharField(verbose_name = "Seller" , max_length = 50 , default = 'unknwon')
    paid = models.FloatField(verbose_name = "Paid Money" , default = 0)
    remainning = models.FloatField(verbose_name = "Remainning Money" , default = 0)
    Date = models.DateField(verbose_name = 'Date' ,  default = date_now())
    time = models.TimeField(verbose_name = "Time"  , default = timezone.now())
    notes = models.TextField(verbose_name = "Notes"  , default = '--')
    state = models.BooleanField(verbose_name= "State" , default = False)
    delivered = models.BooleanField(verbose_name = "Delivered" , default = False)
    
    
    class Meta :
        verbose_name_plural = "Marakez Booking :)"


class booking_bank(models.Model) : 
    id = models.AutoField(primary_key= True , verbose_name = "id")
    intotal = models.FloatField(verbose_name = "Total Money" , default = 0)
   
    
    
    class Meta :
        verbose_name_plural = "(: Booking Bank :)"



class finishDay(models.Model) : 
    id = models.AutoField(primary_key= True , verbose_name = "id")
    totalSales = models.FloatField(verbose_name = "Total Sales" , default = 0)
    systemMoney = models.FloatField(verbose_name = "POS Money" , default = 0)
    initialMoney = models.FloatField(verbose_name = "Initial Money will be" , default = 0)
    Date = models.DateField(verbose_name = 'Date' ,  default =timezone.now())
    time = models.TimeField(verbose_name = "Time"  , default = timezone.now())
    dateTime = models.DateTimeField(verbose_name = "DateTime" , default = timezone.now())
    breakPoint =  models.IntegerField(verbose_name = "Break Point" , default = 0)

    
    
    class Meta :
        verbose_name_plural = "Finish Day"
