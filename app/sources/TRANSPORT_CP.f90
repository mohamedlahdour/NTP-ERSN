!BL1
    subroutine fmm_id(nfmesh,RegMat,fmmid,nregion,totNFM)
       implicit none
       integer(kind=4), intent(in) :: nregion,totNFM
       integer(kind=4), dimension(nregion), intent(in) :: RegMat,nfmesh
       integer(kind=4), dimension(totNFM), intent(out) :: fmmid 
       integer(kind=4) :: m,i,j  
       m = 1
       do i = 1,nregion
          do j=1,nfmesh(i)
             fmmid(m) = RegMat(i)
             m= m+1
          enddo
       enddo   
    end subroutine fmm_id
!BL2
    subroutine Matrix_matrix_I(matrix_I,dim)
       implicit none
       integer(kind=4), intent(in) :: dim
       real(kind=8), dimension(dim,dim), intent(out) :: matrix_I 
       integer(kind=4) :: i,j
       do j = 1,dim
          do i = 1,dim
             if (i == j) then
             matrix_I(i,j) = 1.0D0
             else
             matrix_I(i,j) = 0.0D0
             endif
          enddo   
       enddo 
    end subroutine Matrix_matrix_I
!BL3
    function    en(n,xx) 
!      Exponential integrals E1 through E4
!      Range    -- all positive arguments.
!      Accuracy -- absolute accuracy E-06 to E-07.
!      Method   -- for E1 two chebyshev expansions are used, one below 
!                  and the other above 4.
!                  for E2 through E4 the following recurrence relation is used:
!                  EN(X) = (EN(-X)-X*E(N-1)(X))/(N-1)
       implicit none
       real(kind=8), intent(in) :: xx
       integer(kind=4), intent(in) :: n
       real(kind=8) :: t,f,r,s,ex
       real(kind=8) :: en
       real(kind=8) :: x
       integer(kind=4) :: i
       real(kind=8), dimension(6) :: A
       real(kind=8), dimension(4) :: B
       real(kind=8), dimension(4) :: C
       data  A / -0.5772156649,0.99991930,-0.24991055,0.05519968,&
                 -0.0097600400,0.00107857/
       data  B /  8.5733287401,18.0590169730,8.63476082500,0.2677737343/
       data  C /  9.5733223400,25.6329561486,21.0996530827,3.9584969228/
       x = abs(xx) + 1.0E-20
       if ( n < 1 ) then
       write (*,'(a)') 'error (n in function EN(n,x) must be >= 0)'
       elseif ( x < -1.0E-10 ) then
       write (*,'(a)') 'error (x in function EN(n,x) must be >= 0)'
       elseif ( x <= 0 ) then
           if ( n <= 1 ) then
           en = 1.E20
           else
           en = 1/(n-1)
           endif
       else
       ex=exp(-x)
           if ( n == 0 ) then
           en = ex/x
           else
              if ( x <= 1 ) then
              t  = a(1)+x*(a(2)+x*(a(3)+x*(a(4)+x*(a(5)+x*a(6)))))
              f  = t-log(x)
              en = f
              else
              r  = b(4)+x*(b(3)+x*(b(2)+x*(b(1)+x)))
              s  = c(4)+x*(c(3)+x*(c(2)+x*(c(1)+x)))
              f  = r/s*ex/x
              en  = f
              endif
              do  i=1,n-1
              f =(ex-x*f)/i
              end do
              en = f
           endif
       endif
    end function en
!BL4   
    function fii(signe,taux,SigTi,li)
       implicit none
       real(kind=8), intent(in) :: signe
       real(kind=8), intent(in) :: SigTi, li, taux
       real(kind=8) :: fii,a0,a1,a2,a3,EN
       if     ( SigTi /= 0) then
       a0   = 1/(li*SigTi*SigTi) 
       a1   = EN(2,taux)   
       a2   = EN(3,taux) 
       a3   = EN(3,taux +signe*SigTi*li) 
       fii  = (signe*a1)/SigTi-a0*(a2-a3)
       else
       fii  = 0.5*li*EN(1,taux)
       end if
    end function fii
