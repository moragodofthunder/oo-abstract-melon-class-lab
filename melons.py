import random
import datetime


"""Classes for melon orders."""

class AbstractMelonOrder:
    """An abstract base class that other Melon Orders inherit from."""

    def __init__(self, species, qty, country_code="US"):
        """initialize melon order attributes."""

        if qty > 100:
            raise TooManyMelonsError

        self.species = species
        self.qty = qty
        self.shipped = False
        self.country_code = country_code


    def get_base_price(self):
        """"Determine base price for melon order."""

        self.base_price = random.randint(5, 9)
        
        #Rush Hour pricing adds extra $4 charge to each order
        #placed btw 8-11am M-F

        # current_date = datetime.date.now()
        # day_of_week = current_date.weekday()
        # hour = current_date.hour()

        # if day_of_week > 0 and day_of_week < 6:
        #     if hour > 7.59 and hour < 11.00:
        #         self.base_price = self.base_price + 4

        return self.base_price


    def get_total(self):
        """Calculate price, including tax."""

        base_price = self.get_base_price()
        #Christmas melons will cost 1.5 times base price
        if self.species == "Christmas melon":
            base_price = base_price * 1.5
        
        total = (1 + self.tax) * self.qty * base_price
        #flat fee of $3 will be added to all int. orders < 10 melons
        if self.order_type == "international" and self.qty < 10:
            total = total + 3


        return total

    def mark_shipped(self):
        """Record the fact than an order has been shipped."""

        self.shipped = True

class DomesticMelonOrder(AbstractMelonOrder):
    """A melon order within the USA."""

    order_type = "domestic"
    tax = 0.08

    def __init__(self, species, qty):
        """Initialize melon order attributes."""
        super().__init__(species, qty)

class InternationalMelonOrder(AbstractMelonOrder):
    """An international (non-US) melon order."""

    order_type = "international"
    tax = 0.17

    def __init__(self, species, qty, country_code):
        super().__init__(species, qty)
        self.country_code = country_code
        
    def get_country_code(self):
        """Return the country code."""

        return self.country_code

class GovernmentMelonOrder(AbstractMelonOrder):
    """Melon order for US government"""

    order_type = "government"
    tax = 0.00

    def __init__(self, species, qty):
        super().__init__(species, qty)

        self.passed_inspection = False

    def mark_inspection(self, passed):
        """Record if an order has passed inspection."""

        self.passed_inspection = passed

class TooManyMelonsError(ValueError):
    """Raise when more than 100 melons are ordered at once."""

    def __init__(self):
        super().__init__("No more than 100 melons!")