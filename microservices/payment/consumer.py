from main import redis, Order
import time

key = 'refund_order'
group = 'payment_group'

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
                order = Order.get(obj['product_id'])
                order.status = "refunded"
                order.save()
            except Exception as e:
                print("WTF ERROR, order not found")
                print(e)

    except Exception as e:
        print((str(e)))
    time.sleep(1)
