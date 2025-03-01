import warnings
warnings.filterwarnings("ignore")

import logging
import os
import platform
import enum
import msgpack
import asyncio
import time
from datetime import datetime

from findy.interface import Region, Provider, RunMode
from findy.utils.kafka import publish_message
from findy.utils.progress import ProgressBarProcess, progress_topic, progress_key
from findy.utils.cache import valid, get_cache, dump_cache
import findy.vendor.aiomultiprocess as amp

logger = logging.getLogger(__name__)


class task():
    @staticmethod
    async def get_stock_list_data(region: Region, provider: Provider, sleep, process, desc):
        # 股票列表
        from findy.database.schema.meta.stock_meta import Stock
        await Stock.record_data(region, provider, sleeping_time=sleep, share_para=(process, desc))

    @staticmethod
    async def get_fund_list_data(region: Region, provider: Provider, sleep, process, desc):
        # 基金列表
        from findy.database.schema.meta.fund_meta import Fund
        await Fund.record_data(region, provider, sleeping_time=sleep, share_para=(process, desc))

    @staticmethod
    async def get_stock_trade_day(region: Region, provider: Provider, sleep, process, desc):
        # 交易日
        from findy.database.schema.quotes.trade_day import StockTradeDay
        await StockTradeDay.record_data(region, provider, sleeping_time=sleep, share_para=(process, desc))

    @staticmethod
    async def get_stock_main_index(region: Region, provider: Provider, sleep, process, desc):
        from findy.database.plugins.exchange.main_index import init_main_index
        await init_main_index(region, provider)

    @staticmethod
    async def get_stock_summary_data(region: Region, provider: Provider, sleep, process, desc):
        # 市场整体估值
        from findy.database.schema.misc.overall import StockSummary
        await StockSummary.record_data(region, provider, sleeping_time=sleep, share_para=(process, desc))

    @staticmethod
    async def get_stock_detail_data(region: Region, provider: Provider, sleep, process, desc):
        # 个股详情
        from findy.database.schema.meta.stock_meta import StockDetail
        await StockDetail.record_data(region, provider, sleeping_time=sleep, share_para=(process, desc))

    @staticmethod
    async def get_finance_factor_data(region: Region, provider: Provider, sleep, process, desc):
        # 主要财务指标
        from findy.database.schema.fundamental.finance import FinanceFactor
        await FinanceFactor.record_data(region, provider, sleeping_time=sleep, share_para=(process, desc))

    @staticmethod
    async def get_balance_sheet_data(region: Region, provider: Provider, sleep, process, desc):
        # 资产负债表
        from findy.database.schema.fundamental.finance import BalanceSheet
        await BalanceSheet.record_data(region, provider, sleeping_time=sleep, share_para=(process, desc))

    @staticmethod
    async def get_income_statement_data(region: Region, provider: Provider, sleep, process, desc):
        # 收益表
        from findy.database.schema.fundamental.finance import IncomeStatement
        await IncomeStatement.record_data(region, provider, sleeping_time=sleep, share_para=(process, desc))

    @staticmethod
    async def get_cashflow_statement_data(region: Region, provider: Provider, sleep, process, desc):
        # 现金流量表
        from findy.database.schema.fundamental.finance import CashFlowStatement
        await CashFlowStatement.record_data(region, provider, sleeping_time=sleep, share_para=(process, desc))

    @staticmethod
    async def get_moneyflow_data(region: Region, provider: Provider, sleep, process, desc):
        # 股票资金流向表
        from findy.database.schema.misc.money_flow import StockMoneyFlow
        await StockMoneyFlow.record_data(region, provider, sleeping_time=sleep, share_para=(process, desc))

    @staticmethod
    async def get_dividend_financing_data(region: Region, provider: Provider, sleep, process, desc):
        # 除权概览表
        from findy.database.schema.fundamental.dividend_financing import DividendFinancing
        await DividendFinancing.record_data(region, provider, sleeping_time=sleep, share_para=(process, desc))

    @staticmethod
    async def get_dividend_detail_data(region: Region, provider: Provider, sleep, process, desc):
        # 除权具细表
        from findy.database.schema.fundamental.dividend_financing import DividendDetail
        await DividendDetail.record_data(region, provider, sleeping_time=sleep, share_para=(process, desc))

    @staticmethod
    async def get_rights_issue_detail_data(region: Region, provider: Provider, sleep, process, desc):
        # 配股表
        from findy.database.schema.fundamental.dividend_financing import RightsIssueDetail
        await RightsIssueDetail.record_data(region, provider, sleeping_time=sleep, share_para=(process, desc))

    @staticmethod
    async def get_spo_detail_data(region: Region, provider: Provider, sleep, process, desc):
        # 现金增资
        from findy.database.schema.fundamental.dividend_financing import SpoDetail
        await SpoDetail.record_data(region, provider, sleeping_time=sleep, share_para=(process, desc))

    @staticmethod
    async def get_margin_trading_summary_data(region: Region, provider: Provider, sleep, process, desc):
        # 融资融券概况
        from findy.database.schema.misc.overall import MarginTradingSummary
        await MarginTradingSummary.record_data(region, provider, sleeping_time=sleep, share_para=(process, desc))

    @staticmethod
    async def get_cross_market_summary_data(region: Region, provider: Provider, sleep, process, desc):
        # 北向/南向成交概况
        from findy.database.schema.misc.overall import CrossMarketSummary
        await CrossMarketSummary.record_data(region, provider, sleeping_time=sleep, share_para=(process, desc))

    @staticmethod
    async def get_holder_trading_data(region: Region, provider: Provider, sleep, process, desc):
        # 股东交易
        from findy.database.schema.fundamental.trading import HolderTrading
        await HolderTrading.record_data(region, provider, sleeping_time=sleep, share_para=(process, desc))

    @staticmethod
    async def get_top_ten_holder_data(region: Region, provider: Provider, sleep, process, desc):
        # 前十股东表
        from findy.database.schema.misc.holder import TopTenHolder
        await TopTenHolder.record_data(region, provider, sleeping_time=sleep, share_para=(process, desc))

    @staticmethod
    async def get_top_ten_tradable_holder_data(region: Region, provider: Provider, sleep, process, desc):
        # 前十可交易股东表
        from findy.database.schema.misc.holder import TopTenTradableHolder
        await TopTenTradableHolder.record_data(region, provider, sleeping_time=sleep, share_para=(process, desc))

    @staticmethod
    async def get_stock_valuation_data(region: Region, provider: Provider, sleep, process, desc):
        # 个股估值数据
        from findy.database.schema.fundamental.valuation import StockValuation
        await StockValuation.record_data(region, provider, sleeping_time=sleep, share_para=(process, desc))

    @staticmethod
    async def get_etf_valuation_data(region: Region, provider: Provider, sleep, process, desc):
        # ETF估值数据
        from findy.database.schema.fundamental.valuation import EtfValuation
        await EtfValuation.record_data(region, provider, sleeping_time=sleep, share_para=(process, desc))

    @staticmethod
    async def get_stock_1d_k_data(region: Region, provider: Provider, sleep, process, desc):
        # 日线
        from findy.database.schema.quotes.stock.stock_1d_kdata import Stock1dKdata
        await Stock1dKdata.record_data(region, provider, sleeping_time=sleep, share_para=(process, desc))

    @staticmethod
    async def get_stock_1d_hfq_k_data(region: Region, provider: Provider, sleep, process, desc):
        # 日线复权
        from findy.database.schema.quotes.stock.stock_1d_kdata import Stock1dHfqKdata
        await Stock1dHfqKdata.record_data(region, provider, sleeping_time=sleep, share_para=(process, desc))

    @staticmethod
    async def get_stock_1w_k_data(region: Region, provider: Provider, sleep, process, desc):
        # 周线
        from findy.database.schema.quotes.stock.stock_1wk_kdata import Stock1wkKdata
        await Stock1wkKdata.record_data(region, provider, sleeping_time=sleep, share_para=(process, desc))

    @staticmethod
    async def get_stock_1w_hfq_k_data(region: Region, provider: Provider, sleep, process, desc):
        # 周线复权
        from findy.database.schema.quotes.stock.stock_1wk_kdata import Stock1wkHfqKdata
        await Stock1wkHfqKdata.record_data(region, provider, sleeping_time=sleep, share_para=(process, desc))

    @staticmethod
    async def get_stock_1mon_k_data(region: Region, provider: Provider, sleep, process, desc):
        # 月线
        from findy.database.schema.quotes.stock.stock_1mon_kdata import Stock1monKdata
        await Stock1monKdata.record_data(region, provider, sleeping_time=sleep, share_para=(process, desc))

    @staticmethod
    async def get_stock_1mon_hfq_k_data(region: Region, provider: Provider, sleep, process, desc):
        # 月线复权
        from findy.database.schema.quotes.stock.stock_1mon_kdata import Stock1monHfqKdata
        await Stock1monHfqKdata.record_data(region, provider, sleeping_time=sleep, share_para=(process, desc))

    @staticmethod
    async def get_stock_1m_k_data(region: Region, provider: Provider, sleep, process, desc):
        # 1分钟线
        from findy.database.schema.quotes.stock.stock_1m_kdata import Stock1mKdata
        await Stock1mKdata.record_data(region, provider, sleeping_time=sleep, share_para=(process, desc))

    @staticmethod
    async def get_stock_1m_hfq_k_data(region: Region, provider: Provider, sleep, process, desc):
        # 1分钟线复权
        from findy.database.schema.quotes.stock.stock_1m_kdata import Stock1mHfqKdata
        await Stock1mHfqKdata.record_data(region, provider, sleeping_time=sleep, share_para=(process, desc))

    @staticmethod
    async def get_stock_5m_k_data(region: Region, provider: Provider, sleep, process, desc):
        # 5分钟线
        from findy.database.schema.quotes.stock.stock_5m_kdata import Stock5mKdata
        await Stock5mKdata.record_data(region, provider, sleeping_time=sleep, share_para=(process, desc))

    @staticmethod
    async def get_stock_5m_hfq_k_data(region: Region, provider: Provider, sleep, process, desc):
        # 5分钟线复权
        from findy.database.schema.quotes.stock.stock_5m_kdata import Stock5mHfqKdata
        await Stock5mHfqKdata.record_data(region, provider, sleeping_time=sleep, share_para=(process, desc))

    @staticmethod
    async def get_stock_15m_k_data(region: Region, provider: Provider, sleep, process, desc):
        # 15分钟线
        from findy.database.schema.quotes.stock.stock_15m_kdata import Stock15mKdata
        await Stock15mKdata.record_data(region, provider, sleeping_time=sleep, share_para=(process, desc))

    @staticmethod
    async def get_stock_15m_hfq_k_data(region: Region, provider: Provider, sleep, process, desc):
        # 15分钟线复权
        from findy.database.schema.quotes.stock.stock_15m_kdata import Stock15mHfqKdata
        await Stock15mHfqKdata.record_data(region, provider, sleeping_time=sleep, share_para=(process, desc))

    @staticmethod
    async def get_stock_30m_k_data(region: Region, provider: Provider, sleep, process, desc):
        # 30分钟线
        from findy.database.schema.quotes.stock.stock_30m_kdata import Stock30mKdata
        await Stock30mKdata.record_data(region, provider, sleeping_time=sleep, share_para=(process, desc))

    @staticmethod
    async def get_stock_30m_hfq_k_data(region: Region, provider: Provider, sleep, process, desc):
        # 30分钟线复权
        from findy.database.schema.quotes.stock.stock_30m_kdata import Stock30mHfqKdata
        await Stock30mHfqKdata.record_data(region, provider, sleeping_time=sleep, share_para=(process, desc))

    @staticmethod
    async def get_stock_1h_k_data(region: Region, provider: Provider, sleep, process, desc):
        # 1小时线
        from findy.database.schema.quotes.stock.stock_1h_kdata import Stock1hKdata
        await Stock1hKdata.record_data(region, provider, sleeping_time=sleep, share_para=(process, desc))

    @staticmethod
    async def get_stock_1h_hfq_k_data(region: Region, provider: Provider, sleep, process, desc):
        # 1小时线复权
        from findy.database.schema.quotes.stock.stock_1h_kdata import Stock1hHfqKdata
        await Stock1hHfqKdata.record_data(region, provider, sleeping_time=sleep, share_para=(process, desc))

    @staticmethod
    async def get_etf_1d_k_data(region: Region, provider: Provider, sleep, process, desc):
        from findy.database.schema.quotes.etf.etf_1d_kdata import Etf1dKdata
        await Etf1dKdata.record_data(region, provider, sleeping_time=sleep, share_para=(process, desc))

    @staticmethod
    async def get_index_1d_k_data(region: Region, provider: Provider, sleep, process, desc):
        from findy.database.schema.quotes.index.index_1d_kdata import Index1dKdata
        await Index1dKdata.record_data(region, provider, sleeping_time=sleep, share_para=(process, desc))


