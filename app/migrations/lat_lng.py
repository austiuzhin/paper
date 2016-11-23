from d_base import Item


total = Item.query.filter(Item.id).count()
total_n = Item.query.filter(Item.lat == None).count()