!BL5
    function fij(signe,taux,li,lj,SigTi,SigTj)
       implicit none
       real(kind=8), intent(in) :: signe
       real(kind=8), intent(in) :: li,lj,SigTi,SigTj,taux
       real(kind=8) :: fij,a0,a1,a2,a3,a4,EN
       if     ( SigTi /= 0 .and. SigTj /= 0 ) then
       a0   = 1/(li*SigTi*SigTj)
       a1   = EN(3,taux)
       a2   = EN(3,taux+signe*li*SigTi)
       a3   = EN(3,taux+signe*lj*SigTj)
       a4   = EN(3,taux+signe*li*SigTi+signe*lj*SigTj)
       fij  = 0.5*a0*(a1-a2-a3+a4)
       elseif ( SigTi == 0 .and. SigTj /= 0 ) then
       a0   = 1/SigTj
       a1   = EN(2,taux)
       a2   = EN(2,taux+signe*lj*SigTj)
       fij  = signe*0.5*li*a0*(a1-a2)
       elseif ( SigTi /= 0 .and. SigTj == 0 ) then
       a0   = 1/SigTi
       a1   = EN(2,taux)
       a2   = EN(2,taux+signe*li*SigTi)
       fij  = signe*0.5*lj*a0*(a1-a2)
       else
       fij  = 0.5*li*lj*EN(1,taux)
       end if
    end function fij
!BL6
    subroutine Transport_Corr(SigSS,SigTT,SigS,SigT,ng,Nmat,order)
       implicit none
       integer(kind=4), intent(in) :: ng,Nmat,order
       real(kind=8), dimension(Nmat,order,ng,ng), intent(in) :: SigSS
       real(kind=8), dimension(Nmat,ng), intent(in) :: SigTT
       real(kind=8), dimension(Nmat,ng,ng), intent(out) :: SigS
       real(kind=8), dimension(Nmat,ng), intent(out) :: SigT
       integer(kind=4) :: i,j
       if (order==1) then
          SigT = SigTT
          SigS(:,:,:) = SigSS(:,1,:,:)
       else
          do i = 1,Nmat
             do  j = 1,ng
             SigT(i,j) = SigTT(i,j) - SigSS(i,2,j,j)
             SigS(i,j,j) = SigSS(i,1,j,j) - SigSS(i,2,j,j)
             enddo
          enddo
       endif
    end subroutine Transport_Corr
