from django.core.exceptions import ValidationError
##################################################

def validate_rate(rate):
    if rate > 10:
        raise ValidationError("The max rate is 10 of 10")
    if rate < 0 :
        raise ValidationError("The Minimum rate is 0 of 10")
    
def validate_price(price):
    if price < 0 :
        raise ValidationError("The price can not be negative")
    
def validate_quantity(quantity):
    if quantity == 0 :
        raise ValidationError("the quantity should be bigger than zero")