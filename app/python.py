import SlabCP
import SlabSN
import SlabMOC
import numpy as np
import json
from datetime import datetime
import subprocess
start=datetime.now()
sigtt = []
sigss = []
sigt = []
nusigf = []
sigs = []
chi = []
vol = []
filename = open('app/link/script.py', "r" ).read()
Pij_Method = open('app/link/script00.py', "r" ).read()
Sn_Method = open('app/link/script01.py', "r" ).read()
MOC_Method = open('app/link/script02.py', "r" ).read()
BC = open('app/link/script08.py', "r" ).read()
scheme1 = open('app/link/script09.py', "r" ).read()
scheme2 = open('app/link/script10.py', "r" ).read()
Geometry_type = open('app/link/script07.py', "r" ).read()
 #==========================================================================================
 #  Write data for Method MOC
 # ========================================================================================= 
if MOC_Method == str(1):
    with open(filename) as json_data:
        data = json.load(json_data)
        ng = data['data']['parameter']['Total number of energy groups']  
        nmat = data['data']['parameter']['Total number of Materials']
        nregion = data['data']['parameter']['Total number of regions'] 
        regmat = data['data']['parameter']['Which material fills each region']
        dcell = data['data']['parameter']['Size of each region [cm]']
        nfmesh = data['data']['parameter']['Number of fine meshes']
        ngauss = data['data']['parameter']['Number of Angular Discretization']
        order = data['data']['parameter']['The l-order Legendre polynomial']
        order = order + 1
        Max_it = data['data']['parameter']['Maximum Number of Iterations']
        eps = data['data']['parameter']['Criterion of Keff convergence']
        for i in range(nmat):
            sigt.append(data['data']['materials'][i]['XSTotal'])
            nusigf.append(data['data']['materials'][i]['XSNuFission'])
            sigs.append(data['data']['materials'][i]['XSScatter Matrix'])
            chi.append(data['data']['materials'][i]['XSChi'])
        totnfm = sum(nfmesh)
        dim = ng*totnfm 
        mu,wt = SlabMOC.gauleg(-1.,1.,ngauss)
        p = SlabMOC.leg_poly(order,mu,[ngauss]) 
        fmmid = SlabMOC.fmm_id(totnfm,nfmesh,regmat,[nregion])
        delta = SlabMOC.delta_f(totnfm,nfmesh,dcell,[nregion])
        d = SlabMOC.matrix_d(sigs,fmmid,dim,[ng,nmat,order,totnfm])
        l = SlabMOC.matrix_l(sigs,fmmid,dim,[ng,nmat,order,totnfm])
        u = SlabMOC.matrix_u(sigs,fmmid,dim,[ng,nmat,order,totnfm])
        f = SlabMOC.matrix_f(nusigf,chi,fmmid,dim,[ng,nmat,totnfm])
        flux_ni,flux_li = SlabMOC.flux_guess(dim,nregion,nusigf,dcell,p,
                                            [ng,nmat,ngauss,order,totnfm]) 
        del nfmesh            
        SlabMOC.title1()
        SlabMOC.timestamp()
        it,inter,k_eff,phi = SlabMOC.outer_iteration(Max_it,eps,wt,mu,d,f,u,l,p,BC,scheme2,fmmid,sigt,
                             flux_ni,flux_li,delta,[ng,dim,totnfm,ngauss,order,nmat])
        interval = datetime.now()-start  
        print '  Total time to solution      ........................     ', interval  
        SlabMOC.title2()
        SlabMOC.output(str(start),BC,str(interval),k_eff,sigt,nusigf,sigs,chi,mu,wt,
                       dcell,phi,eps,totnfm,it,inter,[dim,ng,nmat,order,nregion,ngauss])
        del sigt,sigs,nusigf,chi,mu,wt,fmmid
        SlabMOC.plot_flux(delta,phi,[totnfm,dim])  
 #==========================================================================================
 #  Write data for Method SN
 # ========================================================================================= 
