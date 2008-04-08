
import numpy as n
from math import degrees

def find_omega(Gw,costth):
	Glen = n.sqrt(n.dot(Gw,Gw))
	#theta = arcsin(Glen/(2*K))
	#costth = cos(2*theta)
	
	#    Trying to implement Soerens omega determination
	#    Solve equation of type a*cos(w)+b*sin(w) = c by fixpoint method.
	a =  Gw[0]/Glen
	b = -Gw[1]/Glen
	c = (costth-1)/n.sqrt(2*(1-costth))
  
	d=a**2+b**2
	sqD=d-c**2
  
	Omega = []
	if sqD > 0:
		sqD=n.sqrt(sqD)
		comega = (a*c + b*sqD)/d
		somega = (b*c - a*sqD)/d
		Omega.append(n.arccos(comega))
		if somega < 0:
			Omega[0] = -Omega[0]
		comega = comega - 2*b*sqD/d
		somega = somega + 2*a*sqD/d
		Omega.append(n.arccos(comega))
		if somega < 0:
			Omega[1] = -Omega[1]
	return Omega




def CellInvert(ucell):
        a = ucell[0]
        b = ucell[1]
        c = ucell[2]
        calp = n.cos(ucell[3]*n.pi/180.)
        cbet = n.cos(ucell[4]*n.pi/180.)
        cgam = n.cos(ucell[5]*n.pi/180.)
        salp = n.sin(ucell[3]*n.pi/180.)
        sbet = n.sin(ucell[4]*n.pi/180.)
        sgam = n.sin(ucell[5]*n.pi/180.)
	V = CellVolume(ucell)

	astar = b*c*salp/V
	bstar = a*c*sbet/V
	cstar = a*b*sgam/V
	salpstar = V/(a*b*c*sbet*sgam)
	sbetstar = V/(a*b*c*salp*sgam)
	sgamstar = V/(a*b*c*salp*sbet)
	calpstar = (cbet*cgam-calp)/(sbet*sgam)
	cbetstar = (calp*cgam-cbet)/(salp*sgam)
	cgamstar = (calp*cbet-cgam)/(salp*sbet)

	alpstar = n.arccos(calpstar)*180./n.pi;
	betstar = n.arccos(cbetstar)*180./n.pi;
	gamstar = n.arccos(cgamstar)*180./n.pi;
  
	return [astar, bstar, cstar, alpstar, betstar, gamstar]


def CellVolume(ucell):
        a = ucell[0]
        b = ucell[1]
        c = ucell[2]
        calp = n.cos(ucell[3]*n.pi/180.)
        cbet = n.cos(ucell[4]*n.pi/180.)
        cgam = n.cos(ucell[5]*n.pi/180.)

        angular = n.sqrt(1 - calp*calp - cbet*cbet - cgam*cgam + 2*calp*cbet*cgam)
        #Volume of unit cell
        V = a*b*c*angular                                             
	return V

def FormB(ucell):
	# calculate B matrix of (Gcart = B Ghkl) following eq. 3.4 in 
	#   H.F. Poulsen.
	#   Three-dimensional X-ray diffraction microscopy. 
	#   Mapping polycrystals and their dynamics. 
	#   (Springer Tracts in Modern Physics, v. 205), (Springer, Berlin, 2004).
	#
	#
	# FormB(unit_cell)
	#
	# unit_cell = [a, b, c, alpha, beta, gamma] 
	# returns B [3x3]
	#
	# Henning Osholm Sorensen, June 11, 2007.
	
        a = ucell[0]
        b = ucell[1]
        c = ucell[2]
        calp = n.cos(ucell[3]*n.pi/180.)
        cbet = n.cos(ucell[4]*n.pi/180.)
        cgam = n.cos(ucell[5]*n.pi/180.)
        salp = n.sin(ucell[3]*n.pi/180.)
        sbet = n.sin(ucell[4]*n.pi/180.)
        sgam = n.sin(ucell[5]*n.pi/180.)

        #Volume of unit cell
        V = CellVolume(ucell)

        #  Calculate reciprocal lattice parameters: NOTICE PHYSICIST DEFINITION of recip axes with 2*pi
        astar = 2*n.pi*b*c*salp/V                        
        bstar = 2*n.pi*a*c*sbet/V                        
        cstar = 2*n.pi*a*b*sgam/V                        
        salpstar = V/(a*b*c*sbet*sgam)                 
        sbetstar = V/(a*b*c*salp*sgam)                 
        sgamstar = V/(a*b*c*salp*sbet)                 
        calpstar = (cbet*cgam-calp)/(sbet*sgam)        
        cbetstar = (calp*cgam-cbet)/(salp*sgam)        
        cgamstar = (calp*cbet-cgam)/(salp*sbet)        

        # Form B matrix following eq. 3.4 in H.F Poulsen
        B = n.array([[astar, bstar*cgamstar, cstar*cbetstar       ],\
             [0,     bstar*sgamstar, -cstar*sbetstar*calp ],\
             [0,     0,               cstar*sbetstar*salp ]])
        return B



