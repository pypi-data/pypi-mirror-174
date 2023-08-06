import argparse
import datetime as dt
import unittest

import numpy as np
import pandas as pd

import lumipy as lm
import lumipy.provider as lp
from test.integration.base_intergration_test import BaseIntegrationTest
from test.provider.int_test_providers import (
    ParameterAndLimitTestProvider,
    TableParameterTestProvider,
    FilteringTestProvider,
    ColumnValidationTestProvider,
)


def make_test_df():
    return pd.DataFrame([
        {f'Col{k}': i * j for i, k in enumerate('ABCDEF')}
        for j in range(1000)
    ])


class TestPythonProviderIntegration2(BaseIntegrationTest):

    def _check_provider_attr_exists(self, attr_name):
        self.assertTrue(
            hasattr(self.atlas, attr_name),
            msg=f'The expected provider \'{attr_name}\' was not found in the atlas'
        )

    def test_pandas_provider(self):

        self._check_provider_attr_exists('pandas_integration_test')

        pit = self.atlas.pandas_integration_test()
        df = pit.select('*').go()

        self.assertSequenceEqual(df.shape, [1000, 6])
        self.assertTrue((make_test_df() == df).all().all())

    def test_filter_pushdown(self):

        self._check_provider_attr_exists('test_pyprovider_filter')

        f = self.atlas.test_pyprovider_filter()
        df = f.select('*').where(f.node_id * 2 >= 0).go()

        self.assertSequenceEqual(df.shape, [5, 3])
        self.assertSequenceEqual(df.OpName.tolist(), ['Gte', 'Multiply', 'ColValue', 'NumValue', 'NumValue'])

    def test_parameters_and_limit(self):

        self._check_provider_attr_exists('test_pyprovider_paramsandlimit')

        para = self.atlas.test_pyprovider_paramsandlimit(param5=dt.date(2022, 1, 1))
        df = para.select('*').limit(100).go()
        self.assertSequenceEqual(df.shape, [7, 3])

        with self.assertRaises(ValueError) as ve:
            self.atlas.test_pyprovider_paramsandlimit().select('*').go()

    def test_table_parameters(self):

        self._check_provider_attr_exists('test_pyprovider_tablevar')

        def random_val(i):
            if i % 4 == 0:
                return np.random.uniform()
            elif i % 4 == 1:
                return np.random.choice(list('zyxwv'))
            elif i % 4 == 2:
                return dt.datetime(2020, 1, 1) + dt.timedelta(days=np.random.randint(0, 100))
            elif i % 4 == 3:
                return np.random.randint(100)

        tv_df = pd.DataFrame([
            {k: random_val(i) for i, k in enumerate('ABCDEF')}
            for _ in range(10)
        ])
        tv = lm.from_pandas(tv_df)
        t = self.atlas.test_pyprovider_tablevar(test_table=tv)

        df = t.select('*').go()

        self.assertSequenceEqual(df.shape, [6, 4])
        self.assertSequenceEqual(df.TableVarNumCols.tolist(), [6] * df.shape[0])
        self.assertSequenceEqual(df.TableVarNumRows.tolist(), [10] * df.shape[0])
        self.assertSequenceEqual(
            df.TableVarColType.tolist(),
            ['float64', 'object', 'datetime64[ns, UTC]', 'int64', 'float64', 'object']
        )
        self.assertSequenceEqual(df.TableVarColName.tolist(), list('ABCDEF'))

    def test_output_dataframe_validation(self):

        self._check_provider_attr_exists('test_pyprovider_dataframe_validation')

        ok_cols = self.atlas.test_pyprovider_dataframe_validation(has_bad_cols=False)
        bad_cols = self.atlas.test_pyprovider_dataframe_validation(has_bad_cols=True)

        ok_df = ok_cols.select('*').go()
        self.assertSequenceEqual(ok_df.shape, [100, 5])

        with self.assertRaises(ValueError) as ve:
            bad_cols.select('*').go()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--domain', dest='domain', default='fbn-ci')
    parser.add_argument('--user_id', dest='user_id', required=True)
    parser.add_argument('--certs_path', dest='certs_path', required=False)
    args = parser.parse_args()

    if args.certs_path:
        lp.copy_certs(args.certs_path)

    providers = [
        lp.PandasProvider(make_test_df(), 'integration.test', description='This is a test dataframe'),
        FilteringTestProvider(),
        ParameterAndLimitTestProvider(),
        TableParameterTestProvider(),
        ColumnValidationTestProvider(),
    ]

    with lp.ProviderManager(*providers, user=args.user_id, domain=args.domain, port=5002):
        runner = unittest.TextTestRunner(verbosity=2)
        loader = unittest.TestLoader()
        runner.run(loader.loadTestsFromTestCase(TestPythonProviderIntegration2))