elif Sn_Method == str(1):
    with open(filename) as json_data:
        data = json.load(json_data)
        ng = data['data']['parameter']['Total number of energy groups']  
        nmat = data['data']['parameter']['Total number of Materials']
        nregion = data['data']['parameter']['Total number of regions'] 
        regmat = data['data']['parameter']['Which material fills each region']
        dcell = data['data']['parameter']['Size of each region [cm]']
        nfmesh = data['data']['parameter']['Number of fine meshes']
        ngauss = data['data']['parameter']['Number of Angular Discretization']
        order = data['data']['parameter']['The l-order Legendre polynomial']
        order = order + 1
        Max_it = data['data']['parameter']['Maximum Number of Iterations']
        eps = data['data']['parameter']['Criterion of Keff convergence']
        for i in range(nmat):
            sigt.append(data['data']['materials'][i]['XSTotal'])
            nusigf.append(data['data']['materials'][i]['XSNuFission'])
            sigs.append(data['data']['materials'][i]['XSScatter Matrix'])
            chi.append(data['data']['materials'][i]['XSChi'])
        totnfm = sum(nfmesh)
        dim = ng*totnfm 
        mu,wt = SlabSN.gauleg(-1.,1.,ngauss)
        p = SlabSN.leg_poly(order,mu,[ngauss]) 
        fmmid = SlabSN.fmm_id(totnfm,nfmesh,regmat,[nregion])
        delta = SlabSN.delta_f(totnfm,nfmesh,dcell,[nregion])
        d = SlabSN.matrix_d(sigs,fmmid,dim,[ng,nmat,order,totnfm])
        l = SlabSN.matrix_l(sigs,fmmid,dim,[ng,nmat,order,totnfm])
        u = SlabSN.matrix_u(sigs,fmmid,dim,[ng,nmat,order,totnfm])
        f = SlabSN.matrix_f(nusigf,chi,fmmid,dim,[ng,nmat,totnfm])
        a,b = SlabSN.matrix_ab(dim,mu,fmmid,sigt,delta,[ng,nmat,totnfm,ngauss])
        flux_ni,flux_li = SlabSN.flux_guess(dim,nregion,nusigf,dcell,wt,p,
                                           [ng,nmat,ngauss,order,totnfm])
        del fmmid,nfmesh
        SlabSN.title1()
        SlabSN.timestamp()
        it,inter,k_eff,phi = SlabSN.outer_iteration(Max_it,scheme1,eps,wt,mu,d,f,u,l,a,b,p,BC,sigt,
                             flux_ni,flux_li,delta,[ng,dim,totnfm,ngauss,order,nmat])
        interval = datetime.now()-start  
        print '  Total time to solution      ........................     ', interval   
        SlabSN.title2()
        SlabSN.output(str(start),BC,str(interval),k_eff,sigt,nusigf,sigs,chi,mu,wt,
                      dcell,phi,eps,totnfm,it,inter,[dim,ng,nmat,order,nregion,ngauss])
        del sigt,sigs,nusigf,chi,mu,wt
        SlabSN.plot_flux(delta,phi,[totnfm,dim])
 #=========================================================================================
 #  Write data for Method CP 
 # =========================================================================================   
elif Pij_Method == str(1):
    with open(filename) as json_data:
        data = json.load(json_data)
        ng = data['data']['parameter']['Total number of energy groups']        
        nmat = data['data']['parameter']['Total number of Materials']
        nregion = data['data']['parameter']['Total number of regions'] 
        regmat = data['data']['parameter']['Which material fills each region']
        dcell = data['data']['parameter']['Size of each region [cm]']
        nfmesh = data['data']['parameter']['Number of fine meshes']
        Max_it = data['data']['parameter']['Maximum Number of Iterations']
        order =  data['data']['parameter']['The l-order Legendre polynomial']
        order = order + 1
        eps = data['data']['parameter']['Criterion of Keff convergence']
        totnfm = sum(nfmesh)
        for i in range(nmat):
            sigtt.append(data['data']['materials'][i]['XSTotal'])
            nusigf.append(data['data']['materials'][i]['XSNuFission'])
            sigss.append(data['data']['materials'][i]['XSScatter Matrix'])
            chi.append(data['data']['materials'][i]['XSChi'])
 
        if BC in ["vacuum"]:
            albedo = [0,0]
        elif BC in ["reflective"]:
            albedo = [1,1]
        elif BC in ["vacuum_reflective"]:
            albedo = [0,1]
        elif BC in ["reflective_vacuum"]:
            albedo = [1,0]      

        for i in range(nregion):
            for j in range(nfmesh[i]):
                vol.append(dcell[i]/nfmesh[i])

        dim = ng*totnfm
        fmmid = SlabCP.fmm_id(nfmesh,regmat,totnfm,[nregion])
        matrix_i = SlabCP.matrix_matrix_i(dim) 
        sigs,sigt = SlabCP.transport_corr(sigss,sigtt,[ng,nmat,order])    
        pij = SlabCP.pij_f(vol,albedo,sigt,fmmid,dim,[ng,totnfm,nmat])
        phi_guess = SlabCP.flux_guess(nusigf,vol,fmmid,[dim,ng,totnfm,nmat])
        d = SlabCP.matrix_d(sigs,fmmid,dim,[ng,totnfm,nmat])
        c = SlabCP.matrix_c(matrix_i,d,pij,[dim])
        ainv = SlabCP.matinv(c,[dim])
        w = SlabCP.matrix_w(ainv,pij,[dim])
        l = SlabCP.matrix_l(sigs,fmmid,dim,[ng,totnfm,nmat])
        u = SlabCP.matrix_u(sigs,fmmid,dim,[ng,totnfm,nmat])
        f = SlabCP.matrix_f(nusigf,chi,fmmid,dim,[ng,totnfm,nmat])
        a,b = SlabCP.matrix_ab(matrix_i,l,w,u,f,[dim])
        SlabCP.title1() 
        SlabCP.timestamp()
        iter,eval,phi = SlabCP.aleig(a,b,eps,phi_guess,ng,totnfm,Max_it,[dim])  
        interval = datetime.now()-start  
        print '  Total time to solution      ........................     ', interval    
        SlabCP.title2() 
        SlabCP.output(str(start),albedo,str(interval),1./eval,sigt,nusigf,sigs,chi,dcell,
                          phi,eps,totnfm,order,iter,[dim,ng,nmat,nregion])
        del sigt,nusigf,sigs,chi,dcell,fmmid,l,d,c,ainv,w,u,f
        SlabCP.plot_sla(vol,phi,[totnfm,dim])

        