!BL7
    subroutine  Pij_f(vol,albedo,SigT,fmmid,pij,ng,dim,totNFM,Nmat)
       integer(kind=4), intent(in) :: ng,dim,totNFM,Nmat
       integer(kind=4), dimension(totNFM), intent(in) :: fmmid 
       real(kind=8), dimension(dim,dim), intent(out) :: Pij
       real(kind=8), dimension(totNFM), intent(in) :: vol
       real(kind=8), dimension(Nmat,ng), intent(in) :: SigT
       real(kind=8), dimension(2), intent(in) :: albedo

       real(kind=8), dimension(dim) :: sig,vo
       real(kind=8), dimension(dim,dim) :: test,pij1
       real(kind=8) :: a0,a1,taucell,tau0,fii,fij
       integer(kind=4) :: ri,rj,k,k0=1,k1,K2,i,j
       pij  = 0.0D0
       pij1 = 0.0D0
       i = 1
       do k1=1,ng
       do K2=1,totNFM
       sig(i) = SigT(fmmid(k2),k1)
       vo(i)  = vol(k2)
       i = i + 1
       enddo
       enddo

       if  ( albedo(1) == 0.0D0 .and. albedo(2) == 0.0D0 ) then
           do k = 1, ng
              do  ri = k0,totNFM*k
                  pij(ri,ri) = fii(1.0D0,0.0D0,sig(ri),vo(ri))
                  tau0 = 0.0
                  do  rj = ri+1,totNFM*k
                      pij(ri,rj) = fij(1.0D0,tau0,vo(ri),vo(rj),sig(ri),sig(rj))
                      tau0 = tau0 + vo(rj)*sig(rj)
                  enddo
              enddo
              k0 = totNFM+k0
           enddo

       elseif ( albedo(1) == 1.0D0 .and. albedo(2) == 1.0D0 ) then
           k0 = 1
       do  k = 1,ng
           m = - 1
           taucell = DOT_PRODUCT(SigT(fmmid(:),k),vol) 
           test = 1.1
           do while ( maxval(test(:,:)) >= 1.0E-10 ) 
                    m   = m + 1 
                        tau0 = 0.0
                    do  ri = k0,totNFM*k
                        a0 = albedo(1)**(m)*fii(1.0D0,m*taucell,sig(ri),vo(ri))
                        a1 = albedo(2)**(m+1)*fii(-1.0D0,(m+1)*taucell,sig(ri),vo(ri))
                        pij1(ri,ri) = pij1(ri,ri) + a0 + a1
                        tau0 = 0.0
                        do  rj = ri+1,totNFM*k
                        a0 = albedo(1)**(m)*fij(1.0D0,(m*taucell+tau0),vo(ri),vo(rj),sig(ri),sig(rj))
                        a1 = albedo(2)**(m+1)*fij(-1.0D0,((m+1)*taucell-tau0),vo(ri),vo(rj),sig(ri),sig(rj))
                            pij1(ri,rj) = pij1(ri,rj) + a0 + a1
                            tau0 = tau0 + vo(rj)*sig(rj) 
                        enddo
                    enddo
           pij  = pij + pij1 
           test = pij1
           pij1 = 0.
           enddo
       k0 = totNFM+k0
       enddo
       else
       print*, "This limit condition is not available"
       stop
       endif
       k0=1
       do k = 1,ng
       do i = k0,totNFM*k
          do j = i,totNFM*k  
             Pij(j,i) = (vo(i)/vo(j))*Pij(i,j)
          end do
       end do 
       k0 = totNFM  + k0
       enddo
    end subroutine Pij_f
!BL8
    subroutine flux_guess(NusigF,vol,fmmid,phi_guess,dim,ng,totNFM,Nmat)
       implicit none
       integer(kind=4), intent(in) :: ng,totNFM,Nmat,dim
       integer(kind=4), dimension(totNFM), intent(in) :: fmmid 
       real(kind=8), dimension(Nmat,ng), intent(in) :: NusigF
       real(kind=8), dimension(totNFM), intent(in) :: vol
       real(kind=8), dimension(dim), intent(out) :: phi_guess
       real(kind=8), dimension(dim) :: a10,a11
       real(kind=8) :: kguess
       integer(kind=4) :: i,m,n
       kguess = 1.0
       i = 1
       do m=1,ng
          do n=1,totNFM
          a10(i) = NusigF(fmmid(n),m)
          a11(i) = vol(n)
          i = i + 1
          enddo
       enddo 
       phi_guess  = kguess/dot_product(a10,a11)
    end subroutine flux_guess
!BL9
    subroutine Matrix_D(SigS,fmmid,D,ng,totNFM,Nmat,dim)
       implicit none
       integer(kind=4), intent(in) :: ng,totNFM,Nmat,dim
       integer(kind=4), dimension(totNFM), intent(in) :: fmmid 
       real(kind=8), dimension(Nmat,ng,ng), intent(in) :: SigS
       real(kind=8), dimension(dim,dim), intent(out) :: D
       integer(kind=4) :: k0,k,i,j
            k0 = 1
            do   k   = 1, ng
                 j   = 1
                 do  i  = k0,totNFM*k
                     D(i,i) = SigS(fmmid(j),k,k)
                     j = j + 1
                 end do
            k0 = totNFM + k0
            enddo
    end subroutine Matrix_D
!BL10
    subroutine Matrix_C(matrix_I,D,pij,C,dim)
       implicit none
       integer(kind=4), intent(in) :: dim
       real(kind=8), dimension(dim,dim), intent(in) :: matrix_I,D,pij
       real(kind=8), dimension(dim,dim), intent(out) :: C
       C(:,:) = matrix_I(:,:) - matmul(D,pij)
    end subroutine Matrix_C 
