"""Streamlit behavior checks for Mercier and the Golf PHEV example.

Install requirements.txt, then run: python -m unittest -v test_app.py
"""

from pathlib import Path
import unittest

from streamlit.testing.v1 import AppTest


APP = Path(__file__).with_name("app.py")
MERCIER = "Mercier Auto — volontaire (2026)"
PHEV = "Hybride rechargeable (PHEV)"
INTERENCHERES = "Interencheres LIVE / Chrono"


class MercierAppTests(unittest.TestCase):
    def assert_app_ok(self, app):
        self.assertEqual(len(app.exception), 0, [exception.message for exception in app.exception])

    def metric(self, app, label_prefix):
        matches = [metric.value for metric in app.metric if metric.label.startswith(label_prefix)]
        self.assertEqual(len(matches), 1, (label_prefix, matches))
        return matches[0]

    def new_app(self, *, preset=False):
        app = AppTest.from_file(APP, default_timeout=15)
        if preset:
            app.query_params["preset"] = "mercier-golf-gte"
        app.run()
        self.assert_app_ok(app)
        return app

    def golf(self):
        app = self.new_app()
        button = next(button for button in app.button if "Golf GTE PHEV" in button.label)
        button.click().run()
        self.assert_app_ok(app)
        return app

    def test_default_profile_and_golf_button(self):
        app = self.new_app()
        self.assertEqual(app.selectbox(key="sale_profile").value, "Alcopa Auction (2026)")
        next(button for button in app.button if "Golf GTE PHEV" in button.label).click().run()
        self.assert_app_ok(app)
        self.assertEqual(app.selectbox(key="sale_profile").value, MERCIER)
        self.assertEqual(app.selectbox(key=f"mercier_energy_{MERCIER}").value, PHEV)
        self.assertEqual(app.number_input(key="hammer_main").value, 10000)
        self.assertEqual(app.number_input(key="budget_max").value, 12000)
        self.assertEqual(self.metric(app, "À payer à la maison"), "11 608,00 €")
        self.assertEqual(self.metric(app, "Enchère maximale au palier"), "10 300,00 €")

    def test_phev_battery_requires_explicit_confirmation(self):
        app = self.golf()
        battery_key = f"mercier_battery_{MERCIER}_{PHEV}"
        self.assertFalse(app.checkbox(key=battery_key).value)
        app.checkbox(key=battery_key).check().run()
        self.assert_app_ok(app)
        self.assertEqual(self.metric(app, "À payer à la maison"), "11 648,00 €")
        app.checkbox(key=battery_key).uncheck().run()
        self.assert_app_ok(app)
        self.assertEqual(self.metric(app, "À payer à la maison"), "11 608,00 €")

    def test_channels_change_only_the_live_surcharge(self):
        app = self.golf()
        for channel, invoice in [
            ("Salle / ordre hors Internet", "11 548,00 €"),
            ("LIVE de la maison", "11 578,00 €"),
            (INTERENCHERES, "11 608,00 €"),
        ]:
            with self.subTest(channel=channel):
                app.selectbox(key=f"platform_{MERCIER}").select(channel).run()
                self.assert_app_ok(app)
                self.assertEqual(self.metric(app, "À payer à la maison"), invoice)
                self.assertEqual(app.number_input(key=f"dossier_{MERCIER}").value, 120)

    def test_ht_input_and_return_to_ttc(self):
        app = self.golf()
        app.radio(key=f"mercier_price_basis_{MERCIER}").set_value("HT à convertir en TTC").run()
        self.assert_app_ok(app)
        self.assertEqual(app.number_input(key=f"mercier_vehicle_vat_{MERCIER}").value, 20)
        self.assertEqual(self.metric(app, "À payer à la maison"), "13 893,60 €")
        self.assertEqual(self.metric(app, "Enchère maximale au palier"), "8 600,00 €")
        app.radio(key=f"mercier_price_basis_{MERCIER}").set_value("TTC").run()
        self.assert_app_ok(app)
        self.assertEqual(self.metric(app, "À payer à la maison"), "11 608,00 €")

    def test_reserve_and_invoice_only_budget_scope(self):
        app = self.golf()
        app.number_input(key="repairs_main").set_value(2000).run()
        self.assert_app_ok(app)
        self.assertEqual(self.metric(app, "À payer à la maison"), "11 608,00 €")
        self.assertEqual(self.metric(app, "Budget tout compris"), "13 608,00 €")
        self.assertEqual(self.metric(app, "Enchère maximale au palier"), "8 500,00 €")
        self.assertEqual(app.number_input(key="repair_budget").value, 2000)
        app.checkbox(key="reuse_after_sale").uncheck().run()
        app.number_input(key="repair_budget").set_value(1000).run()
        self.assert_app_ok(app)
        self.assertEqual(self.metric(app, "Enchère maximale au palier"), "9 400,00 €")
        app.radio(key="budget_scope").set_value("Facture de la maison uniquement").run()
        self.assert_app_ok(app)
        self.assertEqual(self.metric(app, "Enchère maximale au palier"), "10 300,00 €")
        self.assertTrue(app.number_input(key="repair_budget").disabled)

    def test_deposit_changes_balance_not_cost_or_bid_ceiling(self):
        app = self.golf()
        app.number_input(key=f"mercier_deposit_{MERCIER}").set_value(2000).run()
        self.assert_app_ok(app)
        self.assertEqual(self.metric(app, "À payer à la maison"), "11 608,00 €")
        self.assertEqual(self.metric(app, "Enchère maximale au palier"), "10 300,00 €")
        self.assertTrue(any("9 608,00 €" in message.value for message in app.info))

    def test_query_preset_does_not_reset_user_edits_on_rerun(self):
        app = self.new_app(preset=True)
        self.assertEqual(app.selectbox(key="sale_profile").value, MERCIER)
        app.number_input(key="hammer_main").set_value(9300).run()
        app.run()
        self.assert_app_ok(app)
        self.assertEqual(app.number_input(key="hammer_main").value, 9300)
        self.assertEqual(self.metric(app, "À payer à la maison"), "10 808,04 €")


if __name__ == "__main__":
    unittest.main()
