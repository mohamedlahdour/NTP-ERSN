import app.SlabCP
import app.SlabSN
import app.SlabMOC
import numpy as np
import json
from datetime import datetime
import subprocess
import os
start=datetime.now()
sigtt = []
sigss = []
sigt = []
nusigf = []
sigf = []
sigs = []
chi = []
vol = []
regmat  = []
nfmesh  = []
width   = []
assembly  = []
core      = []
PATH = open(os.getcwd()+'/app/link/script.dir', "r" ).read()
Method = open(os.getcwd()+ '/app/link/script00.py', "r" ).read()
BC = open(os.getcwd()+ '/app/link/script08.py', "r" ).read()
scheme1 = open(os.getcwd() +'/app/link/script09.py', "r" ).read()
scheme2 = open(os.getcwd() +'/app/link/script10.py', "r" ).read()
Geometry_type = open(os.getcwd()+'/app/link/script07.py', "r" ).read()
 #==========================================================================================
 #  Write data for Method MOC
 # ========================================================================================= 
if int(Method) == 3:
    with open(PATH) as json_data:
        data = json.load(json_data)
        ng = data['data']['parameter']['Total number of energy groups']  
        nmat = data['data']['parameter']['Total number of materials'] 
        npc = data['data']['parameter']['Total number of pin cells']
        na = data['data']['parameter']['Total number of assemblies']  
        apc = data['data']['parameter']['Total number of active pin cells'] 
        napc = data['data']['parameter']['Total number of active pin cells']
        core = data['data']['parameter']['Core']
        if "Boundary conditions" in data['data']['parameter']:
            BC   = data['data']['parameter']['Boundary conditions']
        else:
            pass
        nx = len(core)
        for j in range(na):
            assembly.append(data['data']['Assemblies'][j]['assembly'])
        nxx = len(assembly[0])
        for j in range(npc):
            width.append(data['data']['PinCells'][j]['width'])
            regmat.append(data['data']['PinCells'][j]['mat_fill'])
            nfmesh.append(data['data']['PinCells'][j]['fine_mesh'])
        ngauss = data['data']['parameter']['Number of angular discretizations']
        Max_it = data['data']['parameter']['Maximum number of iterations']
        order =  data['data']['parameter']['The l-order Legendre polynomial']
        order = order + 1
        eps = data['data']['parameter']['Criterion of Keff convergence']
        for i in range(nmat):
            sigt.append(data['data']['materials'][i]['XSTotal'])
            nusigf.append(data['data']['materials'][i]['XSNuFission'])
            if "XSFission" in data['data']['materials'][i]:
                sigf.append(data['data']['materials'][i]['XSFission'])
            else:
                sigf.append(data['data']['materials'][i]['XSNuFission'])
            sigs.append(data['data']['materials'][i]['XSScatter Matrix'])
            chi.append(data['data']['materials'][i]['XSChi'])
        npx = len(width[0])
        totnfm = sum(nfmesh[0])*nx*nxx
        fmmid,delta = app.SlabMOC.fmm_id(assembly,core,nfmesh,width,regmat,totnfm,[npx,npc,nx,nxx,na])
        dim = ng*totnfm 
        mu,wt = app.SlabMOC.gauleg(-1.,1.,ngauss)
        p = app.SlabMOC.leg_poly(order,mu,[ngauss]) 
        d = app.SlabMOC.matrix_d(sigs,fmmid,dim,[ng,nmat,order,totnfm])
        l = app.SlabMOC.matrix_l(sigs,fmmid,dim,[ng,nmat,order,totnfm])
        u = app.SlabMOC.matrix_u(sigs,fmmid,dim,[ng,nmat,order,totnfm])
        f = app.SlabMOC.matrix_f(nusigf,chi,fmmid,dim,[ng,nmat,totnfm])
        flux_ni,flux_li = app.SlabMOC.flux_guess(dim,fmmid,nusigf,delta,p,[ng,nmat,ngauss,order,totnfm])      
        app.SlabMOC.title1()
        #print fmmid
        app.SlabMOC.timestamp()
        it,inter,k_eff,phi = app.SlabMOC.outer_iteration(Max_it,eps,wt,mu,d,f,u,l,p,BC,scheme2,fmmid,sigt,
                             flux_ni,flux_li,delta,[ng,dim,totnfm,ngauss,order,nmat])
        app.SlabMOC.plot_flux(napc,delta,assembly,nfmesh,phi,fmmid,core,sigf,[dim,totnfm,nmat,ng,nx,nxx,npx,npc,na])
        sfpc = app.SlabMOC.scalarfluxpinc(nmat,ng,nfmesh,delta,assembly,phi,core,[dim,totnfm,nx,nxx,npx,npc,na])
        interval = datetime.now()-start 
        app.SlabMOC.output(str(start),BC,str(interval),k_eff,sigt,nusigf,sigs,chi,mu,wt,delta,
                                       phi,eps,it,inter,[totnfm,dim,ng,nmat,order,ngauss])
        print '  Total time to solution      ........................     ', interval  
        app.SlabMOC.title2()
        del sigt,sigs,nusigf,chi,mu,wt,fmmid,nfmesh 
         
 #==========================================================================================
 #  Write data for Method SN
 # ========================================================================================= 
