"""
Tests for modeling
"""

import astropy
from numpy import testing as tst

from clmm import modeling as pp

density_profile_parametrization = 'nfw'
mass_lims = (1.e12, 1.e16)
mass_Delta = 200
cluster_mass = 1.e15
cluster_concentration = 4

# cosmo_ccl = ccl.Cosmology(Omega_c=0.27, Omega_b=0.045, h=0.67, A_s=2.1e-9, n_s=0.96)
astropy_cosmology_object = astropy.cosmology.FlatLambdaCDM(H0=70, Om0=0.27, Ob0=0.045)
cosmo_ccl = pp._cclify_astropy_cosmo(astropy_cosmology_object)

def test_cosmo_type():
    tst.assert_equal(type(cosmo_apy), astropy.cosmology.FlatLambdaCDM)
    tst.assert_equal(type(cosmo_ccl), dict)
    tst.assert_equal(cosmo_ccl['Omega_c'] + cosmo_ccl['Omega_b'], cosmo_apy.Odm_0 + cosmo_apy.Ob_0)

r3d = np.logspace(-2, 2, 100)
r3d_one = r3d[-1]

rho = pp.get_3d_density(r3d, mdelta=cluster_mass, cdelta=cluster_concentration, cosmo=cosmo_ccl)
rho_one = pp.get_3d_density(r3d_one, mdelta=cluster_mass, cdelta=cluster_concentration, cosmo=cosmo_ccl)

def test_rho():
    tst.assert_equal(rho[-1], rho_one)

Sigma = pp.predict_surface_density(r3d, cluster_mass, cluster_concentration, cosmo=cosmo_ccl, Delta=200, halo_profile_parameterization='nfw')
Sigma_one = pp.predict_surface_density(r3d_one, cluster_mass, cluster_concentration, cosmo=cosmo_ccl, Delta=200, halo_profile_parameterization='nfw')

def test_Sigma():
    assert(np.all(Sigma > 0.))
    tst.assert_equal(Sigma[-1], Sigma_one)

DeltaSigma = pp.predict_excess_surface_density(r3d, cluster_mass, cluster_concentration, cosmo=cosmo_ccl, Delta=200, halo_profile_parameterization='nfw')
DeltaSigma_one = pp.predict_excess_surface_density(r3d_one, cluster_mass, cluster_concentration, cosmo=cosmo_ccl, Delta=200, halo_profile_parameterization='nfw')

def test_DeltaSigma():
    tst.assert_equal(DeltaSigma[-1], DeltaSigma_one)
    assert(np.all(DeltaSigma > 0.))
    assert(DeltaSigma_one > 0.)

Sigmac = pp.get_critical_surface_density(cosmo_ccl, z_cluster=1.0, z_source=2.0)

def test_Sigmac():
    # not sure what to put here yet

gammat = pp.predict_tangential_shear(r3d, mdelta=cluster_mass, cdelta=cluster_concentration, z_cluster=1.0, z_source=2.0, cosmo=cosmo_ccl, Delta=200, halo_profile_parameterization='nfw', z_src_model='single_plane')
gammat_one = pp.predict_tangential_shear(r3d_one, mdelta=cluster_mass, cdelta=cluster_concentration, z_cluster=1.0, z_source=2.0, cosmo=cosmo_ccl, Delta=200, halo_profile_parameterization='nfw', z_src_model='single_plane')

def test_gammat():
    tst.assert_equal(gammat[-1], gammat_one)
    tst.assert_equal(gammat, DeltaSigma / Sigmac)
    tst.assert_equal(gammat_one, DeltaSigma_one / Sigmac)

kappa = pp.predict_convergence(r3d, mdelta=cluster_mass, cdelta=cluster_concentration, z_cluster=1.0, z_source=2.0, cosmo=cosmo_ccl, Delta=200, halo_profile_parameterization='nfw', z_src_model='single_plane')
kappa_one = pp.predict_convergence(r3d_one, mdelta=cluster_mass, cdelta=cluster_concentration, z_cluster=1.0, z_source=2.0, cosmo=cosmo_ccl, Delta=200, halo_profile_parameterization='nfw', z_src_model='single_plane')

def test_kappa():
    tst.assert_equal(kappa[-1], kappa_one)
    assert(kappa_one > 0.
    assert(np.all(kappa > 0.))


gt = pp.predict_reduced_tangential_shear(r3d, mdelta=cluster_mass, cdelta=cluster_concentration, z_cluster=1.0, z_source=2.0, cosmo=cosmo_ccl, Delta=200, halo_profile_parameterization='nfw', z_src_model='single_plane')
gt_one = pp.predict_reduced_tangential_shear(r3d_one, mdelta=cluster_mass, cdelta=cluster_concentration, z_cluster=1.0, z_source=2.0, cosmo=cosmo_ccl, Delta=200, halo_profile_parameterization='nfw', z_src_model='single_plane')

def test_gt():
    tst.assert_equal(gt[-1], gt_one)
    tst.assert_equal(gt, gammat / (1. - kappa))
    tst.assert_equal(gt_one, gammat_one / (1. - kappa_one))

# others: test that inputs are as expected, values from demos
# positive values from sigma onwards