import json
import math

import pandas as pd


with open("portfolio_data.json", encoding="utf-8") as file:
    portfolios = json.load(file)

trades = pd.read_csv("trades_test.csv")
results = []

for _, trade in trades.iterrows():
    portfolio = portfolios.get(str(trade["portfolio_id"]))
    decision = None
    reason = None

    if portfolio is None:
        decision = "Rejected"
        reason = "Portfolio not found"
    else:
        try:
            quantity = float(trade["quantity"])
            price = float(trade["price"])
            action = trade["action"]
            security_id = trade["security_id"]
        except (KeyError, TypeError, ValueError, OverflowError):
            quantity = 0
            price = 0
            action = ""
            security_id = ""
            decision = "Rejected"
            reason = "Invalid trade data."

        if decision is None:
            if (
                not math.isfinite(quantity)
                or not math.isfinite(price)
                or quantity <= 0
                or price <= 0
                or action not in ["Buy", "Sell"]
            ):
                decision = "Rejected"
                reason = "Invalid trade data."
            elif security_id in portfolio["restricted_securities"]:
                decision = "Rejected"
                reason = "Security is restricted for this portfolio."
            elif action == "Sell":
                holding = None
                for current_holding in portfolio["current_holdings"]:
                    if current_holding["security_id"] == security_id:
                        holding = current_holding
                        break

                if holding is None or holding["quantity"] < quantity:
                    decision = "Rejected"
                    reason = "Insufficient holdings to sell."
                else:
                    decision = "Approved"
                    reason = "Trade passed all compliance checks."
            else:
                cost = quantity * price
                if cost > portfolio["cash_balance"]:
                    decision = "Rejected"
                    reason = "Insufficient cash for this buy order."
                else:
                    existing_holding = None
                    other_value = 0
                    for current_holding in portfolio["current_holdings"]:
                        if current_holding["security_id"] == security_id:
                            if existing_holding is None:
                                existing_holding = current_holding
                        else:
                            other_value += (
                                current_holding["quantity"]
                                * current_holding["market_price"]
                            )

                    existing_quantity = (
                        existing_holding["quantity"] if existing_holding else 0
                    )
                    post_trade_cash = portfolio["cash_balance"] - cost
                    post_trade_quantity = existing_quantity + quantity
                    post_trade_value = post_trade_quantity * price
                    total_value = post_trade_cash + post_trade_value + other_value
                    position_pct = post_trade_value / total_value

                    if position_pct > portfolio["max_position_pct"]:
                        decision = "Needs Manual Sign-off"
                        reason = (
                            "Exceeds maximum position concentration — "
                            "requires approval."
                        )
                    else:
                        decision = "Approved"
                        reason = "Trade passed all compliance checks."

    result = trade.to_dict()
    result["decision"] = decision
    result["reason"] = reason
    results.append(result)

pd.DataFrame(results).to_csv("output.csv", index=False)
print("Done. Results saved to output.csv")
