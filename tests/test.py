import unittest

from agent.graph import graph

class GraphTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_all(self):
        resp = await graph.ainvoke({
            "today_sales": 100,
            "today_costs": 200,
            "today_customers": 2,
            "yesterday_sales": 50,
            "yesterday_costs": 100,
            "yesterday_customers": 2
        })
        expected = {
            "status": "loss",
            "warnings": [
                "CAC is increased!"
            ],
            "recommendations": [
                "Your sales are growing. Consider increase advertising budget.",
                "You are in loss! Reduce costs.",
                "CAC is growing significantly! Review marketing campaigns."
            ]
        }
        self.assertEqual(resp, expected)
    async def test_warn_sales_loss(self):
        resp = await graph.ainvoke({
            "today_sales": 100,
            "today_costs": 200,
            "today_customers": 18,
            "yesterday_sales": 50,
            "yesterday_costs": 100,
            "yesterday_customers": 10
        })
        expected = {
            "status": "loss",
            "warnings": [
                "CAC is increased!"
            ],
            "recommendations": [
                "Your sales are growing. Consider increase advertising budget.",
                "You are in loss! Reduce costs."
            ]
        }
        self.assertEqual(resp, expected)
    async def test_warn_sales_cac(self):
        resp = await graph.ainvoke({
            "today_sales": 400,
            "today_costs": 200,
            "today_customers": 2,
            "yesterday_sales": 300,
            "yesterday_costs": 100,
            "yesterday_customers": 2
        })
        expected = {
            "status": "profit",
            "warnings": [
                "CAC is increased!"
            ],
            "recommendations": [
                "Your sales are growing. Consider increase advertising budget.",
                "CAC is growing significantly! Review marketing campaigns."
            ]
        }
        self.assertEqual(resp, expected)
    async def test_nothing(self):
        resp = await graph.ainvoke({
            "today_sales": 300,
            "today_costs": 200,
            "today_customers": 20,
            "yesterday_sales": 300,
            "yesterday_costs": 100,
            "yesterday_customers": 2
        })
        expected = {
            "status": "profit",
            "warnings": [],
            "recommendations": []
        }
        self.assertEqual(resp, expected)
    async def test_sales_grow(self):
        resp = await graph.ainvoke({
            "today_sales": 800,
            "today_costs": 400,
            "today_customers": 20,
            "yesterday_sales": 500,
            "yesterday_costs": 600,
            "yesterday_customers": 10
        })
        expected = {
            'status': 'profit',
            'warnings': [],
            'recommendations': [
                'Your sales are growing. Consider increase advertising budget.'
            ]
        }
        self.assertEqual(resp, expected)
    async def test_no_profit_no_loss(self):
        resp = await graph.ainvoke({
            "today_sales": 700,
            "today_costs": 700,
            "today_customers": 5,
            "yesterday_sales": 300,
            "yesterday_costs": 100,
            "yesterday_customers": 2
        })
        expected = {
            "status": "no profit, no loss",
            "warnings": [
                "CAC is increased!"
            ],
            "recommendations": [
                "Your sales are growing. Consider increase advertising budget.",
                "CAC is growing significantly! Review marketing campaigns."
            ]
        }
        self.assertEqual(resp, expected)
