'''
BSD 3-Clause License

Copyright (c) 2019, open-struct-engineer developers and Donald N. Bockoven III
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

from __future__ import division
import math
import matplotlib.pyplot as plt

def stress_strain_desayi_krishnan(fprimec, ultimate_strain, k, strain):
    '''
    method for a parabolic stress-strain relationship for concrete in compression
    Desayi, P. and Krishnan, S., Equation for the Stress-Strain Curve of Concrete, ACI
    Journal, Proceedings V. 61, No. 3, Mar. 1964, pp. 345-350

    fprimec = f'c = 28-day compressive strength of concrete -- type: float
    ultimate_strain = eu = strain at failure -- type: float  ACI: 0.003 (English Units)
    k = k*f'c = stress at ultimate strain -- type: float  ACI: 0.85 (English Units)
    strain_report = e = strain at location where stress is desired -- type: float
    '''
    if strain <=0:
        return 0

    else:
        fo = fprimec

        # solve for eo = strain at fo
        # E = 2*fo / eo
        # eo has two possible solutions
        # eo = eu - sqrt(-1*(k^2 - 1) * eu^2) / k or sqrt(-1*(k^2 - 1) * eu^2) + eu / k

        eo1 = (ultimate_strain - math.sqrt(-1*(math.pow(k,2) - 1)*math.pow(ultimate_strain,2))) / k
        eo2 = (math.sqrt(-1*(math.pow(k,2) - 1)*math.pow(ultimate_strain,2))+ultimate_strain) / k

        eo = min(eo1,eo2)

        E = 2*fo / eo

        f = (E*strain) / (1+math.pow(strain/eo,2))

        return f

def stress_strain_collins_et_all(fprimec, ultimate_strain, strain):
    '''
    method for a parabolic stress-strain relationship for concrete in compression
    Collins, M.P., Mitchell D. and MacGregor, J.G., Structural Consideration for High-Strength
    Concrete, Concrete International, V. 15, No. 5, May 1993, pp. 27-34.
    '''
    if strain <=0:
        return 0

    else:
        k = 0.67 + (fprimec / 9000.0) # for PSI units
        n = 0.8 + (fprimec / 2500.0) # for PSI units
        Ec = (40000*math.sqrt(fprimec)) + 1000000 # for PSI units

        ecprime = (fprimec / Ec)*(n/(n-1))

        e = strain/ecprime

        if e <= 1:
            f = ((e) * (n / (n-1+math.pow(e,n)))) * fprimec
        else:
            f = ((e) * (n / (n-1+math.pow(e,n*k)))) * fprimec

        return f

def stress_strain_whitney(fprimec, ultimate_strain, strain):
    '''
    method for the Whitney Stress block used in ACI 318
    '''

    if fprimec <= 4000:
        beta1 = 0.85
    elif fprimec <= 8000:
        beta1 = 0.85 - ((0.05*(fprimec-4000))/1000)
    else:
        beta1 = 0.65

    if strain <= (ultimate_strain - (ultimate_strain*beta1)):
        return [0, beta1]

    else:
        return [0.85*fprimec, beta1]

def stress_strain_steel(fy, yield_strain, Es, strain):
    '''
    Linear stress strain definition that will return
    a linear value between 0 and +/- the yield strain
    or Fy is the strain is above or below the yield strain
    '''
    if Es == 0:
        if abs(strain) >= yield_strain:
            return (strain/abs(strain)) * fy
    
        else:
            return (strain*fy)/yield_strain       
    else:
        if abs(strain)*Es >= yield_strain*Es:
            return (strain/abs(strain)) * fy
    
        else:
            return (strain*Es)


def strain_at_depth(eu,neutral_axis_depth,depth_of_interest):
    '''
    Given and Neutral Axis Depth and the maximum compressive strain
    at the extreme compression fiber

    return the associated strain at the depth of interest

    assumptions:
        the strain varies linearly along the elevation axis (y-axis)
        0 depth is the point max compression strain, eu.

    will return a (+) strain for areas in compression and a (-) negative
    strain when area is in tension
    '''

    c = neutral_axis_depth
    d = depth_of_interest

    if c == 0:
        c = 0.000001
    else:
        c = c
    if c-d > 0:

        e  = ((c-d)/c)*eu

    else:
        e = ((c-d)/c)*eu

    return e

def plastic_center(bars_x=[1], bars_y=[1], fy=60000, As=[0.31], fc=3000, eu=0.003, k=0.85, conc_area=1, conc_centroid=[0,0]):
    '''
    given the ulitmate strain, f'c (28-day) strength and k for concrete
    return a the plastic centroid for the three stress-strain equations
    of the concrete

    accounting for the bar area subtracting from the concrete area by (fy/fc@eu - 1)
    similar approach to transformed sections using n = Es/Ec
    '''

    fc_collins = stress_strain_collins_et_all(fc,eu,eu)
    fc_desayi = stress_strain_desayi_krishnan(fc,eu,k,eu)
    fc_whitney = stress_strain_whitney(fc,eu,eu)

    fc = [fc_collins, fc_desayi, fc_whitney[0]]

    cc = [i*conc_area for i in fc]
    cc_mx = [i*conc_centroid[1] for i in cc]
    cc_my = [i*conc_centroid[0] for i in cc]

    C = []
    C_mx = []
    C_my = []
    cb = []
    cb_mx = []
    cb_my = []
    pc = []

    count = 0
    for c in fc:
        cb.append([i * (fy/c  - 1) for i in As])

        C.append(cc[count] + sum(cb[-1]))

        cb_mx.append([(cb[-1][i] * bars_y[i]) for i in range(len(bars_x))])
        cb_my.append([(cb[-1][i] * bars_x[i]) for i in range(len(bars_x))])

        C_mx.append(cc_mx[count]+sum(cb_mx[-1]))
        C_my.append(cc_my[count]+sum(cb_my[-1]))

        yp = C_mx[-1]/C[-1]
        xp = C_my[-1]/C[-1]

        pc.append([xp,yp])

        count +=1

    return pc,[fc,cc,cc_mx,cc_my,cb,cb_mx,cb_my,C,C_mx,C_my]
