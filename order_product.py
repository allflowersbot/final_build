import typing

from dbcm import get_query, get_query_all, connect

class product:

    def __init__(self, prod_id):
        self.pr_id = prod_id

    def get_pr_id(self):
        return self.pr_id

    def get_caption(self):
        return get_query("select caption from products where id = %s;", (self.pr_id,))

    def get_shop_id(self):
        return get_query("select shop_id from products where id = %s;", (self.pr_id,))

    def get_cost(self):
        return get_query("select cost from products where id = %s;", (self.pr_id,))

    def get_file_id(self):
        return get_query("select file_id from products where id = %s;", (self.pr_id,))

    def get_categ(self):
        return get_query("select categories from products where id = %s;", (self.pr_id,))

    def get_time_of_build(self):
        return get_query("select timeofbuild from products where id = %s;", (self.pr_id,))

    def get_default_bucket(self):
        return get_query("select default_bucket from products where id = %s;", (self.pr_id,))

class order:

    total = 0
    def __init__(self, client_id, list_of_shops, list_of_prod_and_amount):
        self.order_id = order.total + 1
        order.total+=1
        self.list_of_shops = list_of_shops
        self.list_of_prod_and_amount = list_of_prod_and_amount
        list_of_managers = []
        for sh_id in list_of_shops:
            cnx = connect()
            curs = cnx.cursor()
            curs.execute("select manager_chat_id from managers where shop_id = {};".format(sh_id))
            people = curs.fetchall()
            for manager in people:
                list_of_managers.append(manager[0])

        self.list_of_managers = set(list_of_managers)
        self.delivery = False
        self.curr_manager = 494609919
        self.curr_shop = 1
        cost = 0
        for pair in list_of_prod_and_amount:
            cost+=int(pair[0].get_cost()) * int(pair[1])
        self.payment_order_id = 0
        self.curr_cost = cost
        self.first_cost = cost
        self.delivery_cost = 0
        self.client_id = client_id
        self.delivery_addr = get_query("select order_shipping_adress from orders where client_order_id = %s;", (self.client_id,))
        self.pay = False

    def get_total(self):
        return order.total

    def make_final_offer(self):
        offer = "товары в заказе:\n"
        array_of_images = []
        i=1
        for pair in self.list_of_prod_and_amount:
            prod = pair[0]
            offer+= "{}) описание: {}\nпервичная цена была: {}\nколичество: {}".format(i, prod.get_caption(), prod.get_cost(), pair[1])
            array_of_images.append(prod.get_file_id())
            i+=1
        offer += "\nтекущая цена заказа: {}".format(self.get_curr_cost())
        offer+="\nадрес доставки: {}".format(self.delivery_addr)
        offer+="\nцена доставки:{}".format(self.delivery_cost)
        offer+="\n#{}#".format(self.order_id)
        contacts = get_query_all("select first_name, last_name, client_phone from clients where client_chat_id = %s;", (self.client_id,))
        offer+="\nконтактное лицо: {} номер телефона:{}".format(contacts[0], contacts[2])
        return offer, array_of_images


    def make_offer(self):
        offer = "товары в заказе:\n"
        array_of_images = []
        i=1
        for pair in self.list_of_prod_and_amount:
            prod = pair[0]
            offer+= "{}) описание: {}\nпервичная цена была: {}\nколичество: {}".format(i, prod.get_caption(), prod.get_cost(), pair[1])
            array_of_images.append(prod.get_file_id())
            i+=1
        offer += "\nтекущая цена заказа: {}".format(self.get_curr_cost())
        offer+="\nадрес доставки: {}".format(self.delivery_addr)
        offer+="\n#{}#".format(self.order_id)
        return offer, array_of_images


    def make_client_offer(self):
        offer = "товары в заказе:\n"
        array_of_images = []
        i=1
        for pair in self.list_of_prod_and_amount:
            prod = pair[0]
            offer+= "{}) описание: {}\nцена: {}\nколичество: {}\nартикул:{}".format(i, prod.get_caption(), prod.get_cost(), pair[1], prod.get_pr_id())
            array_of_images.append(prod.get_file_id())
            i+=1
        offer+="\nадрес доставки: {}".format(self.delivery_addr)
        offer+="\nцена доставки: {} рублей".format(self.get_delivery_cost())
        return offer, array_of_images


    def get_payment_order_id(self):
        return self.payment_order_id

    def set_payment_order_id(self, new_id):
        self.payment_order_id = new_id

    def get_order_id(self):
        return self.order_id

    def get_list_of_shops(self):
        return self.list_of_shops

    def get_list_of_prod(self):
        return self.list_of_prod_and_amount

    def get_list_of_managers(self):
        return self.list_of_managers

    def get_delivery_status(self):
        return self.delivery

    def get_curr_manager(self):
        return self.curr_manager

    def get_curr_shop(self):
        return self.curr_shop

    def get_curr_cost(self):
        return self.curr_cost

    def get_first_cost(self):
        return self.first_cost

    def get_delivery_cost(self):
        return self.delivery_cost

    def get_client_id(self):
        return self.client_id

    def get_addr(self):
        return self.delivery_addr

    def change_curr_manager(self, manager_chat_id):
        self.curr_manager = manager_chat_id

    def change_curr_cost(self, new_cost):
        if self.curr_cost > new_cost:
            self.curr_cost = new_cost
            return True
        else:
            return False

    def change_curr_shop(self, sh_id):
        if sh_id in self.list_of_shops:
            self.curr_shop = sh_id
            return True
        else:
            return False


    def set_delivery_cost(self, deliv_cost):
        self.delivery_cost = deliv_cost


    def update_curr_shop(self):
        self.curr_shop = get_query("select shop_id from managers where manager_chat_id = %s;", (self.curr_manager,))