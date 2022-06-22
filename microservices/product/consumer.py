from main import redis, Product
import time
key = 'order_completed'
group = 'inventory_group'

try:
    redis.xgroup_create(key,group)
except:
    print("Group already exist")

while True:
    try:
        results = redis.xreadgroup(group,key,{key:'>'},None)

        if results == []:
            continue
        print(results)
        for result in results:
            obj = result[1][0][1]
            try:
                product = Product.get(obj['product_id'])
                product.quantity_available = product.quantity_available - int(obj['quantity'])
                product.save()
            except:
                print("There is no Product: Order to be Refunded ")
                redis.xadd('refund_order', obj, '*')

    except Exception as e:
        print((str(e)))
    time.sleep(1)