task_set_chn = [
    ["task_chn_01", task.get_stock_list_data,              Provider.Exchange,  0, 10, "Stock List",               24 * 6, RunMode.Serial],
    ["task_chn_02", task.get_stock_trade_day,              Provider.BaoStock,  0, 10, "Trade Day",                24,     RunMode.Serial],
    # ["task_chn_03", task.get_fund_list_data,                Provider.Exchange,  0, 10, "Fund List",                 24 * 6, RunMode.Serial],
    ["task_chn_04", task.get_stock_main_index,             Provider.BaoStock,  0, 10, "Main Index",               24,     RunMode.Serial],
    ["task_chn_05", task.get_stock_detail_data,            Provider.TuShare,   0,  4, "Stock Detail",             24 * 6, RunMode.Parallel],

    # ["task_chn_06", task.get_dividend_financing_data,      Provider.EastMoney, 0, 10, "Divdend Financing",        24 * 6,  RunMode.Parallel],
    # ["task_chn_07", task.get_top_ten_holder_data,          Provider.EastMoney, 0, 10, "Top Ten Holder",           24 * 6,  RunMode.Parallel],
    # ["task_chn_08", task.get_top_ten_tradable_holder_data, Provider.EastMoney, 0, 10, "Top Ten Tradable Holder",  24 * 6,  RunMode.Parallel],
    # ["task_chn_09", task.get_dividend_detail_data,         Provider.EastMoney, 0, 10, "Divdend Detail",           24 * 6,  RunMode.Parallel],
    # ["task_chn_10", task.get_spo_detail_data,              Provider.EastMoney, 0, 10, "SPO Detail",               24 * 6,  RunMode.Parallel],
    # ["task_chn_11", task.get_rights_issue_detail_data,     Provider.EastMoney, 0, 10, "Rights Issue Detail",      24,      RunMode.Parallel],
    # ["task_chn_12", task.get_holder_trading_data,          Provider.EastMoney, 0, 10, "Holder Trading",           24 * 6,  RunMode.Parallel],

    # # below functions call join-quant sdk task which limit at most 3 concurrent request
    # ["task_chn_13", task.get_finance_factor_data,          Provider.EastMoney, 0, 10, "Finance Factor",           24 * 6,  RunMode.Parallel],
    # ["task_chn_14", task.get_balance_sheet_data,           Provider.EastMoney, 0, 10, "Balance Sheet",            24 * 6,  RunMode.Parallel],
    # ["task_chn_15", task.get_income_statement_data,        Provider.EastMoney, 0, 10, "Income Statement",         24 * 6,  RunMode.Parallel],
    # ["task_chn_16", task.get_cashflow_statement_data,      Provider.EastMoney, 0, 10, "CashFlow Statement",       24,      RunMode.Parallel],
    # ["task_chn_17", task.get_stock_valuation_data,         Provider.JoinQuant, 0, 10, "Stock Valuation",          24,      RunMode.Parallel],
    # ["task_chn_18", task.get_cross_market_summary_data,    Provider.JoinQuant, 0, 10, "Cross Market Summary",     24,      RunMode.Parallel],
    # ["task_chn_19", task.get_stock_summary_data,           Provider.Exchange,  0, 10, "Stock Summary",            24,      RunMode.Parallel],
    # ["task_chn_20", task.get_margin_trading_summary_data,  Provider.JoinQuant, 0, 10, "Margin Trading Summary",   24,      RunMode.Parallel],
    # ["task_chn_21", task.get_etf_valuation_data,           Provider.JoinQuant, 0, 10, "ETF Valuation",            24,      RunMode.Parallel],
    # ["task_chn_22", task.get_moneyflow_data,               Provider.Sina,      1, 10, "MoneyFlow Statement",      24,      RunMode.Parallel],

    # ["task_chn_23", task.get_etf_1d_k_data,                Provider.Sina,      0, 10, "ETF Daily K-Data",         24,      RunMode.Parallel],
    ["task_chn_24", task.get_stock_1d_k_data,              Provider.BaoStock,  0, 100, "Stock Daily   K-Data",     24,      RunMode.Parallel],
    ["task_chn_25", task.get_stock_1w_k_data,              Provider.BaoStock,  0, 100, "Stock Weekly  K-Data",     24,      RunMode.Parallel],
    ["task_chn_26", task.get_stock_1mon_k_data,            Provider.BaoStock,  0, 100, "Stock Monthly K-Data",     24,      RunMode.Parallel],
    ["task_chn_27", task.get_stock_1h_k_data,              Provider.BaoStock,  0,  50, "Stock 1 hours K-Data",     24,      RunMode.Parallel],
    ["task_chn_28", task.get_stock_30m_k_data,             Provider.BaoStock,  0,  50, "Stock 30 mins K-Data",     24,      RunMode.Parallel],
    ["task_chn_29", task.get_stock_15m_k_data,             Provider.BaoStock,  0,  40, "Stock 15 mins K-Data",     24,      RunMode.Parallel],
    ["task_chn_30", task.get_stock_5m_k_data,              Provider.BaoStock,  0,  20, "Stock 5 mins  K-Data",     24,      RunMode.Parallel],
    # ["task_chn_31", task.get_stock_1m_k_data,              Provider.BaoStock,  0, 10, "Stock 1 mins  K-Data",     24,      RunMode.Parallel],

    # ["task_chn_32", task.get_stock_1d_hfq_k_data,          Provider.BaoStock,  0, 10, "Stock Daily   HFQ K-Data", 24,      RunMode.Parallel],
    # ["task_chn_33", task.get_stock_1w_hfq_k_data,          Provider.BaoStock,  0, 10, "Stock Weekly  HFQ K-Data", 24,      RunMode.Parallel],
    # ["task_chn_34", task.get_stock_1mon_hfq_k_data,        Provider.BaoStock,  0, 10, "Stock Monthly HFQ K-Data", 24,      RunMode.Parallel],
    # ["task_chn_35", task.get_stock_1h_hfq_k_data,          Provider.BaoStock,  0, 10, "Stock 1 hours HFQ K-Data", 24,      RunMode.Parallel],
    # ["task_chn_36", task.get_stock_30m_hfq_k_data,         Provider.BaoStock,  0, 10, "Stock 30 mins HFQ K-Data", 24,      RunMode.Parallel],
    # ["task_chn_37", task.get_stock_15m_hfq_k_data,         Provider.BaoStock,  0, 10, "Stock 15 mins HFQ K-Data", 24,      RunMode.Parallel],
    # ["task_chn_38", task.get_stock_5m_hfq_k_data,          Provider.BaoStock,  0, 10, "Stock 5 mins  HFQ K-Data", 24,      RunMode.Parallel],
    # ["task_chn_39", task.get_stock_1m_hfq_k_data,          Provider.BaoStock,  0, 10, "Stock 1 mins HFQ K-Data",  24,      RunMode.Parallel],
]


