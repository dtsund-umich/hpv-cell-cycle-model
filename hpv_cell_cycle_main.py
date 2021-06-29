# Copyright (c) 2015 Derrick Sund
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


from scipy.integrate import odeint
from numpy import arange
import time
import datetime
import os
import sys

infile = ""
dirname = ""

if len(sys.argv) > 1:
    infile = sys.argv[1]
    if not os.path.isfile(infile):
        sys.stderr.write(infile + ": No such file found.\n")
        sys.exit(1)

#Constants.  Do not add constants directly to the derivative function; violators
#will have rabid weasels set upon them.
#All of these constants come directly from the Goldbeter paper.

GF = 100 #XXX This one is adjustable
K_agf = 0.1
k_dap1 = 0.15
eps = 17
v_sap1 = 1
k_de2f = 0.002
k_de2fp = 1.1
k_dprb = 0.01
k_dprbp = 0.06
k_dprbpp = 0.04
k_pc1 = 0.05
k_pc2 = 0.5
k_pc3 = 0.025
k_pc4 = 0.5
K_1 = 0.1
K_2 = 0.1
K_3 = 0.1
K_4 = 0.1
V_1 = 2.2
V_2 = 2
V_3 = 1
V_4 = 2
K_1e2f = 5
K_2e2f = 5
V_1e2f = 4
V_2e2f = 0.75
v_se2f = 0.15
v_sprb = 0.8
Cdk4_tot = 1.5
K_i7 = 0.1
K_i8 = 2
k_cd1 = 0.4
k_cd2 = 0.005
k_decom1 = 0.1
k_com1 = 0.175
k_c1 = 0.15
k_c2 = 0.05
k_ddd = 0.05
K_dd = 0.1
K_1d = 0.1
K_2d = 0.1
V_dd = 5
V_m1d = 1
V_m2d = 0.2
a_e = 0.25
Cdk2_tot = 2
i_b1 = 0.5
K_i9 = 0.1
K_i10 = 2
k_ce = 0.29
k_c3 = 0.2
k_c4 = 0.1
k_decom2 = 0.1
k_com2 = 0.2
k_dde = 0.005
k_ddskp2 = 0.005
k_dpe = 0.075
k_dpei = 0.15
K_de = 0.1
K_dceskp2 = 2
K_dskp2 = 0.5
K_cdh1 = 0.4
K_1e = 0.1
K_2e = 0.1
K_5e = 0.1
K_6e = 0.1
V_de = 3
V_dskp2 = 1.1
V_m1e = 2
V_m2e = 1.4
V_m5e = 5
V_6e = 0.8
v_spei = 0.13
v_sskp2 = 0.15
x_e1 = 1
x_e2 = 1
a_a = 0.2
i_b2 = 0.5
K_i11 = 0.1
K_i12 = 2
K_i13 = 0.1
K_i14 = 2
k_ca = 0.0375
k_decom3 = 0.1
k_com3 = 0.2
k_c5 = 0.15
k_c6 = 0.125
k_dda = 0.005
k_ddp27 = 0.06
k_ddp27p = 0.01
k_dcdh1a = 0.1
k_dcdh1i = 0.2
k_dpa = 0.075
k_dpai = 0.15
K_da = 1.1
K_dp27p = 0.1
K_dp27skp2 = 0.1
K_acdc20 = 2
K_1a = 0.1
K_2a = 0.1
K_1cdh1 = 0.01
K_2cdh1 = 0.01
K_5a = 0.1
K_6a = 0.1
K_1p27 = 0.5
K_2p27 = 0.5
V_dp27p = 5
V_da = 2.5
V_m1a = 2
V_m2a = 1.85
V_m5a = 4
V_6a = 1
v_scdh1a = 0.11
v_spai = 0.105
v_s1p27 = 0.8
v_s2p27 = 0.1
V_1cdh1 = 1.25
V_2cdh1 = 8
V_1p27 = 100
V_2p27 = 0.1
x_a1 = 1
x_a2 = 1
a_b = 0.11
Cdk1_tot = 0.5
i_b = 0.75
i_b3 = 0.5
k_c7 = 0.12
k_c8 = 0.2
k_decom4 = 0.1
k_com4 = 0.25
k_dcdc20a = 0.05
k_dcdc20i = 0.14
k_ddb = 0.005
k_dpb = 0.1
k_dpbi = 0.2
k_dwee1 = 0.1
k_dwee1p = 0.2
K_db = 0.005
K_dbcdc20 = 0.2
K_dbcdh1 = 0.1
k_sw = 5
K_1b = 0.1
K_2b = 0.1
K_3b = 0.1
K_4b = 0.1
K_5b = 0.1
K_6b = 0.1
K_7b = 0.1
K_8b = 0.1
v_cb = 0.05
V_db = 0.06
V_m1b = 3.9
V_m2b = 2.1
v_scdc20i = 0.1
V_m3b = 8
V_m4b = 0.7
V_m5b = 5
V_6b = 1
V_m7b = 1.2
V_m8b = 1
v_spbi = 0.12
v_swee1 = 0.06
x_b1 = 1
x_b2 = 1
ATR_tot = 0.5
Chk1_tot = 0.5
Cdc45_tot = 0.5
k_aatr = 0.022
k_datr = 0.15
k_dpol = 0.2
k_dprim = 0.15
k_spol = 0.8
k_sprim = 0.05
K_1cdc45 = 0.02
K_2cdc45 = 0.02
K_1chk = 0.5
K_2chk = 0.5
Pol_tot = 0.5
V_1cdc45 = 0.8
V_2cdc45 = 0.12
V_1chk = 4
V_2chk = 0.1
K_dw = 0.5
K_iw = 1
n = 4
v_dw = 0.5
v_sw = 0