elif int(Method) == 2:
    with open(PATH) as json_data:
        data = json.load(json_data)
        ng = data['data']['parameter']['Total number of energy groups']  
        nmat = data['data']['parameter']['Total number of materials'] 
        npc = data['data']['parameter']['Total number of pin cells']
        na = data['data']['parameter']['Total number of assemblies']   
        napc = data['data']['parameter']['Total number of active pin cells']
        core = data['data']['parameter']['Core']
        if "Boundary conditions" in data['data']['parameter']:
            BC   = data['data']['parameter']['Boundary conditions']
        else:
            pass
        nx = len(core)
        for j in range(na):
            assembly.append(data['data']['Assemblies'][j]['assembly'])
        nxx = len(assembly[0])
        for j in range(npc):
            width.append(data['data']['PinCells'][j]['width'])
            regmat.append(data['data']['PinCells'][j]['mat_fill'])
            nfmesh.append(data['data']['PinCells'][j]['fine_mesh'])
        ngauss = data['data']['parameter']['Number of angular discretizations']
        Max_it = data['data']['parameter']['Maximum number of iterations']
        order =  data['data']['parameter']['The l-order Legendre polynomial']
        order = order + 1
        eps = data['data']['parameter']['Criterion of Keff convergence']
        for i in range(nmat):
            sigt.append(data['data']['materials'][i]['XSTotal'])
            nusigf.append(data['data']['materials'][i]['XSNuFission'])
            if "XSFission" in data['data']['materials'][i]:
                sigf.append(data['data']['materials'][i]['XSFission'])
            else:
                sigf.append(data['data']['materials'][i]['XSNuFission'])
            sigs.append(data['data']['materials'][i]['XSScatter Matrix'])
            chi.append(data['data']['materials'][i]['XSChi'])
        npx = len(width[0])
        totnfm = sum(nfmesh[0])*nx*nxx
        fmmid,delta = app.SlabSN.fmm_id(assembly,core,nfmesh,width,regmat,totnfm,[npx,npc,nx,nxx,na])
        dim = ng*totnfm 
        mu,wt = app.SlabSN.gauleg(-1.,1.,ngauss)
        p = app.SlabSN.leg_poly(order,mu,[ngauss]) 
        d = app.SlabSN.matrix_d(sigs,fmmid,dim,[ng,nmat,order,totnfm])
        l = app.SlabSN.matrix_l(sigs,fmmid,dim,[ng,nmat,order,totnfm])
        u = app.SlabSN.matrix_u(sigs,fmmid,dim,[ng,nmat,order,totnfm])
        f = app.SlabSN.matrix_f(nusigf,chi,fmmid,dim,[ng,nmat,totnfm])
        a,b = app.SlabSN.matrix_ab(dim,mu,fmmid,sigt,delta,[ng,nmat,totnfm,ngauss])
        flux_ni,flux_li = app.SlabSN.flux_guess(dim,fmmid,nusigf,delta,p,[ng,nmat,ngauss,order,totnfm])
        app.SlabSN.title1()
        app.SlabSN.timestamp()
        it,inter,k_eff,phi = app.SlabSN.outer_iteration(Max_it,scheme1,eps,wt,mu,d,f,u,l,a,b,p,BC,sigt,
                             flux_ni,flux_li,delta,nusigf,chi,fmmid,[ng,dim,totnfm,ngauss,order,nmat])
        sfpc,sf = app.SlabSN.scalarfluxpinc(nfmesh,delta,assembly,phi,sigf,fmmid,core,[dim,totnfm,nmat,ng,nx,nxx,npx,npc,na])
        app.SlabSN.plot_flux(nmat,nx,nxx,napc,delta,phi,sfpc,sf,[dim,totnfm,ng])
        interval = datetime.now()-start
        app.SlabSN.output(str(start),BC,str(interval),k_eff,sigt,nusigf,sigs,chi,mu,wt,delta,
                     phi,eps,it,inter,[totnfm,dim,ng,nmat,order,ngauss])

        print '  Total time to solution      ........................     ', interval  
        app.SlabSN.title2()
        del sigt,sigs,nusigf,chi,mu,wt,fmmid,nfmesh

 #=========================================================================================
 #  Write data for Method CP 
 # =========================================================================================   
