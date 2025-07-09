from django.contrib import admin
from .models import finishDay,booking_bank , marakez_booking,  marakez_names, marakez_receits , marakez_products , AmountAdjusting,gotOver ,tarabeza_users , Accounts , FinishingHistory , Products , receits , Shift_Finishing , Employees , deletedReceits , gavedMoney , inOutEmployeeHistory
# Register your models here.

class AccountsAdmin(admin.ModelAdmin) : 
    list_display  = [x.name for x in Accounts._meta.get_fields()] 
    
    pass
admin.site.register(Accounts , AccountsAdmin)


class dayFinish(admin.ModelAdmin) : 
    list_display  = [x.name for x in finishDay._meta.get_fields()] 
    
    pass
admin.site.register(finishDay , dayFinish)


class ProductsAdmin(admin.ModelAdmin) : 
    list_display = [x.name for x in Products._meta.get_fields()]

admin.site.register(Products , ProductsAdmin)


class receitsAdmin(admin.ModelAdmin) : 
    list_display = [x.name for x in receits._meta.get_fields() ]

admin.site.register(receits , receitsAdmin)

class FinishingAdmin(admin.ModelAdmin) : 
    list_display = [x.name for x in Shift_Finishing._meta.get_fields() ]

admin.site.register(Shift_Finishing , FinishingAdmin)


class EmployeesAdmin(admin.ModelAdmin) : 
    list_display = [x.name for x in Employees._meta.get_fields() ]

admin.site.register(Employees , EmployeesAdmin)

class deletedAdmin(admin.ModelAdmin) : 
    list_display = [x.name for x in deletedReceits._meta.get_fields() ]

admin.site.register(deletedReceits , deletedAdmin)

class gavedMoneyAdmin(admin.ModelAdmin) : 
    list_display = [x.name for x in gavedMoney._meta.get_fields() ]

admin.site.register(gavedMoney , gavedMoneyAdmin)





class inOutHistoryAdmin(admin.ModelAdmin) : 
    list_display = [x.name for x in inOutEmployeeHistory._meta.get_fields() ]

admin.site.register(inOutEmployeeHistory , inOutHistoryAdmin)




class FinishingHistoryAdmin(admin.ModelAdmin) : 
    list_display = [x.name for x in FinishingHistory._meta.get_fields() ]

admin.site.register(FinishingHistory , FinishingHistoryAdmin )






class tarabeza_usersAdmin(admin.ModelAdmin) : 
    list_display = [x.name for x in tarabeza_users._meta.get_fields() ]

admin.site.register(tarabeza_users , tarabeza_usersAdmin )





class over_admin(admin.ModelAdmin) : 
    list_display = [x.name for x in gotOver._meta.get_fields() ]

admin.site.register(gotOver , over_admin )


class adjusting_admin(admin.ModelAdmin) : 
    list_display = [x.name for x in AmountAdjusting._meta.get_fields() ]

admin.site.register(AmountAdjusting , adjusting_admin )




# MARAKEZ 

class marakez_products_admin(admin.ModelAdmin) : 
    list_display = [x.name for x in marakez_products._meta.get_fields() ]

admin.site.register(marakez_products , marakez_products_admin )




class marakez_receits_admin(admin.ModelAdmin) : 
    list_display = [x.name for x in marakez_receits._meta.get_fields() ]

admin.site.register(marakez_receits , marakez_receits_admin )



class marakez_names_admin(admin.ModelAdmin) : 
    list_display = [x.name for x in marakez_names._meta.get_fields() ]

admin.site.register(marakez_names , marakez_names_admin )



class marakez_booking_admin(admin.ModelAdmin) : 
    list_display = [x.name for x in marakez_booking._meta.get_fields() ]

admin.site.register(marakez_booking , marakez_booking_admin )



class booking_bank_admin(admin.ModelAdmin) : 
    list_display = [x.name for x in booking_bank._meta.get_fields() ]

admin.site.register(booking_bank , booking_bank_admin )
