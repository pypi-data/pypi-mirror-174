from unittest import TestCase
from orkg import ORKG
import numpy as np


class TestTemplates(TestCase):
    """
    Some test scenarios might need to be adjusted to the content of the running ORKG instance
    """
    orkg = ORKG(host="https://sandbox.orkg.org")

    def test_materialize(self):
        self.orkg.templates.materialize_templates(templates=['R12002'], verbose=False)
        print(self.orkg.templates.list_templates())
        self.assertTrue(True)

    def test_df_template(self):
        from pandas import DataFrame as df
        lst = ['this', 'is', 'fancy']
        lst2 = [4, 2, np.nan]
        param = df(list(zip(lst, lst2)), columns=['word', 'length'])
        self.orkg.templates.materialize_template(template_id='R199091')
        self.orkg.templates.test_df(label="what!", dataset=(param, 'Fancy Table'), uses_library="pyORKG").pretty_print(format='json-ld')
        self.assertTrue(True)

    def test_something(self):
        from math import ceil
        import pandas as pd
        from scipy.stats import ttest_ind
        self.orkg.templates.materialize_template('R12002')
        tp = self.orkg.templates

        df = pd.read_csv('data.csv')
        tt = ttest_ind(df['non-failing heart (NF)'],
                       df['failing heart (F)'],
                       equal_var=False, nan_policy='omit')
        pvalue = tt.pvalue
        pvalue_ceil = ceil(pvalue * 1000) / 1000.0
        pvalue_str = '{:.16f}'.format(pvalue)

        tp.students_ttest(
            label='Statistically significant hypothesis test with IRE binding dependent variable on failing and non-failing hearts (p<{})'.format(
                pvalue_ceil),
            has_dependent_variable='http://purl.obolibrary.org/obo/GO_0030350',
            # the study design dependent variable (iron-responsive element binding)
            has_specified_input=(
            df, 'Summary data showing iron-responsive element (IRE) binding activity in LV tissue samples'),
            # the input dataset
            has_specified_output=tp.pvalue('the p-value of the statistical hypothesis test (p<{})'.format(pvalue_ceil),
                                           tp.scalar_value_specification('{}'.format(pvalue_str), pvalue_str)
                                           ),
        ).serialize_to_file('article.contribution.1.json', format='json-ld')
        self.assertTrue(True)