!BL11
    subroutine matinv(a,ainv,n)
       implicit none
       integer(kind=4), intent(in) :: n
       real(kind=8), dimension(n,n), intent(in) :: a
       real(kind=8), dimension(n,n), intent(out) :: ainv
       real(kind=8), dimension(n,2*n) :: b
       integer(kind=4) :: i,j,k
       real(kind=8) :: pivot=0.0D0,xnum
!      make augmented matrix 
       do i=1,n 
       do j=1,n 
       b(i,j)=0.0
       b(i,j+n)=0.0
       b(i,j)=a(i,j)
       if(i.eq.j) then 
       b(i,j+n)=1.0
       end if  
       end do
       end do 
       do i=1,n
!      choose the leftmost non-zero element as pivot 
       do j=1,n
       if (abs(b(i,j)).gt. 0.0) then
       pivot=b(i,j)
       exit 
       end if
       end do 
!      step 1: change the chosen pivot into "1" by dividing 
!      the pivot's row by the pivot number 
       do j=1,2*n
       b(i,j)=b(i,j)/pivot
       end do
       pivot=b(i,i)  !update pivot value 
!      step 2: change the remainder of the pivot's column into 0's
!      by adding to each row a suitable     multiple of the pivot row 
       do k=1,n !row 
       if(k.ne.i) then
       xnum=b(k,i)/pivot   !same column with the current pivot
       do j=1,2*n !col 
       b(k,j)=b(k,j)-xnum*b(i,j) 
       end do 
       end if 
       end do 
       end do 
!      prepare the final inverted matrix 
       do i=1,n 
       do j=1,n 
       ainv(i,j)=b(i,j+n) 
       end do 
       end do 
       return
    end subroutine matinv 
!BL12
    subroutine Matrix_W(ainv,pij,W,dim)
       implicit none
       integer(kind=4), intent(in) :: dim
       real(kind=8), dimension(dim,dim), intent(in) :: ainv,pij
       real(kind=8), dimension(dim,dim), intent(out) :: W
       W(:,:) = matmul(pij,ainv)
    end subroutine Matrix_W
!BL13
    subroutine Matrix_L(SigS,fmmid,L,ng,totNFM,Nmat,dim)
       implicit none
       integer(kind=4), intent(in) :: ng,totNFM,Nmat,dim
       integer(kind=4), dimension(totNFM), intent(in) :: fmmid 
       real(kind=8), dimension(Nmat,ng,ng), intent(in) :: SigS
       real(kind=8), dimension(dim,dim), intent(out) :: L
       integer(kind=4) :: i,k0,k1,k2,k3
                   L(:,:) = 0.0
                k2  = 0
            do  k1  = 1,ng
                k0  = 1
                k3  = 0
                    do while (k0<k1) 
                             do  i  = 1,totNFM
                             L(i+k3,i+(k1-1)*totNFM) = SigS(fmmid(i),k0,k1) ! 1 --> 2 SigS(1,1,2)
                             enddo
                             k0 = k0 + 1
                             k3 = k3 + totNFM
                    enddo
            enddo
    end subroutine 
!BL14    
    subroutine Matrix_U(SigS,fmmid,U,ng,totNFM,Nmat,dim)
       implicit none
       integer(kind=4), intent(in) :: ng,totNFM,Nmat,dim
       integer(kind=4), dimension(totNFM), intent(in) :: fmmid 
       real(kind=8), dimension(Nmat,ng,ng), intent(in) :: SigS
       real(kind=8), dimension(dim,dim), intent(out) :: U
       integer(kind=4) :: i,k0,k1,k2,k3
                U(:,:) = 0.0
                k2  = 0
            do  k1  = 1,ng
                k0  = 1
                k3  = 0
                    do while (k0<k1) 
                             do  i  = 1,totNFM
                             U(i+(k1-1)*totNFM,i+k3) = SigS(fmmid(i),k1,k0) ! 1 --> 2 SigS(1,1,2)
                             enddo
                             k0 = k0 + 1
                             k3 = k3 + totNFM
                    enddo
            enddo
    end subroutine Matrix_U
