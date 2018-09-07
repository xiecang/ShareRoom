from app.view_models.book import BookViewModel


class TradeInfo:
    def __init__(self, goods):
        self.total = 0
        self.trades = []
        self.__parse(goods)

    def __parse(self, goods):
        self.total = len(goods)
        self.trades = [self.__map_to_trade(single) for single in goods]

    def __map_to_trade(self, single):
        if single.create_datetime:
            time = single.create_datetime.strftime("%Y-%m-%d")
        else:
            time = '未知'
        return dict(
            user_name=single.user.nickname,
            time=time,
            id=single.id,
        )


class MyTrades:
    def __init__(self, trades_of_mine, trade_count_list):
        self.trades = []

        self.__trades_of_mine = trades_of_mine
        self.__trade_count_list = trade_count_list

        self.trades = self.__parse()

    def __parse(self):
        tmp_trade = []
        for trade in self.__trades_of_mine:
            my_trade = self.__matching(trade)
            tmp_trade.append(my_trade)
        return tmp_trade

    def __matching(self, trade):
        count = 0
        for wish_count in self.__trade_count_list:
            if trade.isbn == wish_count['isbn']:
                count = wish_count['count']
        # my_gift = MyGift(gift.id, BookViewModel(gift.book), count)
        # return my_gift
        r = {
            'wishes_count': count,
            'book': BookViewModel(trade.book),
            'id': trade.id,
        }
        return r
