'''
Problem 1: Paying The Minimum
program calculates the credit card balance after
one year if a person only pays the minimum
monthly payment required by the credit card company each month
'''
balance = 3200
annualInterestRate = 0.2
monthlyPaymentRate = 0.04
percemtage = annualInterestRate/12
year = 12


balance_list = []
min_month_payment_list = []
updated_bal_list = []

for month in range(1,year+1):
   min_month_payment = monthlyPaymentRate * balance
   min_month_payment_list.append(round(min_month_payment, 2))
   
   monthly_unpaid_balance =  balance - min_month_payment
   
   updated_bal = percemtage * monthly_unpaid_balance + monthly_unpaid_balance
   balance_list.append(updated_bal)
   balance = updated_bal 
    if month != 12:
       print "Month: %s \nMinimum monthly payment: %s \nRemaining balance: %s" %(month, round(min_month_payment,2), round(updated_bal, 2) )
    else:
       total = sum(min_month_payment_list)
      print "Month: %s \nMinimum monthly payment: %s \nRemaining balance: %s \nTotal paid: %s \nRemaining balance: %s" %(month, round(min_month_payment,2),round(updated_bal, 2), round(total,2),round(updated_bal, 2) )
    





monthlyInterestRate = annualInterestRate/12
minPay = 0
'''
Problem 2: Paying Debt Off In A Year
This part  calculates the minimum fixed monthly
payment needed in order pay off a credit card
balance within 12 months.
'''
balanceCopy = balance
while balance > 0:
   balance = balanceCopy
   minPay += 10
   for i in range(12):
       monthlyUnpaid = balance - minPay
       balance = monthlyUnpaid + monthlyInterestRate*monthlyUnpaid
print "Lowest Payment: "+str(round(minPay,2))

'''
Problem 3: Using Bisection Search
To Make The Program Faster
''' 
lower_bound = balance/12
upper_bound = (balance * (1+monthlyInterestRate)**12)/12.0
balanceCopy = balance
mid = (upper_bound + lower_bound) /2
w= 0
while balance != 0 and w !=100 :  
    balance = balanceCopy
    minPay = mid
    for i in range(12):
        monthlyUnpaid = round(balance - minPay,3)
        balance = round(monthlyUnpaid + monthlyInterestRate*monthlyUnpaid,2)
    w +=1
    if balance >0 :
        lower_bound = mid
        mid = (upper_bound + lower_bound) /2
        mid =round(mid, 3) 
    if balance < 0 :
        upper_bound = mid
        mid = (upper_bound + lower_bound) /2
        mid =round(mid, 3) 
print "Lowest Payment: "+str(round(minPay,2))