!BL15
    subroutine Matrix_F(NusigF,CHI,fmmid,F,ng,totNFM,Nmat,dim)
       implicit none
       integer(kind=4), intent(in) :: ng,totNFM,Nmat,dim
       integer(kind=4), dimension(totNFM), intent(in) :: fmmid 
       real(kind=8), dimension(Nmat,ng), intent(in) :: NusigF,CHI
       real(kind=8), dimension(dim,dim), intent(out) :: F
       integer(kind=4) :: i,j,k0,k1,k2,k3,k
            F(:,:) = 0.0
            k0 = 1
            do   k   = 1, ng
                 j   = 1
                 do  i  = k0,totNFM*k
                     F(i,i) = CHI(fmmid(j),k)*NusigF(fmmid(j),k)
                     j = j + 1
                 end do
            k0 = totNFM + k0
            enddo
              
            k2  = 0
            do  k1  = 1,ng
                k0  = 1
                k3  = 0
                    do while (k0<k1) 
                             do  i  = 1,totNFM
                             F(i+k3,i+(k1-1)*totNFM) =  CHI(fmmid(i),k1)*NusigF(fmmid(i),k0)
                             F(i+(k1-1)*totNFM,i+k3) =  CHI(fmmid(i),k0)*NusigF(fmmid(i),k1)
                             enddo
                             k0 = k0 + 1
                             k3 = k3 + totNFM
                    enddo
            enddo
    end subroutine Matrix_F
!BL16
    subroutine Matrix_AB(matrix_I,L,W,U,F,A,B,dim)
       implicit none
       integer(kind=4), intent(in) :: dim
       real(kind=8), dimension(dim,dim), intent(in) :: matrix_I,L,W,U,F
       real(kind=8), dimension(dim,dim), intent(out) :: A,B
       A(:,:)   = matrix_I(:,:) - matmul(W,L) - matmul(W,U)
       B(:,:)   = matmul(W,F)
    end subroutine Matrix_AB
!BL17
    subroutine aleig(a,b,eps,iter,eval,phi,phi_guess,ng,totNFM,Max_it,dim)
!      -------------------  The inverse power method  -------------------
!                           (A - 1/Keff*B)*phi = 0
! 
!      ------------------------------------------------------------------
       implicit none
       integer(kind=4), intent(in) :: ng,totNFM,Max_it,dim
       real(kind=8), intent(in) :: eps
       real(kind=8), dimension(dim,dim), intent(in) :: a,b
       real(kind=8), dimension(dim), intent(in) :: phi_guess
       real(kind=8), dimension(dim), intent(out) :: phi
       real(kind=8), intent(out) :: eval
       integer(kind=4), intent(out) :: iter
       real(kind=8), dimension(dim,dim) :: ai,ainv
       real(kind=8), dimension(dim) :: gar,vec1,vec2
       real(kind=8), dimension(dim) :: phi1,phi2
       real(kind=8), dimension(ng) :: moy
       real(kind=8) :: s1,s2,err1,err2,test,eval1,eval2,epsil1=1.0,epsil2=1.0
       integer(kind=4) :: i,k0,k1
       call matinv(a,ainv,dim)
       ai = matmul(ainv,b)
       iter = 0
       phi1 = phi_guess
       eval1 = 0.0
       do while ( epsil1 >= eps .and. epsil2 >= eps )       
           iter = iter + 1
           if ( iter > Max_it ) then
           print*, 'error(unable to converge(1))'
           stop
           end if
           gar    = matmul(ai,phi1)
           vec1   = matmul(a,phi1)
           vec2   = matmul(b,phi1)
           s1     = dot_product(vec1,vec2)
           s2     = dot_product(vec2,vec2)
           eval2  = s1/s2
!          critere de convergence sur les valeurs porpres               
           epsil1 =  abs(eval2-eval1)/eval2
           eval1  = eval2 
           phi2   = gar*eval1         
           err1   = maxval(abs(phi2))
           err2   = maxval(abs(phi2-phi1))
