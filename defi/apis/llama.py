import pandas as pd
import requests


class LlamaAPI:
    def __init__(self):
        self.url = "https://api.llama.fi"

    def get_protocols(self):
        """
        Get list all DeFi protocols across all blockchains

        Returns:
            DataFrame: All DeFi dApps 
        """
        json_response = requests.get(f"{self.url}/protocols").json()
        df = pd.DataFrame(json_response)
        return df.set_index('name', inplace=False)

    def get_protocol(self, protocol):
        """
        Get metrics and historic TVL for one DeFi dApp

        Args:
            protocol (String): Name of protocol ie "Uniswap"

        Returns:
            tuple (Dictionary, DataFrame): Dictionary with protocol metadata & DataFrame with historical TVL
        """
        json_response = requests.get(f"{self.url}/protocol/{protocol}").json()
        try:
            df = pd.DataFrame(json_response['tvl'])
            df.date = pd.to_datetime(df.date, unit='s')
            df = df.set_index('date')
            return json_response, df
        except KeyError:
            print(f"{protocol} not found")  # Use loggers instead of prints
            return {}, pd.DataFrame()

    def get_chart(self):
        """
        Get historical TVL across all DeFi dApps, cummulative result

        Returns:
            DataFrame: DataFrame date-indexed with all days TVL 
        """

        json_response = requests.get(f"{self.url}/charts").json()
        df = pd.DataFrame(json_response)
        df.date = pd.to_datetime(df.date, unit='s')
        df = df.set_index('date')
        return df
