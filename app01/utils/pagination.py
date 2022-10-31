import math


class Pagination:
    def __init__(self, current_page, all_count, base_url, query_params, per_page=20, page_page_count=11,position='pos'):
        """
        :param current_page: 当前页码
        :param all_count: 数据库中总条数
        :param base_url: 原始URL
        :param query_params: 保留原搜索条件
        :param per_page: 一页展示多少条
        :param page_page_count: 最多展示多少个页码
        """

        self.all_count = all_count

        self.per_page = per_page
        self.current_count = math.ceil(all_count / per_page)
        self.position=position

        try:
            self.current_page = int(current_page)
            if not 0 < self.current_page <= self.current_count:
                self.current_page = 1
        except Exception:
            self.current_page = 1
        self.base_url = base_url
        self.query_params = query_params
        self.page_page_count = page_page_count
        self.half_page_count = int(self.page_page_count / 2)
        if self.current_count < self.page_page_count:
            # 如果可分页的页码小于最大显示页码，就让最大显示页码变成可分页页码
            self.page_page_count = self.current_count

    def page_html(self):
        # 计算页码的起始和结束
        # 分类讨论
        # 1. 正常情况
        start = self.current_page - self.half_page_count
        end = self.current_page + self.half_page_count
        if self.current_page <= self.half_page_count:
            # 在最左侧
            start = 1
            # 右边就是最大值
            end = self.page_page_count
        if self.current_page + self.half_page_count >= self.current_count:
            # 在最右侧
            start = self.current_count - self.page_page_count+1
            end = self.current_count
        # 生成分页
        page_list = []

        # 上一页
        if self.current_page != 1:
            self.query_params['page'] = self.current_page - 1
            page_list.append(f'<li><a href="{self.base_url}?{self.query_encode}#{self.position}">上一页</a></li>')

        for i in range(start, end + 1):
            self.query_params['page'] = i
            if self.current_page == i:
                li = f'<li class="active"><a href="{self.base_url}?{self.query_encode}#{self.position}">{i}</a></li>'
            else:
                li = f'<li><a href="{self.base_url}?{self.query_encode}#{self.position}">{i}</a></li>'
            page_list.append(li)
        # 下一页
        if self.current_page != self.current_count:
            self.query_params['page'] = self.current_page + 1
            page_list.append(f'<li><a href="{self.base_url}?{self.query_encode}#{self.position}">下一页</a></li>')
        if len(page_list)==1:
            # 不显示分页器
            page_list=[]

        return ''.join(page_list)

    @property
    def start(self):
        return (self.current_page - 1) * self.per_page

    @property
    def end(self):
        return self.current_page * self.per_page

    @property
    def query_encode(self):
        return self.query_params.urlencode()