elif int(Method) == 1:
    with open(PATH) as json_data:
        data = json.load(json_data)
        ng = data['data']['parameter']['Total number of energy groups']  
        nmat = data['data']['parameter']['Total number of materials'] 
        npc = data['data']['parameter']['Total number of pin cells']
        na = data['data']['parameter']['Total number of assemblies']   
        napc = data['data']['parameter']['Total number of active pin cells']
        core = data['data']['parameter']['Core']
        if "Boundary conditions" in data['data']['parameter']:
            BC   = data['data']['parameter']['Boundary conditions']
        else:
            pass
        nx = len(core)
        for j in range(na):
            assembly.append(data['data']['Assemblies'][j]['assembly'])
        nxx = len(assembly[0])
        for j in range(npc):
            width.append(data['data']['PinCells'][j]['width'])
            regmat.append(data['data']['PinCells'][j]['mat_fill'])
            nfmesh.append(data['data']['PinCells'][j]['fine_mesh'])
        ngauss = data['data']['parameter']['Number of angular discretizations']
        Max_it = data['data']['parameter']['Maximum number of iterations']
        order =  data['data']['parameter']['The l-order Legendre polynomial']
        order = order + 1
        eps = data['data']['parameter']['Criterion of Keff convergence']
        for i in range(nmat):
            sigtt.append(data['data']['materials'][i]['XSTotal'])
            nusigf.append(data['data']['materials'][i]['XSNuFission'])
            if "XSFission" in data['data']['materials'][i]:
                sigf.append(data['data']['materials'][i]['XSFission'])
            else:
                sigf.append(data['data']['materials'][i]['XSNuFission'])
            sigss.append(data['data']['materials'][i]['XSScatter Matrix'])
            chi.append(data['data']['materials'][i]['XSChi'])
        npx = len(width[0])
        totnfm = sum(nfmesh[0])*nx*nxx
        app.SlabCP.title1()
        fmmid,delta = app.SlabSN.fmm_id(assembly,core,nfmesh,width,regmat,totnfm,[npx,npc,nx,nxx,na])
        dim = ng*totnfm 
        if BC in ["vacuum"]:
            albedo = [0,0]
        elif BC in ["reflective"]:
            albedo = [1,1]
        elif BC in ["vacuum_reflective"]:
            albedo = [0,1]
        elif BC in ["reflective_vacuum"]:
            albedo = [1,0]
        matrix_i = app.SlabCP.matrix_matrix_i(dim) 
        sigs,sigt = app.SlabCP.transport_corr(sigss,sigtt,[ng,nmat,order])
        pij = app.SlabCP.pij_f(delta,albedo,sigt,fmmid,dim,[ng,totnfm,nmat])
        phi_guess = app.SlabCP.flux_guess(nusigf,delta,fmmid,[dim,ng,totnfm,nmat])
        d = app.SlabCP.matrix_d(sigs,fmmid,dim,[ng,totnfm,nmat])
        c = app.SlabCP.matrix_c(matrix_i,d,pij,[dim])
        ainv = app.SlabCP.matinv(c,[dim])
        w = app.SlabCP.matrix_w(ainv,pij,[dim])
        l = app.SlabCP.matrix_l(sigs,fmmid,dim,[ng,totnfm,nmat])
        u = app.SlabCP.matrix_u(sigs,fmmid,dim,[ng,totnfm,nmat])
        f = app.SlabCP.matrix_f(nusigf,chi,fmmid,dim,[ng,totnfm,nmat])
        a,b = app.SlabCP.matrix_ab(matrix_i,l,w,u,f,[dim])
        app.SlabCP.timestamp()
        iter,eval,phi = app.SlabCP.aleig(a,b,eps,phi_guess,ng,totnfm,Max_it,[dim])
        app.SlabCP.plot_flux(napc,delta,assembly,nfmesh,phi,fmmid,core,sigf,[dim,totnfm,nmat,ng,nx,nxx,npx,npc,na])
        sfpc = app.SlabCP.scalarfluxpinc(nmat,ng,nfmesh,delta,assembly,phi,core,[dim,totnfm,nx,nxx,npx,npc,na])
        interval = datetime.now()-start  
        print '  Total time to solution      ........................     ', interval    
        app.SlabCP.title2()


        

