"""SoT — configs de lab estáveis e importáveis."""

from econofisica.labs import M01_VENDEDOR, M01_GBM


def test_m01_defaults():
    c = M01_VENDEDOR
    assert c.S0 == c.K == 100.0
    assert c.premio == 7.0
    assert c.N == 1000
    assert c.seed == 42


def test_m01_gbm_defaults():
    c = M01_GBM
    assert c.sample_sizes == (1_000, 10_000, 100_000)
    assert c.N_max == 100_000
    assert c.sigma == 0.02
    assert c.sigma_wide == 0.20
    assert "lab-m01-gbm" in c.output_rel
