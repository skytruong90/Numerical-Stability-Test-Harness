from stability_harness.core import integrate,run_sweep

def test_rk4_more_accurate_than_euler()->None:
    exact=2.718281828459045**-1
    assert abs(integrate("rk4",0.1,1,1)-exact)<abs(integrate("euler",0.1,1,1)-exact)

def test_sweep_passes()->None:
    assert run_sweep({"time_steps":[0.1,0.05],"max_rk4_error":0.001})["passed"]
