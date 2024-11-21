from django.test import TestCase

# Create your tests here.
from datetime import time

# Example: Create or update a record
sheet = MyModel.objects.create(
    checkin=time(9, 0, 0), 
    checkout=time(19, 30, 0)  # Overtime of 1.5 hours
)
sheet.update_status()
sheet.save()

# Check if `ot` is correct
print(sheet.ot)  # Should print 1 (1.5 hours truncated to integer)
