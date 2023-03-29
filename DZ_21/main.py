from classes import Shop, Store, Request


def shop_store():
    print("В магазине хранится:")
    for key, value in shop.items.items():
        print(key, value)

    print("На складе хранится:")
    for key, value in store.items.items():
        print(key, value)


if __name__ == '__main__':
    shop = Shop()
    # shop.add("печеньки", 5)
    # shop.add ("собачки", 5 )
    # shop.add ("помидоры", 20 )
    shop.add("сок", 5)
    shop.add("лимонад", 5)
    shop.add("елки", 5)
    store = Store()
    store.add("печеньки", 5)
    store.add("булочки", 10)
    store.add("собачки", 5)
    shop_store()

    print("Шаблон заполнения - Доставить (количество) (наименование товара) из склад в магазин")
    user_str = input()
    user_str_list = user_str.split(" ")
    try:
        user_str_list[1] = int(user_str_list[1])
    except:
        print("Неверно заполнен шаблон!")
    else:
        r = Request(user_str)
        print(r)
        if r.product in store.get_items():
            if r.amount <= store.get_items()[r.product]:
                print("Нужное количество есть на складе")
                print("Курьер везет со склад в магазин")
                if sum(shop.get_items().values()) + int(r.amount) < shop.capacity:
                    print(f"Курьер доставил {r.amount} {r.product} в магазин")
                    store.remove(r.product, r.amount)
                    shop.add(r.product, r.amount)
                else:
                    print("В магазин недостаточно места, попобуйте что-то другое")
            else:
                print("Не хватает на складе, попробуйте заказать меньше")
        else:
            print("Такого товара нет на складе")
        shop_store()