!          critere de convergence sur les vecteurs porpres   
           epsil2 = err2/err1       
           phi1   = phi2      
           if (iter == 1)  then
                   test = epsil1
           elseif (iter >= 10 .and. epsil1 > test) then
           print*, 'error(unable to converge(2) )'
           print*, 'because error in iteration ten is sup to one'
           end if
           phi = phi1
           eval = eval1
           write(*,'(t3,"Iteration",i4,":",5x,"===>",5x,"keff =",F9.6,5x,"===>",5x,"res =",e10.3)')iter,1/eval,epsil1
       end do

       moy = 0.0
       k1 = 1
       do k0 = 1,ng
          do i=k1,totNFM*k0
             moy(k0) = moy(k0) + phi(i)
          end do
          do i=k1,totNFM*k0
             phi(i) = phi(i)/(moy(k0)/totNFM)
          end do
          k1 = k1 + totNFM 
       enddo

    end subroutine aleig
!BL18
    subroutine vol_ray(entree,nfmesh,rayon,ray,vol,nregion,totNFM)
        implicit none
        integer(kind=4), intent(in) :: totNFM,nregion
        integer(kind=4), dimension(nregion), intent(in) :: nfmesh
        real(kind=8), dimension(nregion), intent(in) :: rayon
        real(kind=8), dimension(totNFM), intent(out) :: ray,vol
        integer(kind=4) :: k1,k2=0,i
        real(kind=8) :: x1,x2,som,PI,cte = 4.0/3.0
        logical entree
        data PI     /3.1415927/
        
        do  k1 = 1,nregion
           do   i = 1,nfmesh(k1)
                x1 = i
                x2 = nfmesh(k1)
                ray(k2+i) = sqrt(x1/x2)*rayon(k1)
           enddo
           som = 0.d0
        do   i = 1,nfmesh(k1)
             if (entree .eqv. .true.) then
             vol(k2+i) = cte*PI*(ray(k2+i)**3-som)
             som = ray(i+k2)**3
             else
             vol(k2+i) = PI*(ray(k2+i)**2-som)
             som = ray(i+k2)**2
             endif
        enddo
        k2 = k2 + nfmesh(k1)
        enddo
    end subroutine vol_ray
