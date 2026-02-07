from ...domain.analyzers import StandardMarketAnalyzer
from ...domain.models import MarketInfo


class AnalyzerFactory:

    @staticmethod
    def get_standard_analyzer(market_info: MarketInfo) -> StandardMarketAnalyzer:
        return StandardMarketAnalyzer(market_info)