def FormAinv(ucell):
	# calculate the inverse of the A matrix given in eq. 3.23 of 
	#   H.F. Poulsen.
	#   Three-dimensional X-ray diffraction microscopy. 
	#   Mapping polycrystals and their dynamics. 
	#   (Springer Tracts in Modern Physics, v. 205), (Springer, Berlin, 2004).
	#
	#
	# FormAinv(unit_cell)
	#
	# unit_cell = [a, b, c, alpha, beta, gamma] 
	# returns Ainv [3x3]
	#
	# Jette Oddershede, March 7, 2008.
	
        a = ucell[0]
        b = ucell[1]
        c = ucell[2]
        calp = n.cos(ucell[3]*n.pi/180.)
        cbet = n.cos(ucell[4]*n.pi/180.)
        cgam = n.cos(ucell[5]*n.pi/180.)
        salp = n.sin(ucell[3]*n.pi/180.)
        sbet = n.sin(ucell[4]*n.pi/180.)
        sgam = n.sin(ucell[5]*n.pi/180.)

        #Volume of unit cell
        V = CellVolume(ucell)

        #  Calculate reciprocal lattice parameters
        salpstar = V/(a*b*c*sbet*sgam)                 
        calpstar = (cbet*cgam-calp)/(sbet*sgam)        

        # Form A matrix following eq. 3.23 in H.F Poulsen
        A = n.array([[a, b*cgam,  c*cbet       ],\
             [0, b*sgam, -c*sbet*calpstar ],\
             [0, 0,       c*sbet*salpstar ]])
        Ainv = n.linalg.inv(A)
        return Ainv


def A2ucell(A):
        # calculate lattice constants from the A-matix as
	# defined in H.F.Poulsen 2004 eqn.3.23
	#
	# A2ucell(A)
	#
	# A [3x3] upper triangular matrix
	# returns unit_cell = [a, b, c, alpha, beta, gamma] 
	#
	# Jette Oddershede, March 10, 2008.

		g = n.dot(n.transpose(A),A)
		a = n.sqrt(g[0,0])
		b = n.sqrt(g[1,1])
		c = n.sqrt(g[2,2])
		alpha = degrees(n.arccos(g[1,2]/b/c))
		beta  = degrees(n.arccos(g[0,2]/a/c))
		gamma = degrees(n.arccos(g[0,1]/a/b))
		ucell = [a, b, c, alpha, beta, gamma]
		return ucell
	
def epsilon2B(epsilon,A0inv):
        #   calculate B matrix of (Gcart = B Ghkl) from epsilon and A0inv
	#   as in H.F. Poulsen (2004) page 33.
        #
	# epsilon2B(epsilon, A0inv)
	#
	# epsilon = [e11, e12, e13, e22, e23, e33] 
	# A0inv = upper triangular 3x3 matrix, inverse of the A-matrix
	#                calculated using the unstrained lattice constants
	#
	# returns B [3x3] for strained lattice constants
	#
	# Jette Oddershede, March 10, 2008.
	
	A = n.zeros([3,3])
	A[0,0] = (epsilon[0]+1)/A0inv[0,0]
	A[1,1] = (epsilon[3]+1)/A0inv[1,1]
	A[2,2] = (epsilon[5]+1)/A0inv[2,2]
	A[0,1] = (2*epsilon[1]-A[0,0]*A0inv[0,1])/A0inv[1,1] 
	A[1,2] = (2*epsilon[4]-A[1,1]*A0inv[1,2])/A0inv[2,2]
	A[0,2] = (2*epsilon[2]-A[0,0]*A0inv[0,2]-A[0,1]*A0inv[1,2])/A0inv[2,2]
	strainedcell = A2ucell(A)
	B = FormB(strainedcell)
	return B
	