Chk1 = 0
Mw = 0

#md = (k_dd * v_sd * gf / (k_gf + gf)) / (v_dd - (v_sd * gf / (k_gf + gf)))

#Ink4 coefficients
alpha_ink4 = 0#1 #Set this to 0 to nullify the Ink4 module
omega_ink4 = 1

beta_ink4cdk = 1
delta_ink4cdk = 0.1

#E7-pRB coefficients
beta_e7prb = 1
delta_e7prb = 1
beta_e7prbp = 1
delta_e7prbp = 1
omega_e7prb = 1
omega_e7prbp = 1


#p53 module coefficients
alpha_p14 = 0.1
K_i15 = 0.1
K_i16 = 2
omega_p14 = 0.15
beta_p14mdm2 = 0.05
delta_p14mdm2 = 0.5
alpha_mdm2 = 0.5
omega_mdm2 = 0.15
beta_p14mdm2 = 0.05
delta_p14mdm2 = 0.5
omega_p14mdm2 = 0.15
alpha_p53 = 0.15
omega_p53 = 0.1
omega_p53mdm2 = 0.15
omega_p53e6 = 0.15
alpha_p21 = 0#4 #Set this to 0 to nullify the effects of p53 module
omega_p21 = 0.15
beta_p21e7 = 0.2
beta_p21md = 0.2
beta_p21me = 0.2
beta_p21ma = 0.2
beta_p21mb = 0.2
delta_p21e7 = 0.2
delta_p21md = 0.2
delta_p21me = 0.2
delta_p21ma = 0.2
delta_p21mb = 0.2
k_p53 = 0.2
omega_p21me = 1
k_p21 = 0.2

#Dummy initial conditions
y0 = [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0,0,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]


E6_tot = 0
E7_tot = 0


#Potentially override parameters
if infile != "":
    reader = open(infile)
    for line in reader.readlines():
        exec(line)

#Functions to be called from the derivative functions.
def E6(t):
    return E6_tot#5 #dummy

def E7(t):
    return E7_tot#5 #dummy

def fM(y):
    if y[2] == 0:
        return 0.018
    return 0.018+100*y[2]**2/(y[0]+y[1]+y[2]+y[4])**2 #Tyson, adjustable