!BL19
subroutine Output(start,albedo,tm,k_eff,SigT,NusigF,SigS,Chi,dcell,phi,eps,totNFM,dim,&
                  ng,Nmat,order,nregion,it)
        implicit none
        integer(kind=4), intent(in) :: ng,dim,totNFM,Nmat,order,nregion,it
        real(kind=8), dimension(Nmat,ng), intent(in) :: SigT,NusigF,Chi
        real(kind=8), dimension(Nmat,ng,ng), intent(in) :: SigS
        real(kind=8), dimension(dim), intent(in) :: phi
        real(kind=8), dimension(nregion), intent(in) :: dcell
        real(kind=8), dimension(2), intent(in) :: albedo
        CHARACTER(50), intent(in) :: start,tm
        real(kind=8), intent(in) :: eps,k_eff
        integer(kind=4) :: i,j
        open (100,file='app/Output/OUTPUT_CP.TXT')
        write (100, FMT=* ) '********************************************************************************'
        write (100, FMT=* ) 'ERSN, UNIVERSITY ABDELMALEK ESSAADI FACULTY OF SCIENCES - TETOUAN, MOROCCO'
        write (100, FMT=* ) 'CODE  DEVELOPED  BY  MOHAMED  LAHDOUR,  PHD  STUDENT'
        write (100, FMT=* ) 'NTP-ERSN:        CP COLLISION PROBABILITY METHOD'
        write (100, FMT=* ) 'VERSION NUMBER:  1.1'
        write (100, FMT=* ) 'VERSION DATE:    8  OTOBER  2018'
        write (100,3010) 'RAN ON:          ', start,'(H:M:S)'
        write (100, FMT=* ) '********************************************************************************'
        write (100, FMT=* ) '           ----------------------------------------------------------' 
        write (100, FMT=* ) '                     INPUT  PARAMETER - VALUES  FROM  INPUT'              
        write (100, FMT=* ) '           ----------------------------------------------------------'
        write (100, FMT=* ) ''
        write (100, FMT=* ) 'ENERGY GROUP NUMBER:                     ',ng
        write (100, FMT=* ) 'REGIONS NUMBER:                          ',nregion
        write (100, FMT=* ) 'MATERIALS NUMBER:                        ',Nmat
        write (100,3040)    'SIZE FOR EACH MATERIAL PER [CM]:         ',dcell       
        write (100, FMT=* ) 'ORDER LEGENDRE POLONOMIAL:               ',order-1
        write (100, FMT=* ) 'TOTAL NUMBER OF FINE MESHES:             ',totNFM
        write (100,3050)    'CONVERGENCE CRITERION of KEFF AND FLUX:  ',eps
        write (100, FMT=* ) ''
        write (100, FMT=* ) '           ----------------------------------------------------------'
        write (100, FMT=* ) '                      CALCULATION  RUN-TIME  PARAMETERS  CP' 
        write (100, FMT=* ) '           ----------------------------------------------------------'
        write (100, FMT=* ) ''
        write (100, FMT=* ) 'PSEUDO  CROSS  SECTIONS  DATA: '
        write (100, FMT=* ) ''

        do i = 1,Nmat
        write (100, 3070) ' MATERIAL :', i  
        write (100, FMT=* ) ''
        write (100, FMT=* ) '        GROUP ','          TOTAL ','       ABSORPTION ',&
                            '     NU*FISSION ','     SCATTERING ','     FISSION SPECTRUM'
        write (100, FMT=* ) ''
            do j = 1,ng
            write(100,3080) j,SigT(i,j),SigT(i,j)-SigS(i,j,j),NusigF(i,j),SigS(i,j,j),Chi(i,j)
            enddo
        enddo
        write (100, FMT=* ) ''
        write (100, FMT=* ) '           ----------------------------------------------------------'
        write (100, FMT=* ) '                             SCALAR  FLUX  SOLUTION' 
        write (100, FMT=* ) '           ----------------------------------------------------------'
        write (100, FMT=* ) ''
        write (100, FMT=* ) 'FLUXES  PER  MESH  PER  ENERGY  GROUP:'  
        write (100, FMT=* ) '' 
        write (100,3000)'       M E S H ', ('     G R O U P',i,i=1,ng)
        write (100, FMT=* ) ''
        do i=1,totNFM
        write(100,2000) i,(phi(i+j), j=0,dim-1,totNFM)
        enddo
        write (100, FMT=* ) ''
        write (100, FMT=* ) '           ----------------------------------------------------------'
        write (100, FMT=* ) '             OUTPUT  PARAMETER - SOLUTION  TO  TRANSPORT  EQUATION' 
        write (100, FMT=* ) '           ----------------------------------------------------------'
        write (100, FMT=* ) ''
        if  ( albedo(1) == 1.0D0 .and. albedo(2) == 1.0D0 ) then
        write (100,3090)    'K-INF                    =',k_eff
        else
        write (100,3090)    'K-EFF                    =',k_eff
        endif
        write (100,3020)    'N. OUTER ITERATIONS      =',it
        write (100,4000)    'TOTAL EXECUTION TIME     =',tm,'(H:M:S)'
        write (100, FMT=* ) ''
        write (100, FMT=* ) '********************************************************************************'
        2000 format(1x,1p,i11,5x,200e16.5) 
        3000 format(1x,A14,2x,300(A14,i2))  
        3010 format(1x,A17,A22,A10)
        3020 format(1x,A26,4x,i10)
        3040 format(1x,A33,2x,200F10.5)
        3050 format(1x,1p,A41,4x,e8.1)
        3070 format(1x,A18,i4)
        3080 format(1x,1p,i11,5x,e16.5,e16.5,e16.5,e16.5,e16.5)
        3090 format(1x,A26,6x,f8.6)
        4000 format(1x,A26,4x,A10,A10)
        close(100)
end subroutine Output
!BL20
    subroutine plot_Sla(vol,phi,totNFM,dim)
        implicit none
        integer(kind=4), intent(in) :: dim,totNFM
        real(kind=8), dimension(dim), intent(in) :: phi
        real(kind=8), dimension(totNFM), intent(in) :: vol
        integer(kind=4) :: i,j
        real(kind=8) :: som
        open (11,file='app/Output/flux_cp.h')
        som = -sum(vol)*0.5
        do i=1,totNFM
        write(11,'(1F11.6,200F10.6)') som,(phi(i+j),j=0,dim-1,totNFM) 
        som = som + vol(i)
        enddo
        close(11)
    end subroutine plot_Sla