def euler2U(phi1,PHI,phi2):
	# U matrix from Euler angles phi1, PHI, phi2.
	# The formalism follows the ID11-3DXRD specs
	#
	#   U = euler2u(phi1, PHI, phi2)
	#
	# INPUT: phi, PHI, and phi2 in radians
	# OUTPUT [U11 U12 U13; U21 U22 U23; U31 U32 U33]
	#
	#  Henning Poulsen, Risoe 15/6 2002.
	#
	# Changed input angles to be in radians instead of degrees
	# Henning Osholm Sorensen, Riso National Laboratory, June 23, 2006.
	#
	# Translated from MATLAB to python by Jette Oddershede, March 26 2008
	#
	U = n.zeros([3,3])
	U[0,0] =  n.cos(phi1)*n.cos(phi2)-n.sin(phi1)*n.sin(phi2)*n.cos(PHI)
	U[1,0] =  n.sin(phi1)*n.cos(phi2)+n.cos(phi1)*n.sin(phi2)*n.cos(PHI)
	U[2,0] =  n.sin(phi2)*n.sin(PHI)
	U[0,1] =  -n.cos(phi1)*n.sin(phi2)-n.sin(phi1)*n.cos(phi2)*n.cos(PHI)
	U[1,1] =  -n.sin(phi1)*n.sin(phi2)+n.cos(phi1)*n.cos(phi2)*n.cos(PHI)
	U[2,1] =  n.cos(phi2)*n.sin(PHI)
	U[0,2] =  n.sin(phi1)*n.sin(PHI) 
	U[1,2] =  -n.cos(phi1)*n.sin(PHI)
	U[2,2] =  n.cos(PHI)
	return U
	
def U2euler(U):
        # Euler angles (phi1, PHI, phi2) from U matrix
	# The formalism follows the ID11-3DXRD specs
	# Note that there are two solutions
	# (phi1, PHI, phi2) AND (phi1 + pi, -PHI, phi2 + pi)
	# We pick the one with phi1 in the range [-pi/2 pi/2]
	#
	# Henning Poulsen, Risoe National Laboratory June 15, 2002.
	#
	# Fails if U[2,1] or U[1,2] = 0 e.g. then U[2,2] = ~1
	# If U[2,2] ~ 1 ph1 = ph2 = atan(U[1,0]/U[0,0])/2
	# In this case there is only one solution.
	#
	# Henning Osholm Sorensen, Risoe National Laboratory, June 23, 2006.
	#
	# Translated from MATLAB to python by Henning Osholm, March 28, 2008.
	phi1 = [0,0]
	PHI  = [0,0]
	phi2 = [0,0]

	PHI[0] = n.arccos(U[2,2])
	if PHI[0] < 0.0001:
            phi2[0] = n.arctan(U[1,0]/U[0,0])/2.
            phi1[0] = phi2[0]
	else:
            # There is two solutions
            phi1[0] = n.arctan(-U[0,2]/U[1,2])
            phi2[0] = n.arctan(-U[2,0]/U[2,1])
            PHI[1] = 2*n.pi-PHI[0]
	    phi1[1] = phi1[0]+n.pi
	    phi2[1] = phi2[0]+n.pi

	# The correct combination is found by brute-force
	minsum = n.Inf  
	for j in range(2):
	    for k in range(2):
                U2 = euler2U(phi1[1],PHI[j],phi2[k])
		Udev = abs(U2-U)
		sumUdev = n.sum(Udev)
		if sumUdev < minsum:
		    minsum = sumUdev
		    mj = j
		    mk = k
	return [ phi1[1], PHI[mj], phi2[mk] ]

def rod2U(r):
	# rod2U calculates the U orientation matrix given an oriention
	# represented in Rodrigues space. r = [r1, r2, r3]
	g = n.zeros((3,3))
	r2 = n.dot(r,r)

        for i in range(3):
            for j in range(3):
                if i==j:
                   fac = 1;
		else:
                   fac = 0
		term=0
		for k in range(3):
                   if [i,j,k] == [0,1,2] or [i,j,k] == [1,2,0] or [i,j,k] == [2,0,1]:
                      sign = 1
		   elif [i,j,k] == [2,1,0] or [i,j,k] == [0,2,1] or [i,j,k] == [1,0,2]:
		      sign = -1
		   else:
                      sign = 0
		   term = term + 2*sign*r[k];
		g[i,j] =  1/(1+r2) * ((1-r2)*fac + 2*r[i]*r[j] - term);
	return n.transpose(g)

