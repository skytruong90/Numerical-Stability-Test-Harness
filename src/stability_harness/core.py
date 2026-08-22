from __future__ import annotations
import math
from typing import Any,Callable

def _f(rate:float)->Callable[[float,float],float]: return lambda _t,y:-rate*y

def integrate(method:str,dt:float,duration:float,rate:float,y0:float=1.0)->float:
    f=_f(rate); y=y0; t=0.0
    for _ in range(round(duration/dt)):
        if method=="euler": y += dt*f(t,y)
        elif method=="rk4":
            k1=f(t,y); k2=f(t+dt/2,y+dt*k1/2); k3=f(t+dt/2,y+dt*k2/2); k4=f(t+dt,y+dt*k3); y += dt*(k1+2*k2+2*k3+k4)/6
        else: raise ValueError(method)
        t+=dt
        if not math.isfinite(y): return y
    return y

def run_sweep(cfg:dict[str,Any])->dict[str,Any]:
    duration=float(cfg.get("duration_s",5)); rate=float(cfg.get("rate",1.2)); y0=float(cfg.get("initial",1.0)); exact=y0*math.exp(-rate*duration); rows=[]
    for dt in [float(x) for x in cfg.get("time_steps",[0.5,0.2,0.1,0.05])]:
        for method in ("euler","rk4"):
            value=integrate(method,dt,duration,rate,y0); error=abs(value-exact) if math.isfinite(value) else float("inf"); rows.append({"method":method,"dt":dt,"value":value,"absolute_error":error,"finite":math.isfinite(value)})
    limit=float(cfg.get("max_rk4_error",0.001)); rk4=[r for r in rows if r["method"]=="rk4"]; passed=all(r["finite"] for r in rows) and min(r["absolute_error"] for r in rk4)<=limit
    return {"exact_terminal":exact,"cases":rows,"passed":passed,"best_rk4_error":min(r["absolute_error"] for r in rk4)}
