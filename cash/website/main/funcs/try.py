

totalSales = [ {"name":"product 2" , "amount" : "30" , "price" : "15" , "type" : "manfaz"} , {"name":"product 1" , "amount" : "20" , "price" : "15" , "type" : "manfaz"} , {"name" : "product 3" , "amount" :"30" , "type":"manfaz"}]
additivies = [{  "name" : "product 2" , "amount" : "20"}  , {  "name" : "product 1" , "amount" : "50"} , {"name" :"product 3" , "amount" : "30"}]
foram = []
others = []

remainningAdditives = []
remainningEssentials = []
saledAdditivies = []
saledEssentials = []


for x in totalSales : 
    if x['type'] == "foram" : 
        foram.append(x)
    else : 
        others.append(x)

for  x in others : 
    for i in additivies : 
        productName = i['name']
        addAmounts = int(i['amount'])
        if x['name'] == productName  :
            if int(x['amount']) > addAmounts :

                # has additives and essentials 
                # all additives has been saled 

                addSaled = int(i['amount']) 

                saledAdditivies.append({"name" : x['name'] , "amount"  : addSaled})
                essSaled = int(x['amount'])  - addSaled
                saledEssentials.append({"name":x['name'] , "amount" : essSaled})
            else : 
                addSaled = int(x['amount'])
                addRemmaining = int(i['amount']) - addSaled
                saledAdditivies.append({"name" : x['name'] , "amount" : addSaled})
                remainningAdditives.append({"name" :  x['name'] , "amount" : addRemmaining})

sep = "==="*30

print(sep)
print(  "total Sales : ", totalSales)
print(sep)
print("remainning Essentials : " , remainningEssentials )
print(sep )
print("saled Additives : " , saledAdditivies )
print(sep)
print("saled Essentials : " , saledEssentials)
print(sep)
print("Remaiining Additives   : " , saledEssentials)
# insert all additives 
