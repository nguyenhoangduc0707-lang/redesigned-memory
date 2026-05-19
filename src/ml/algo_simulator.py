from dataclasses import dataclass


@dataclass
class CampaignScenario:
    budget: float
    post_count: int
    conversion_rate: float
    avg_order_value: float
    commission_rate: float = 0.1


class AlgoSimulator:
    def simulate(self, scenario: CampaignScenario):
        reach = max(scenario.post_count, 0) * 1200
        clicks = reach * 0.035
        sales = clicks * max(scenario.conversion_rate, 0)
        revenue = sales * max(scenario.avg_order_value, 0)
        commission = revenue * max(scenario.commission_rate, 0)
        roi = (commission - scenario.budget) / scenario.budget if scenario.budget else 0
        return {
            "reach": round(reach),
            "clicks": round(clicks, 2),
            "sales": round(sales, 2),
            "revenue": round(revenue, 2),
            "commission": round(commission, 2),
            "roi": round(roi, 4),
        }


def simulate_campaign(**kwargs):
    return AlgoSimulator().simulate(CampaignScenario(**kwargs))


if __name__ == "__main__":
    print(simulate_campaign(budget=1000000, post_count=12, conversion_rate=0.02, avg_order_value=250000))