#Variable key
names = []
names.append("AP1")
names.append("pRB")
names.append("pRBc1")
names.append("pRBp")
names.append("pRBc2")
names.append("pRBpp")
names.append("E2F")
names.append("E2Fp")
names.append("Cd")
names.append("Mdi")
names.append("Md")
names.append("Mdp27")
names.append("Ce")
names.append("Mei")
names.append("Me")
names.append("Skp2")
names.append("Mep27")
names.append("Pei")
names.append("Pe")
names.append("Ca")
names.append("Mai")
names.append("Ma")
names.append("Map27")
names.append("p27")
names.append("p27p")
names.append("Cdh1i")
names.append("Cdh1a")
names.append("Pai")
names.append("Pa")
names.append("Cb")
names.append("Mbi")
names.append("Mb")
names.append("Mbp27")
names.append("Cdc20i")
names.append("Cdc20a")
names.append("Pbi")
names.append("Pb")
names.append("Wee1")
names.append("Wee1p")
names.append("Ink4")
names.append("Ink4-CDK")
names.append("E7-pRB")
names.append("E7-pRBp")
names.append("p14")
names.append("MDM2")
names.append("MDM2-p14")
names.append("p53")
names.append("p21")
names.append("E7-p21")
names.append("p21-Md")
names.append("p21-Me")
names.append("p21-Ma")
names.append("p21-Mb")

#y[0] = AP1
#y[1] = pRB
#y[2] = pRBc1
#y[3] = pRBp
#y[4] = pRBc2
#y[5] = pRBpp
#y[6] = E2F
#y[7] = E2Fp
#y[8] = Cd
#y[9] = Mdi
#y[10] = Md
#y[11] = Mdp27
#y[12] = Ce
#y[13] = Mei
#y[14] = Me
#y[15] = Skp2
#y[16] = Mep27
#y[17] = Pei
#y[18] = Pe
#y[19] = Ca
#y[20] = Mai
#y[21] = Ma
#y[22] = Map27
#y[23] = p27
#y[24] = p27p
#y[25] = Cdh1i
#y[26] = Cdh1a
#y[27] = Pai
#y[28] = Pa
#y[29] = Cb
#y[30] = Mbi
#y[31] = Mb
#y[32] = Mbp27
#y[33] = Cdc20i
#y[34] = Cdc20a
#y[35] = Pbi
#y[36] = Pb
#y[37] = Wee1
#y[38] = Wee1p
#y[39] = Ink4
#y[40] = Ink4-CDK
#y[41] = E7-pRB
#y[42] = E7-pRBp
#y[43] = p14
#y[44] = MDM2
#y[45] = MDM2-p14
#y[46] = p53
#y[47] = p21
#y[48] = E7-p21
#y[49] = p21-Md
#y[50] = p21-Me
#y[51] = p21-Ma
#y[52] = p21-Mb