!BL21
    subroutine timestamp()
!      ------------------------------------------------------------------------
!      TIMESTAMP prints the current YMDHMS date as a time stamp.
!      Example:
!      31 May 2001   9:45:54.872 AM
!      Licensing:
!      This code is distributed under the GNU LGPL license.
!      Modified:
!      18 May 2013
!      Author:
!      John Burkardt
!      Parameters:
!      None
!      ------------------------------------------------------------------------
       implicit none

       character ( len = 8 ) ampm
       integer ( kind = 4 ) d
       integer ( kind = 4 ) h
       integer ( kind = 4 ) m
       integer ( kind = 4 ) mm
       character ( len = 9 ), parameter, dimension(12) :: month = (/ &
       'January  ', 'February ', 'March    ', 'April    ', &
       'May      ', 'June     ', 'July     ', 'August   ', &
       'September', 'October  ', 'November ', 'December ' /)
       integer ( kind = 4 ) n
       integer ( kind = 4 ) s
       integer ( kind = 4 ) values(8)
       integer ( kind = 4 ) y
       call date_and_time ( values = values )
       y = values(1)
       m = values(2)
       d = values(3)
       h = values(5)
       n = values(6)
       s = values(7)
       mm = values(8)
       if ( h < 12 ) then
       ampm = 'AM'
       else if ( h == 12 ) then
       if ( n == 0 .and. s == 0 ) then
       ampm = 'Noon'
       else
       ampm = 'PM'
       end if
       else
       h = h - 12
       if ( h < 12 ) then
       ampm = 'PM'
       else if ( h == 12 ) then
       if ( n == 0 .and. s == 0 ) then
       ampm = 'Midnight'
       else
       ampm = 'AM'
       end if
       end if
       end if
       write ( *, '(i6,1x,a,1x,i4,2x,i2,a1,i2.2,a1,i2.2,a1,i3.3,1x,a)' ) &
       d, trim ( month(m) ), y, h, ':', n, ':', s, '.', mm, trim ( ampm )
       return
    end subroutine timestamp
!BL22
    subroutine title1()         
       write(*,FMT='(/24(A/))') & 
       '      ███╗   ██╗████████╗██████╗&
       &       ███████╗██████╗ ███████╗███╗   ██╗',&
       '      ████╗  ██║╚══██╔══╝██╔══██╗      ██&
       &╔════╝██╔══██╗██╔════╝████╗  ██║',&
       '      ██╔██╗ ██║   ██║   ██████╔╝█████╗█████╗&
       &  ██████╔╝███████╗██╔██╗ ██   ',&
       '      ██║╚██╗██║   ██║   ██╔═══╝ ╚════╝██╔══╝&
       &  ██╔══██╗╚════██║██║╚██╗██║',&
       '      ██║ ╚████║   ██║   ██║           ███████╗██║&
       &  ██║███████║██║ ╚████║',&
       '      ╚═╝  ╚═══╝   ╚═╝   ╚═╝           ╚══════╝&
       &╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝',& 
       '______________________________________________________________________________'
       write(*,FMT=*) '                                                   Version Number: 1.1 '     
       write(*,FMT=*) '     Copyright:      2015-2018 FS-Tetouan University Abdelmalk Essaadi '
       write ( *, FMT=* ) '.'
       write ( *, FMT=* ) '   FORTRAN90 version' 
       write ( *, FMT=* ) '   The collision probability method'  
       write ( *, FMT=* ) '   Calculation of 1D collision probabilities'
       write ( *, FMT=* ) '   Slab 1D geometry' 
       write ( *, FMT=* ) '.'
    end subroutine title1
!BL23
    subroutine title2()
       write ( *, FMT=* )' ************************************************************************'
       write ( *, FMT=* )'                               Finished'                             
       write ( *, FMT=* )' ************************************************************************'  
    end subroutine title2


 
