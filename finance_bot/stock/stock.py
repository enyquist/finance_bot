# standard libraries
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Union

# third party libraries
import pandas as pd
from yahoo_fin import stock_info as si


@dataclass
class Stock:
    """
    This class is used to represent a stock.
    """

    ticker: str

    def __post_init__(self):
        """
        This method is called after the object is initialized.
        """

        self.ticker = self.ticker.upper()
        self.today = datetime.today()
        self.history = si.get_data(self.ticker)
        self.dividends = si.get_dividends(self.ticker)
        # self.report = self._stock_report()

    def _current_price(self) -> float:
        """
        This method returns the current price of the stock.

        Returns:
            float: The current price of the stock.
        """

        return si.get_live_price(self.ticker)

    def _annual_performance(self) -> float:
        """
        This method returns the annual performance of the stock.

        Returns:
            float: The annual performance of the stock.
        """

        annual_date = (self.today - timedelta(days=365)).strftime("%Y-%m-%d")
        annual_price = self.history.loc[annual_date]["open"]
        return (self._current_price() - annual_price) / annual_price

    def _annual_price(self, years: Union[str, int] = 1) -> float:
        """
        This method returns the annual price of the stock.

        Args:
            years (int, optional): Years previous. Defaults to 1.

        Returns:
            float: Price of the stock years previous.
        """

        if years == "max":
            annual_date = self.history.index[0]
        else:
            annual_date = (self.today - timedelta(days=365 * years)).strftime("%Y-%m-%d")

        return self.history.loc[annual_date]["open"]

    def _annual_dividends(self, years: Union[str, int] = 1) -> float:
        """
        This method returns the annual dividends of the stock.

        Args:
            years (int, optional): Years previous. Defaults to 1.

        Returns:
            float: Dividends of the stock years previous.
        """

        if years == "max":
            annual_date = self.dividends.index[0]
        else:
            annual_date = (self.today - timedelta(days=365 * years)).strftime("%Y-%m-%d")

        return self.dividends.loc[annual_date:]["dividend"].sum()

    def _cagr(self, years: Union[str, int] = 3) -> float:
        """
        This method returns the compound annual growth rate of the stock.

        Args:
            years (Union[str, int], optional): Years previous. Defaults to 3.

        Returns:
            float: Compound annual growth rate of the stock.
        """

        if years == "max":
            years = self.history.shape[0] / 365
        else:
            years = int(years)

        return ((self._current_price() + self._annual_dividends(years)) / self._annual_price(years)) ** (1 / years) - 1

    def _stock_report(self) -> pd.DataFrame:
        """
        This method returns a DataFrame containing the stock report.

        Returns:
            pd.DataFrame: Stock report.
        """

        report = pd.DataFrame(
            {
                "Ticker": [self.ticker],
                "Current Price": [self._current_price()],
                "Annual Performance": [self._annual_performance()],
                "3 Year CAGR": [self._cagr(3)],
                "5 Year CAGR": [self._cagr(5)],
                "10 Year CAGR": [self._cagr(10)],
                "Max CAGR": [self._cagr("max")],
            }
        )

        return report
