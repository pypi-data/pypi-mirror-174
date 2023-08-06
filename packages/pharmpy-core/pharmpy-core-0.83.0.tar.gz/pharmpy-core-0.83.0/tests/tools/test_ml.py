import sys

import pytest

from pharmpy.modeling import load_example_model
from pharmpy.tools import predict_influential_individuals, predict_outliers


@pytest.mark.skipif(
    sys.version_info >= (3, 10), reason="Skipping tests requiring tflite for Python 3.10"
)
def test_predict_outliers():
    model = load_example_model('pheno')
    res = predict_outliers(model, model.modelfit_results)
    assert len(res) == 59
    assert res['residual'][1] == pytest.approx(-0.28144291043281555)


@pytest.mark.skipif(
    sys.version_info >= (3, 10), reason="Skipping tests requiring tflite for Python 3.10"
)
def test_predict_influential_individuals():
    model = load_example_model('pheno')
    res = predict_influential_individuals(model, model.modelfit_results)
    assert len(res) == 59
    assert res['dofv'][59] == pytest.approx(0.08806940913200378)