task_set_us = [
    ["task_us_01", task.get_stock_list_data,              Provider.Exchange,  0, 3, "Stock List",               24,      RunMode.Serial],
    ["task_us_02", task.get_stock_trade_day,              Provider.Yahoo,     0, 3, "Trade Day",                24,      RunMode.Serial],
    ["task_us_03", task.get_stock_main_index,             Provider.Exchange,  0, 3, "Main Index",               24,      RunMode.Serial],
    ["task_us_04", task.get_stock_detail_data,            Provider.Yahoo,     0, 3, "Stock Detail",             24 * 6,  RunMode.Parallel],

    ["task_us_05", task.get_index_1d_k_data,              Provider.Yahoo,     0, 3, "Index Daily   K-Data",     24,      RunMode.Parallel],
    ["task_us_06", task.get_stock_1d_k_data,              Provider.Yahoo,     0, 3, "Stock Daily   K-Data",     24,      RunMode.Parallel],
    ["task_us_07", task.get_stock_1w_k_data,              Provider.Yahoo,     0, 3, "Stock Weekly  K-Data",     24,      RunMode.Parallel],
    ["task_us_08", task.get_stock_1mon_k_data,            Provider.Yahoo,     0, 3, "Stock Monthly K-Data",     24,      RunMode.Parallel],
    ["task_us_09", task.get_stock_1h_k_data,              Provider.Yahoo,     0, 3, "Stock 1 hours K-Data",     24,      RunMode.Parallel],
    ["task_us_10", task.get_stock_30m_k_data,             Provider.Yahoo,     0, 3, "Stock 30 mins K-Data",     24,      RunMode.Parallel],
    ["task_us_11", task.get_stock_15m_k_data,             Provider.Yahoo,     0, 3, "Stock 15 mins K-Data",     24,      RunMode.Parallel],
    ["task_us_12", task.get_stock_5m_k_data,              Provider.Yahoo,     0, 3, "Stock 5 mins  K-Data",     24,      RunMode.Parallel],
    ["task_us_13", task.get_stock_1m_k_data,              Provider.Yahoo,     0, 3, "Stock 1 mins  K-Data",     24,      RunMode.Parallel],
]