def sintl(ucell,hkl):
	# sintl calculate sin(theta)/lambda of the reflection "hkl" given
	# the unit cell "ucell" 
	#
	# sintl(ucell,hkl)
	#
	# INPUT:  ucell = [a, b, c, alpha, beta, gamma]
	#         hkl = [h, k, l]
	# OUTPUT: sin(theta)/lambda
	#
	# Henning Osholm Sorensen, Risoe National Laboratory, June 23, 2006.

	a   = float(ucell[0])
	b   = float(ucell[1])
	c   = float(ucell[2])
	calp = n.cos(ucell[3]*n.pi/180.)
	cbet = n.cos(ucell[4]*n.pi/180.)
	cgam = n.cos(ucell[5]*n.pi/180.)

	(h,k,l) = hkl
	
	part1 = (h*h/a**2) * (1-calp**2) + (k*k/b**2) *\
		(1-cbet**2) + (l*l/c**2) * (1-cgam**2) +\
		2*h*k*(calp*cbet-cgam)/(a*b) + 2*h*l*(calp*cgam-cbet)/(a*c) +\
		2*k*l*(cbet*cgam-calp)/(b*c)

	part2 = 1 - (calp**2 + cbet**2 + cgam**2) + 2*calp*cbet*cgam

	stl= n.sqrt(part1) / (2*n.sqrt(part2))

	return stl


def genhkl(ucell,sysconditions,sintlmin,sintlmax):
    """
     Generate reflections up to maximum sin(theta)/lambda (sintlmax)
     The program follows the method described in: 
     Le Page and Gabe (1979) J. Appl. Cryst., 12, 464-466
    
     Henning Osholm Sorensen, June 23, 2006.
    """
    segm = n.array([[[ 0, 0,  0],[ 1, 0, 0],[ 0, 1, 0],[ 0, 0,  1]],\
                    [[-1, 0,  1],[-1, 0, 0],[ 0, 1, 0],[ 0, 0,  1]],\
                    [[-1, 1,  0],[-1, 0, 0],[ 0, 1, 0],[ 0, 0, -1]],\
                    [[ 0, 1, -1],[ 1, 0, 0],[ 0, 1, 0],[ 0, 0, -1]]])

    nref = 0
    H = n.array([[0,0,0]])         # Data of half sphere
    stl = n.array([0])
    sintlH = 0.0

    for i in range(4):
        segn = i
        # initialize the identifiers
        htest = 0
        ktest = 0
        ltest = 0
        HLAST = segm[segn,0,:]
        HSAVE = HLAST
        sintlH= sintl(ucell,HSAVE)

        while ltest == 0:
            while ktest == 0:
                while htest == 0:
                    nref = nref + 1
                    if nref != 1:
                        if sysabs(HLAST,sysconditions) == 0:
                            H = n.concatenate((H,[HLAST]))
                            H = n.concatenate((H,[-HLAST]))
                            stl = n.concatenate((stl,[sintlH]))
                            stl = n.concatenate((stl,[sintlH]))
                        else: 
                            nref=nref - 1
                    HNEW = HLAST + segm[segn,1,:]
                    sintlH = sintl(ucell,HNEW)
                    #if (sintlH >= sintlmin) and (sintlH <= sintlmax):
                    if sintlH <= sintlmax:
                        HLAST = HNEW
                    else: 
                        htest = 1
      
                HLAST[0] = HSAVE[0]
                HLAST    = HLAST + segm[segn,2,:]
                HNEW     = HLAST
                sintlH   = sintl(ucell,HNEW)
                if sintlH > sintlmax:
                    ktest = 1
                htest = 0

            HLAST[1] = HSAVE[1]
            HLAST = HLAST + segm[segn,3,:]
            HNEW = HLAST
            sintlH=sintl(ucell,HNEW)
            if sintlH > sintlmax:
                ltest = 1
            ktest = 0

    H =  H[1:]  #remove the [0 0 0] used for being able to use n.concatanate
    #stl =  stl[1:] #remove the [0 0 0] used for being able to use n.concatanate
    #stl = transpose([stl])
    #Hstl = concatenate((H,stl),1) # combine hkl and sintl
    #return Hstl
    return H

