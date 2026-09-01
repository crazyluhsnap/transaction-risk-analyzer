from .analyzer import analyze_transaction
from .account_analyzer import analyze_account
from .network_risk import get_network_risk_for_transaction
from .risk_aggregator import calculate_final_risk

class RiskEngine:
    def __init__(self,df,cycles):
        self.df=df
        self.cycles=cycles

    def analyze_transaction(self,transaction):
        transaction_result=analyze_transaction(
            transaction
        )

        account_result=analyze_account(
            self.df,
            transaction["sender"],
            transaction["timestamp"]
        )

        network_result=get_network_risk_for_transaction(
            transaction["transaction_id"],
            self.cycles
        )

        final_result=calculate_final_risk(
            transaction_result,
            account_result,
            network_result
        )

        return final_result