class Para(enum.Enum):
    TaskID = 0
    FunName = 1
    Provider = 2
    Sleep = 3
    Processor = 4
    Desc = 5
    Cache = 6
    Mode = 7


async def loop_task_set(args):
    now = time.time()
    region, item, _ = args

    logger.info(f"Start Func: {item[Para.FunName.value].__name__}")
    await item[Para.FunName.value](region, item[Para.Provider.value], item[Para.Sleep.value], item[Para.Processor.value], item[Para.Desc.value])
    logger.info(f"End Func: {item[Para.FunName.value].__name__}, cost: {time.time() - now}\n")
    return item


async def fetch_process(region: Region, kafka_producer):
    print("")
    print("*" * 80)
    print(f"*    Start Fetching {region.value.upper()} Stock information...      {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("*" * 80)

    if region == Region.CHN:
        task_set = task_set_chn
    elif region == Region.US:
        task_set = task_set_us
    else:
        return

    print("")
    print("parallel fetching processing...")
    print("")

    schedule_log_file = f'update_schedule_log_{region.value}'
    schedule_cache = get_cache(schedule_log_file)

    if schedule_cache is None:
        schedule_cache = {}

    tasks_list = [(region, item, index) for index, item in enumerate(task_set) if not valid(region, item[Para.FunName.value].__name__, item[Para.Cache.value], schedule_cache)]

    pbar_update = {"task": "main", "total": len(tasks_list), "desc": "Total Jobs", "position": 0, "leave": True, "update": 0}
    publish_message(kafka_producer, progress_topic, progress_key, msgpack.dumps(pbar_update))

    for task in tasks_list[:]:
        task[1][Para.Desc.value] = (task[2] + 2, task[1][Para.Desc.value])

        if task[1][Para.Mode.value] == RunMode.Serial:
            result = await loop_task_set(task)

            publish_message(kafka_producer, progress_topic, progress_key,
                            msgpack.dumps({"command": "@task-finish", "task": result[Para.Desc.value][0]}))

            pbar_update['update'] = 1
            publish_message(kafka_producer, progress_topic, progress_key, msgpack.dumps(pbar_update))

            schedule_cache.update({f"{task[0].value}_{result[Para.FunName.value].__name__}": datetime.now()})
            dump_cache(schedule_log_file, schedule_cache)
            tasks_list.remove(task)

    Multi = True
    if Multi:
        tasks = len(tasks_list)
        cpus = max(1, min(tasks, os.cpu_count()))
        childconcurrency = max(1, round(tasks / cpus))

        current_os = platform.system().lower()
        if current_os != "windows":
            import uvloop
            loop_initializer = uvloop.new_event_loop
        else:
            loop_initializer = None

        async with amp.Pool(cpus, childconcurrency=childconcurrency, loop_initializer=loop_initializer) as pool:
            async for result in pool.map(loop_task_set, tasks_list):
                publish_message(kafka_producer, progress_topic, progress_key,
                                msgpack.dumps({"command": "@task-finish", "task": result[Para.Desc.value][0]}))

                pbar_update['update'] = 1
                publish_message(kafka_producer, progress_topic, progress_key, msgpack.dumps(pbar_update))

                schedule_cache.update({f"{region.value}_{result[Para.FunName.value].__name__}": datetime.now()})
                dump_cache(schedule_log_file, schedule_cache)
    else:
        for task in tasks_list:
            result = await loop_task_set(task)

            publish_message(kafka_producer, progress_topic, progress_key,
                            msgpack.dumps({"command": "@task-finish", "task": result[Para.Desc.value][0]}))

            pbar_update['update'] = 1
            publish_message(kafka_producer, progress_topic, progress_key, msgpack.dumps(pbar_update))

            schedule_cache.update({f"{region.value}_{result[Para.FunName.value].__name__}": datetime.now()})
            dump_cache(schedule_log_file, schedule_cache)


def fetching(region: Region):
    pbar = ProgressBarProcess()
    pbar.start()

    kafka_producer = pbar.getProducer()
    print("waiting for kafka connection.....")
    time.sleep(5)

    asyncio.run(fetch_process(region, kafka_producer))

    pbar_update = {"command": "@end"}
    publish_message(kafka_producer, progress_topic, progress_key, msgpack.dumps(pbar_update))

    pbar.join()


if __name__ == '__main__':
    fetching(Region.CHN)
