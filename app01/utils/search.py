from urllib.parse import urlencode


class Search:
    def __init__(self, key, order, order_list, query_params):
        self.order_list = order_list
        self.query_params = {}
        self.order = order
        self.key = key
        for i in query_params:
            self.query_params[i] = query_params.getlist(i)

    def order_html(self):
        order_list = []
        for li in self.order_list:
            self.query_params[self.key] = li[0]
            # print(self.order,li[0],sep="\t\t\t")
            if self.order == li[0]:
                li = f'<li class="active"><a href="?{self.query_encode}">{li[1]}</a></li>'
            else:
                li = f'<li><a href="?{self.query_encode}">{li[1]}</a></li>'
            order_list.append(li)
        if not self.order:
            # 没有传递order
            str_li = order_list[0]
            new_str = str_li[0:3] + ' class="active"' + str_li[3:]
            order_list[0] = new_str
        return ''.join(order_list)

    @property
    def query_encode(self):
        return urlencode(self.query_params, doseq=True)
