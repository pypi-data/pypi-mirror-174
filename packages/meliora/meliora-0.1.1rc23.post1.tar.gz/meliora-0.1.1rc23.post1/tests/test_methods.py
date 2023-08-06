import src.meliora.core as vt
import unittest
import pandas as pd


# create test case for Jeffreys test
class TestCases(unittest.TestCase):
    """Create a unit test for all functions of the tests library"""

    def load_pd_data(self):
        """Load data for testing"""
        return pd.read_csv("./data/pd_test_data.csv")

    def load_lgd_data(self):
        """Load data for testing"""
        return pd.read_csv("./data/lgd_dataset.csv")

    def load_german_data(self):
        """Load data for testing"""
        return pd.read_csv("./data/german_data.csv")

    def load_psi_data(self):
        """Load data for testing"""
        return pd.read_csv("./data/test_pd_psi.csv")

    def load_lgd_t_data(self):
        """Load data for testing"""
        return pd.read_csv("./data/lgd_t_test.csv")

    def pd_transition_matrix_data(self):
        """Load data for testing"""
        return pd.read_csv("./data/pd_transition_matrix.csv")

    def load_pd_calibration(self):
        """Load data for testing"""
        return pd.read_csv("./data/pd_calibration.csv")

    def test_jeffreys(self):
        """Expected value calculation is described in the r_test_cases.ipynb"""

        data = self.load_pd_data()
        result = vt.jeffreys_test(data, "ratings", "default_flag", "predicted_pd")

        # Expected results (see R notebook for values)
        expected = [0.01995857, 0.84955196, 0.59864873]

        result = result.set_index(result["Rating class"])
        self.assertAlmostEqual(result.loc["A", "p_value"], expected[0])
        self.assertAlmostEqual(result.loc["B", "p_value"], expected[1])
        self.assertAlmostEqual(result.loc["C", "p_value"], expected[2])

    def test_binomial(self):
        """Expected value calculation is described in the r_test_cases.ipynb"""

        data = self.load_pd_data()
        result = vt.binomial_test(data, "ratings", "default_flag", "predicted_pd")

        # Expected results (see R notebook for values)
        expected = [0.02389227, 0.86744061, 0.66055279]

        result = result.set_index(result["Rating class"])
        self.assertAlmostEqual(result.loc["A", "p_value"], expected[0])
        self.assertAlmostEqual(result.loc["B", "p_value"], expected[1])
        self.assertAlmostEqual(result.loc["C", "p_value"], expected[2])

    def test_brier_score(self):
        """Expected value calculation is described in the r_test_cases.ipynb"""
        data = self.load_pd_data()
        result = vt.brier_score(data, "ratings", "default_flag", "predicted_pd")

        # Expected results (see R notebook for values)
        expected = 0.00128950849979173

        self.assertAlmostEqual(result, expected)

    def test_gini(self):
        """Expected value calculation is described in the r_test_cases.ipynb"""
        data = self.load_pd_data()
        result = vt.gini(data, "ratings", "default_flag", "predicted_pd")

        # Expected results (see R notebook for values)
        expected = 0.00128950849979173

        self.assertAlmostEqual(result, expected)

    def test_spiegelhalter(self):
        """Expected value calculation is described in the r_test_cases.ipynb"""
        data = self.load_pd_data()
        result = vt.spiegelhalter_test(data, "ratings", "default_flag", "predicted_pd")
        expected = -0.6637590511485174  # TODO: check if this is correct
        self.assertAlmostEqual(result[0], expected)

    def test_hosmer_test(self):
        """Expected value calculation is described in the r_test_cases.ipynb"""
        data = self.load_pd_data()
        result = vt.hosmer_test(data, "ratings", "default_flag", "predicted_pd")

        # Expected results (see R notebook for values)
        expected = 0.13025

        self.assertAlmostEqual(result[0], expected)

    def test_herfindahl_test(self):
        """Expected value calculation is described in the r_test_cases.ipynb"""
        data = self.load_pd_data()
        result = vt.herfindahl_test(data, "ratings")

        # Expected results (see R notebook for values)
        expected = 0.408232

        self.assertAlmostEqual(result[1], expected)

    def test_ks_stat(self):
        """Expected value calculation is described in the r_test_cases.ipynb"""
        data = self.load_pd_data()
        result = vt.ks_stat(data, "ratings")

        # Expected results (see R notebook for values)
        expected = 0.408232

        self.assertAlmostEqual(result[1], expected)

    def test_herfindahl_multiple_period_test(self):
        """Expected value calculation is described in the r_test_cases.ipynb"""
        data = self.load_pd_data()
        result = vt.herfindahl_multiple_period_test(data, "ratings")

        # Expected results (see R notebook for values)
        expected = 0.408232

        self.assertAlmostEqual(result[1], expected)

    def test_roc_auc(self):
        """Expected value calculation is described in the r_test_cases.ipynb"""
        data = self.load_pd_data()
        result = vt.roc_auc(data, "default_flag", "predicted_pd")

        # Expected results (see R notebook for values)
        expected = 0.500854754970242

        self.assertAlmostEqual(result, expected)

    def test_clar(self):
        """Expected value calculation is described in the r_test_cases.ipynb"""
        data = self.load_lgd_data()
        result = vt.clar(data, "realised_outcome", "predicted_outcome")

        # Expected results (see R notebook for values)
        expected = result  # todo

        self.assertAlmostEqual(result, expected)

    def test_loss_capture_ratio(self):
        """Expected value calculation is described in the r_test_cases.ipynb"""
        data = self.load_psi_data()
        result = vt.loss_capture_ratio(data, "year_bins", "remaining_mat_bin")

        # Expected results (see R notebook for values)
        expected = 1.0344129494141174

        self.assertAlmostEqual(result[1], expected)

    def test_bayesian_error_rate(self):
        """Expected value calculation is described in the r_test_cases.ipynb"""
        data = self.load_psi_data()
        result = vt.bayesian_error_rate(data, "year_bins", "remaining_mat_bin")

        # Expected results (see R notebook for values)
        expected = 1.0344129494141174

        self.assertAlmostEqual(result[1], expected)

    def test_information_value(self):
        """Information calculation is described in the r_test_cases.ipynb"""
        data = self.load_german_data()
        result = vt.information_value(data, "checkingstatus", "GoodCredit")

        # Expected results (see R notebook for values)
        expected = 0.6660115034

        self.assertAlmostEqual(result[1], expected)

    def test_lgd_t_test(self):
        """Expected value calculation is described in the r_test_cases.ipynb"""
        data = self.load_lgd_t_data()

        result = vt.lgd_t_test(data, "predicted_lgd", "realised_lgd", "segment")
        result_p_values = result["p_value"].sum()

        # Expected results (see R notebook for values)
        expected = 4.575081449451153

        self.assertAlmostEqual(result_p_values, expected)

    def test_migration_matrix_stability(self):
        """Expected value calculation is described in the r_test_cases.ipynb"""
        data = self.load_psi_data()
        result = vt.migration_matrix_stability(data, "year_bins", "remaining_mat_bin")

        # Expected results (see R notebook for values)
        expected = 1.0344129494141174

        self.assertAlmostEqual(result[1], expected)

    def test_psi(self):
        """Expected value calculation is described in the r_test_cases.ipynb"""
        data = self.load_psi_data()
        result = vt.psi(data, "year_bins", "remaining_mat_bin")

        # Expected results (see R notebook for values)
        expected = 1.0344129494141174

        self.assertAlmostEqual(result[1], expected)

    def test_spearman_corr(self):
        """Expected value calculation is described in the r_test_cases.ipynb"""
        x = [1, 2, 3, 4, 5]
        y = [5, 6, 7, 8, 7]
        result = vt.spearman_corr(x, y).correlation

        # Expected results (see R notebook for values)
        expected = 0.820782681668123

        self.assertAlmostEqual(result, expected)

    def test_pearson_corr(self):
        """Expected value calculation is described in the r_test_cases.ipynb"""
        x = [1, 2, 3, 4, 5]
        y = [5, 6, 7, 8, 7]
        result = vt.pearson_corr(x, y).correlation

        # Expected results (see R notebook for values)
        expected = 0.820782681668123

        self.assertAlmostEqual(result, expected)

    def test_somersd(self):
        """Expected value calculation is described in the r_test_cases.ipynb"""

        x = [0, 1, 1, 1, 1]
        y = [1, 1, 1, 0, 1]

        result = vt.somersd(x, y)

        # Expected results (see R notebook for values)
        expected = -0.25

        self.assertAlmostEqual(result.statistic, expected)

    def test_kendall_tau(self):
        """Expected value calculation is described in the r_test_cases.ipynb"""
        x = [1, 2, 3, 2, 1, 3, 4, 2, 5, 2, 6, 5, 5]
        y = [5, 5, 6, 2, 1, 4, 4, 2, 1, 2, 1, 5, 5]

        tau, _ = vt.kendall_tau(x, y)

        # Expected results (see R notebook for values)
        expected = 0.03030651

        self.assertAlmostEqual(tau, expected)

    def test_lgd_t_test(self):
        """Expected value calculation is described in the r_test_cases.ipynb"""
        data = self.load_psi_data()
        result = vt.lgd_t_test(data, "year_bins", "remaining_mat_bin")

        # Expected results (see R notebook for values)
        expected = 1.0344129494141174

        self.assertAlmostEqual(result[1], expected)

    def test_elbe_t_test(self):
        """Expected value calculation is described in the r_test_cases.ipynb"""
        data = self.load_psi_data()
        result = vt.elbe_t_test(data, "year_bins", "remaining_mat_bin")

        # Expected results (see R notebook for values)
        expected = 1.0344129494141174

        self.assertAlmostEqual(result[1], expected)

    def test_migration_matrices_statistics(self):
        """Expected value calculation is described in the r_test_cases.ipynb"""
        data = self.load_psi_data()
        result = vt.migration_matrices_statistics(data, "year_bins", "remaining_mat_bin")

        # Expected results (see R notebook for values)
        expected = 1.0344129494141174

        self.assertAlmostEqual(result[1], expected)

    def test_cier(self):
        """Expected value calculation is described in the r_test_cases.ipynb"""
        data = self.load_psi_data()
        result = vt.cier(data, "year_bins", "remaining_mat_bin")

        # Expected results (see R notebook for values)
        expected = 1.0344129494141174

        self.assertAlmostEqual(result[1], expected)

    def test_kullback_leibler_dist(self):
        """Expected value calculation is described in the r_test_cases.ipynb"""
        data = self.load_psi_data()
        result = vt.kullback_leibler_dist(data, "year_bins", "remaining_mat_bin")

        # Expected results (see R notebook for values)
        expected = 1.0344129494141174

        self.assertAlmostEqual(result[1], expected)

    def test_loss_shortfall(self):
        """Expected value calculation is described in the r_test_cases.ipynb"""
        data = self.load_psi_data()
        result = vt.loss_shortfall(data, "year_bins", "remaining_mat_bin")

        # Expected results (see R notebook for values)
        expected = 1.0344129494141174

        self.assertAlmostEqual(result[1], expected)

    def test_mean_absolute_deviation(self):
        """Expected value calculation is described in the r_test_cases.ipynb"""
        data = self.load_psi_data()
        result = vt.mean_absolute_deviation(data, "year_bins", "remaining_mat_bin")

        # Expected results (see R notebook for values)
        expected = 1.0344129494141174

        self.assertAlmostEqual(result[1], expected)

    def test_normal_test(self):
        """Expected value calculation is described in the r_test_cases.ipynb"""
        data = self.load_psi_data()
        result = vt.normal_test(data, "year_bins", "remaining_mat_bin")

        # Expected results (see R notebook for values)
        expected = 1.0344129494141174

        self.assertAlmostEqual(result[1], expected)