def sysabs(hkl,syscond):
    #  sysabs checks whether a reflection is systematic absent
    #  
    #  sysabs = sysabs(hkl,syscond)
    # 
    #  INPUT: hkl = [h k l] 
    #          syscond: [1x23] with condition for systematic absences in this
    #          space group, X in syscond should given as shown below
    #  OUTPUT: sysbs: if 1 the reflection is systematic absent 
    #                 if 0 its not
    # 
    # syscond:
    # class        systematic abs               sysconditions[i]
    # HKL          H+K=XN                            0
    #              H+L=XN                            1
    #              K+L=XN                            2
    #              H+K,H+L,K+L = XN                  3
    #              H+K+L=XN                          4
    #              -H+K+L=XN                         5 
    # HHL          H=XN                              6
    #              L=XN                              7
    #              H+L=XN                            8
    #              2H+L=XN                           9
    # 0KL          K=XN                             10
    #              L=XN                             11
    #              K+L=XN                           12
    # H0L          H=XN                             13
    #              L=XN                             14
    #              H+L=XN                           15
    # HK0          H=XN                             16
    #              K=XN                             17
    #              H+K=XN                           18
    # HH0          H=XN                             19
    # H00          H=XN                             20
    # 0K0          K=XN                             21
    # 00L          L=XN                             22
    # Henning Osholm Sorensen, June 23, 2006.
    
    (h, k, l) = hkl
    sysabs = 0
    
    # HKL class
    if syscond[0] != 0:
        x = syscond[0]
        if (abs(h+k))%x !=0:
            sysabs=1

    if syscond[1] != 0 :
        x = syscond[1]
        if (abs(h+l))%x !=0:
            sysabs=1

    if syscond[2] != 0:
        x = syscond[2]
        if (abs(k+l))%x !=0:
            sysabs=1

    if syscond[3] != 0:
        sysabs=1
        x = syscond[3]
        if (abs(h+k))%x == 0:
            if (abs(h+l))%x == 0:
                if  (abs(k+l))%x == 0:
                    sysabs=0

    if syscond[4] != 0:
        x = syscond[4]
        if (abs(h+k+l))%x != 0:
            sysabs=1

    if syscond[5] != 0:
        x = syscond[5]
        if (abs(-h+k+l))%x != 0:
            sysabs=1

    # HHL class
    if (h-k) == 0:
        if syscond[6] != 0 :
            x = syscond[6]
            if (abs(h))%x != 0:
                sysabs = 1
        if syscond[7] != 0:
            x = syscond[7]
            if (abs(l))%x != 0:
                sysabs = 1
        if syscond[8] != 0:
            x = syscond[8]
            if (abs(h+l))%x != 0:
                sysabs = 1
        if syscond[9] != 0:
            x = syscond[9]
            if (abs(h+h+l))%x != 0:
                sysabs = 1

    # 0KL class
    if h == 0:
        if syscond[10] != 0:
            x = syscond[10]
            if (abs(k))%x != 0:
                sysabs = 1
        if syscond[11] != 0:
            x = syscond[11]
            if (abs(l))%x != 0:
                sysabs = 1
        if syscond[12] != 0:
            x = syscond[12]
            if (abs(k+l))%x != 0:
                sysabs = 1

    # H0L class
    if k == 0:
        if syscond[13] != 0:
            x = syscond[13]
            if (abs(h))%x != 0:
                sysabs = 1
        if syscond[14] != 0:
            x = syscond[14]
            if (abs(l))%x != 0:
                sysabs = 1
        if syscond[15] != 0:
            x = syscond[15]
            if (abs(h+l))%x != 0:
                sysabs = 1


    # HK0 class
    if l == 0:
        if syscond[16] != 0:
            x = syscond[16]
            if (abs(h))%x != 0:
                sysabs = 1
        if syscond[17] != 0:
            x = syscond[17]
            if (abs(k))%x != 0:
                sysabs = 1
        if syscond[18] != 0:
            x = syscond[18]
            if (abs(h+k))%x != 0:
                sysabs = 1

    # HH0 class
    if l == 0:
        if h-k==0:
            if syscond[19] != 0: 
                x = syscond[19]
                if (abs(h))%x != 0:
                    sysabs = 1

    # H00 class
    if abs(k)+abs(l) == 0:
        if syscond[20] != 0:
            x = syscond[20]
            if (abs(h))%x != 0:
                sysabs = 1

    # 0K0 class
    if abs(h)+abs(l) == 0:
        if syscond[21] != 0:
            x = syscond[21]
            if (abs(k))%x != 0:
                sysabs = 1

    # 00L class
    if abs(h)+abs(k) == 0:
        if syscond[22] != 0:
            x = syscond[22]
            if (abs(l))%x != 0:
                sysabs = 1

    return sysabs