#The derivative function for the differential equation system.
def func(y,t):
    return [
             (v_sap1 * GF/(K_agf +GF) - k_dap1 * y[0]) * eps,
             (v_sprb - k_pc1 * y[1] * y[6] + k_pc2 * y[2] - V_1 * y[1]/(K_1 + y[1]) * (y[10] + y[11]) + V_2 * y[3]/(K_2 + y[3]) - k_dprb * y[1] - beta_e7prb * E7(t) * y[1] + delta_e7prb * y[41]) * eps,
             (k_pc1 * y[1] * y[6] - k_pc2 * y[2]) * eps,
             (V_1 * y[1]/(K_1 + y[1]) * (y[10] + y[11]) - V_2 * y[3]/(K_2 + y[3]) - V_3 * y[3]/(K_3 + y[3]) * y[14] + V_4 * y[5]/(K_4 + y[5]) - k_pc3 * y[3] * y[6] + k_pc4 * y[4] - k_dprbp * y[3] - beta_e7prbp * E7(t) * y[3] + delta_e7prbp * y[42]) * eps,
             (k_pc3 * y[3] * y[6] - k_pc4 * y[4]) * eps,
             (V_3 * y[3]/(K_3 + y[3]) * y[14] - V_4 * y[5]/(K_4 + y[5]) - k_dprbpp * y[5]) * eps,
             (v_se2f - k_pc1 * y[1] * y[6] + k_pc2 * y[2] - k_pc3 * y[3] * y[6] + k_pc4 * y[4] - V_1e2f * y[21] * y[6]/(K_1e2f + y[6]) + V_2e2f * y[7]/(K_2e2f + y[7]) - k_de2f * y[6]) * eps,
             (V_1e2f * y[21] * y[6]/(K_1e2f + y[6]) - V_2e2f * y[7]/(K_2e2f + y[7]) - k_de2fp * y[7]) * eps,
             (k_cd1 * y[0] + k_cd2 * y[6] * K_i7/(K_i7 + y[1]) * K_i8/(K_i8 + y[3]) - k_com1 * y[8] * (Cdk4_tot - (y[9] + y[10] + y[11] + y[40])) + k_decom1 * y[9] - V_dd * y[8]/(K_dd + y[8]) - k_ddd * y[8]) * eps,
             (k_com1 * y[8] * (Cdk4_tot - (y[9] + y[10] + y[11] + y[40])) - k_decom1 * y[9] + V_m2d * y[10]/(K_2d + y[10]) - V_m1d * y[9]/(K_1d + y[9])) * eps,
             (V_m1d * y[9]/(K_1d + y[9]) - V_m2d * y[10]/(K_2d + y[10]) - k_c1 * y[10] * y[23] + k_c2 * y[11] - beta_p21md * y[47] * y[10] + delta_p21md * y[49]) * eps,
             (k_c1 * y[10] * y[23] - k_c2 * y[11]) * eps,
             (k_ce * y[6] * K_i9/(K_i9 + y[1]) * K_i10/(K_i10 + y[3]) - k_com2 * y[12] * (Cdk2_tot - (y[13] + y[14] + y[16] + y[20] + y[21] + y[22])) + k_decom2 * y[13] - V_de * y[15]/(K_dceskp2 + y[15]) * y[12]/(K_de + y[12]) - k_dde * y[12]) * eps,
             (k_com2 * y[12] * (Cdk2_tot - (y[13] + y[14] + y[16] + y[20] + y[21] + y[22])) - k_decom2 * y[13] + V_m2e * (y[37] + i_b1) * y[14]/(K_2e + y[14]) - V_m1e * y[18] * y[13]/(K_1e + y[13]) ) * eps,
             (V_m1e * y[18] * y[13]/(K_1e + y[13]) - V_m2e * (y[37] + i_b1) * y[14]/(K_2e + y[14]) - k_c3 * y[14] * y[23] + k_c4 * y[16] - beta_p21me * y[47] * y[14] + delta_p21me * y[50]) * eps,
             (v_sskp2 - V_dskp2 * y[15]/(K_dskp2 + y[15]) * y[26]/(K_cdh1 + y[26]) - k_ddskp2 * y[15]) * eps,
             (k_c3 * y[14] * y[23] - k_c4 * y[16]) * eps,
             (v_spei + V_6e * (x_e1 + x_e2 * Chk1) * y[18]/(K_6e + y[18]) - V_m5e * (y[14] + a_e) * y[17]/(K_5e + y[17]) - k_dpei * y[17]) * eps,
             (V_m5e * (y[14] + a_e) * y[17]/(K_5e + y[17]) - V_6e * (x_e1 + x_e2 * Chk1) * y[18]/(K_6e + y[18]) - k_dpe * y[18]) * eps,
             (k_ca * y[6] * K_i11/(K_i11 + y[1]) * K_i12/(K_i12 + y[3]) - k_com3 * y[19] * (Cdk2_tot - (y[13] + y[14] + y[16] + y[20] + y[21] + y[22])) + k_decom3 * y[20] - V_da * y[19]/(K_da + y[19]) * y[34]/(K_acdc20 + y[34]) - k_dda * y[19]) * eps,
             (k_com3 * y[19] * (Cdk2_tot - (y[13] + y[14] + y[16] + y[20] + y[21] + y[22])) - k_decom3 * y[20]  + V_m2a * (y[37] + i_b2) * y[21]/(K_2a + y[21]) - V_m1a * y[28] * y[20]/(K_1a + y[20])) * eps,
             (V_m1a * y[28] * y[20]/(K_1a + y[20]) - V_m2a * (y[37] + i_b2) * y[21]/(K_2a + y[21]) - k_c5 * y[21] * y[23] + k_c6 * y[22] - beta_p21ma * y[47] * y[21] + delta_p21ma * y[51]) * eps,
             (k_c5 * y[21] * y[23] - k_c6 * y[22]) * eps,
             (v_s1p27 + v_s2p27 * y[6] * K_i13/(K_i13 + y[1]) * K_i14/(K_i14 + y[3]) - k_c1 * y[10] * y[23] + k_c2 * y[11] - k_c3 * y[14] * y[23] + k_c4 * y[16] - k_c5 * y[21] * y[23] + k_c6 * y[22] - k_c7 * y[31] * y[23] + k_c8 * y[32] - V_1p27 * y[14] * y[23]/(K_1p27 + y[23]) + V_2p27 * y[24]/(K_2p27 + y[24]) - k_ddp27 * y[23]) * eps,
             (V_1p27 * y[14] * y[23]/(K_1p27 + y[23]) - V_2p27 * y[24]/(K_2p27 + y[24]) - V_dp27p * y[15]/(K_dp27skp2 + y[15]) * y[24]/(K_dp27p + y[24]) - k_ddp27p * y[24]) * eps,
             (V_2cdh1 * y[26]/(K_2cdh1 + y[26]) * (y[21] + y[31]) - V_1cdh1 * y[25]/(K_1cdh1 + y[25]) - k_dcdh1i * y[25]) * eps,
             (v_scdh1a - V_2cdh1 * y[26]/(K_2cdh1 + y[26]) * (y[21] + y[31]) + V_1cdh1 * y[25]/(K_1cdh1 + y[25]) - k_dcdh1a * y[26]) * eps,
             (v_spai + V_6a * (x_a1 + x_a2 * Chk1) * y[28]/(K_6a + y[28]) - V_m5a * (y[21] + a_a) * y[27]/(K_5a + y[27]) - k_dpai * y[27]) * eps,
             (-V_6a * (x_a1 + x_a2 * Chk1) * y[28]/(K_6a + y[28]) + V_m5a * (y[21] + a_a) * y[27]/(K_5a + y[27]) - k_dpa * y[28]) * eps,
             (v_cb - k_com4  * y[29] * (Cdk1_tot - (y[30] + y[31] + y[32])) + k_decom4 * y[30] - V_db * y[29]/(K_db + y[29]) *(y[34]/(K_dbcdc20 + y[34]) + y[26]/(K_dbcdh1 + y[26])) - k_ddb * y[29]) * eps,
             (k_com4  * y[29] * (Cdk1_tot - (y[30] + y[31] + y[32])) - k_decom4 * y[30] + V_m2b * (y[37] + i_b3) * y[31]/(K_2b + y[31]) - V_m1b * y[36] * y[30]/(K_1b + y[30])) * eps,
             (V_m1b * y[36] * y[30]/(K_1b + y[30]) - V_m2b * (y[37] + i_b3) * y[31]/(K_2b + y[31]) - k_c7 * y[31] * y[23] + k_c8 * y[32] - beta_p21mb * y[47] * y[31] + delta_p21mb * y[52]) * eps,
             (k_c7 * y[31] * y[23] - k_c8 * y[32]) * eps,
             (v_scdc20i - V_m3b * y[31] * y[33]/(K_3b + y[33]) + V_m4b * y[34]/(K_4b + y[34]) - k_dcdc20i * y[33]) * eps,
             (V_m3b * y[31] * y[33]/(K_3b + y[33]) - V_m4b * y[34]/(K_4b + y[34]) - k_dcdc20a * y[34]) * eps,
             (v_spbi + V_6b * (x_b1 + x_b2 * Chk1) * y[36]/(K_6b + y[36]) - V_m5b * (y[31] + a_b) * y[35]/(K_5b + y[35]) - k_dpbi * y[35]) * eps,
             (V_m5b * (y[31] + a_b) * y[35]/(K_5b + y[35]) - V_6b * (x_b1 + x_b2 * Chk1) * y[36]/(K_6b + y[36]) - k_dpb * y[36]) * eps,
             (v_swee1 + k_sw * Mw - V_m7b * (y[31] + i_b) * y[37]/(K_7b + y[37]) + V_m8b * y[38]/(K_8b + y[38]) - k_dwee1 * y[37]) * eps,
             (V_m7b * (y[31] + i_b) * y[37]/(K_7b + y[37]) - V_m8b * y[38]/(K_8b + y[38]) - k_dwee1p * y[38]) * eps,
             (alpha_ink4 - omega_ink4 * y[39] - beta_ink4cdk * y[39] * (Cdk4_tot - (y[9] + y[10] + y[11] + y[40])) + delta_ink4cdk * y[40]) * eps,
             (beta_ink4cdk * y[39] * (Cdk4_tot - (y[9] + y[10] + y[11] + y[40])) - delta_ink4cdk * y[40]) * eps,
             (beta_e7prb * E7(t) * y[1] - delta_e7prb * y[41] - omega_e7prb * y[41]) * eps,
             (beta_e7prbp * E7(t) * y[3] - delta_e7prbp * y[42] - omega_e7prbp * y[42]) * eps,
             (alpha_p14 * y[6] * K_i15/(K_i15 + y[1]) * K_i16/(K_i16 + y[3]) - omega_p14 * y[43] - beta_p14mdm2 * y[43] * y[44] + delta_p14mdm2 * y[45]) * eps,
             (alpha_mdm2 * y[46] - omega_mdm2 * y[44] - beta_p14mdm2 * y[43] * y[44] + delta_p14mdm2 * y[45]) * eps,
             (beta_p14mdm2 * y[43] * y[44] - delta_p14mdm2 * y[45] - omega_p14mdm2 * y[45]) * eps,
             (alpha_p53 - omega_p53 * y[46] - y[46]/(k_p53 + y[46]) * (omega_p53mdm2 * y[44] + omega_p53e6 * E6(t)) ) * eps,
             (alpha_p21 * y[46] - omega_p21 * y[47] - omega_p21me * y[47]/(y[47] + k_p21) * y[14] - beta_p21e7 * y[47] * E7(t) + delta_p21e7 * y[48] - beta_p21md * y[47] * y[10] + delta_p21md * y[49] - beta_p21me * y[47] * y[14] + delta_p21me * y[50] - beta_p21ma * y[47] * y[21] + delta_p21ma * y[51] - beta_p21mb * y[47] * y[31] + delta_p21mb * y[52]) * eps,
             (beta_p21e7 * y[47] * E7(t) - delta_p21e7 * y[48]) * eps,
             (beta_p21md * y[47] * y[10] - delta_p21md * y[49]) * eps,
             (beta_p21me * y[47] * y[14] - delta_p21me * y[50]) * eps,
             (beta_p21ma * y[47] * y[21] - delta_p21ma * y[51]) * eps,
             (beta_p21mb * y[47] * y[31] - delta_p21mb * y[52]) * eps,
           ]

t = arange(0, 500.0, 0.01)

y = odeint(func, y0, t, ixpr=True)

if dirname == "":
    dirname = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H:%M:%S')
os.makedirs(dirname)
os.chdir(dirname)

for i in range(len(y0)):
    writer = open(names[i]+".txt", 'w')
    for j in range(len(t)):
        writer.write(str(t[j]) + " " + str(y[j][i]) + "\n")
    writer.close()

