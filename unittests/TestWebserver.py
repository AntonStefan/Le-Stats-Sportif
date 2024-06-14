import unittest
from data_ingestor import DataIngestor
from calculus_routes import calculate_mean_by_category, calculate_state_mean, calculate_state_mean_by_category, calculate_states_mean, calculate_best5, calculate_worst5, calculate_global_mean, calculate_diff_from_mean, calculate_state_diff_from_mean


class TestCalculate(unittest.TestCase):
    def setUp(self):
        self.data_ingestor = DataIngestor("./test.csv")  # Use your actual CSV file path


    def test_calculate_state_mean_with_valid_data(self):

        # Test with valid data
        question_test = 'Percent of adults aged 18 years and older who have obesity'
        result = calculate_state_mean(self.data_ingestor, question_test, 'Ohio')
        expected_result = {'Ohio': 29.4}
        self.assertEqual(result, expected_result)
        self.assertIsNotNone(result)


    def test_calculate_states_mean_with_valid_data(self):

        # Test with valid data
        question_test = 'Percent of adults aged 18 years and older who have obesity'
        result = calculate_states_mean(self.data_ingestor, question_test)  # Call the function with the test data

        # Define expected result based on test data
        expected_result =  {'Alaska': 27.9,
                            'Ohio': 29.4,
                            'Pennsylvania': 30.2,
                            'North Carolina': 31.9,
                            'Georgia': 33.5,
                            'California': 33.8,
                            'Michigan': 35.9
                            }

        # Perform the assertion
        self.assertEqual(result, expected_result)
        self.assertIsNotNone(result)


    def test_calculate_best5_with_valid_data(self):

        # Test with valid data
        question_test = 'Percent of adults aged 18 years and older who have obesity'
        result = calculate_best5(self.data_ingestor, question_test)
        expected_result = {'Alaska': 27.9,
                           'Ohio': 29.4,
                           'Pennsylvania': 30.2,
                           'North Carolina': 31.9,
                           'Georgia': 33.5
                           }
        self.assertEqual(result, expected_result)
        self.assertIsNotNone(result)


    def test_calculate_worst5_handles_missing_values(self):

        # Test when there are missing values in the data
        question_test = 'Percent of adults aged 18 years and older who have obesity'

        # Modify the data to introduce missing values
        self.data_ingestor.df.loc[0, 'Data_Value'] = None
        result = calculate_worst5(self.data_ingestor, question_test)
        expected_result = {'Michigan': 35.9,
                          'California': 33.8,
                          'Georgia': 33.5,
                          'North Carolina': 31.9,
                          'Pennsylvania': 30.2
                          }
        self.assertEqual(result, expected_result)
        self.assertIsNotNone(result)


    def test_calculate_global_mean_with_valid_data(self):

        # Test with valid data
        question_test = 'Percent of adults aged 18 years and older who have obesity'
        result = calculate_global_mean(self.data_ingestor, question_test)

        # Expected global mean can be calculated manually based on the provided CSV data
        expected_result = {"global_mean": 31.8}
        self.assertEqual(result, expected_result)
        self.assertIsNotNone(result)

    def test_calculate_diff_from_mean_with_valid_data(self):

        # Test with valid data
        question_test = 'Percent of adults aged 18 years and older who have obesity'
        result = calculate_diff_from_mean(self.data_ingestor, question_test)

        # Expected result can be calculated manually based on the provided CSV data
        expected_result = {'Alaska': 3.900000000000002,
                            'California': -1.9999999999999964,
                            'Georgia': -1.6999999999999993,
                            'Michigan': -4.099999999999998,
                            'North Carolina': -0.09999999999999787,
                            'Ohio': 2.400000000000002,
                            'Pennsylvania': 1.6000000000000014
                            }

        self.assertEqual(result, expected_result)
        self.assertIsNotNone(result)


    def test_calculate_state_diff_from_mean_with_valid_data(self):

        # Test with valid data
        question_test = 'Percent of adults aged 18 years and older who have obesity'
        state_test = 'Ohio'  # Test with Ohio as the state
        result = calculate_state_diff_from_mean(self.data_ingestor, question_test, state_test)

        # Expected result can be calculated manually based on the provided CSV data
        expected_result = {'Ohio': 2.400000000000002}
        self.assertEqual(result, expected_result)
        self.assertIsNotNone(result)


    def test_calculate_mean_by_category_with_valid_data(self):

        # Test with valid data
        question_test = 'Percent of adults aged 18 years and older who have obesity'

        result = calculate_mean_by_category(self.data_ingestor, question_test)
        expected_result = {"('Alaska', 'Income', '$25,000 - $34,999')": 27.9, "('California', 'High school graduate', 'Education')": 33.8, "('Georgia', 'Male', 'Gender')": 33.5, "('Michigan', 'Hispanic', 'Race/Ethnicity')": 35.9, "('North Carolina', 'Black', 'Race/Ethnicity')": 31.9, "('Ohio', 'Male', 'Gender')": 29.4, "('Pennsylvania', 'Income', '$35,000 - $49,999')": 30.2}
        self.assertEqual(result, expected_result)
        self.assertIsNotNone(result)


    def test_calculate_state_mean_by_category_with_valid_data(self):

        # Test with valid data
        question_test = 'Percent of adults aged 18 years and older who have obesity'
        state_test = 'Ohio'
        result = calculate_state_mean_by_category(self.data_ingestor, question_test, state_test)

        # Since the result is a nested dictionary, we can check if the state key exists
        self.assertIn(state_test, result)

        # We can also check if the inner dictionary has any items
        self.assertTrue(result[state_test])

        expected_result = {'Ohio': {"('Male', 'Gender')": 29.4}}
        self.assertEqual(result, expected_result)

        # Or we can directly check if the result is not None
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()
