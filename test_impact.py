import unittest
from impact import analyze


class ImpactTests(unittest.TestCase):
    def models(self):
        return [{"name": "stg_orders", "tests": True}, {"name": "fct_sales", "depends_on": ["stg_orders"], "tests": True}, {"name": "report", "depends_on": ["fct_sales"]}]

    def test_finds_downstream_impact(self):
        report = analyze(self.models(), "stg_orders")
        self.assertEqual(report["impacted"], ["fct_sales", "report"])

    def test_returns_minimal_rerun_set(self):
        self.assertEqual(analyze(self.models(), "fct_sales")["rerun"], ["fct_sales", "report"])

    def test_flags_untested_model(self):
        self.assertEqual(analyze(self.models())["untested"], ["report"])


if __name__ == "__main__":
    unittest.main()
