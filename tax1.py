
zus = 0.0976 + 0.015 #stawka emerytalna + rentowa
ch = 0.0245 #stawka chorobowa
z = 0.0125 #stawka zdrowotna nieodliczalna od podatku
ku = 111.25 * 12 #koszty uzyskania przychodu
kw = 556.02 #kwota wolna od podatku
z7 = 0.0775 #stawka ub. zdrowotnego odliczana od podatku
z9 = 0.09 #stawka ub. zdrowotnego placona
step = 85528
limit_zus = 127890
r_1 = 0.18 #stawka podatku do progu podatkowego (step)
r_2 = 0.32 #stawka powyzej progu podatkowego
tax_1 = 15395.04


def gross_net(B):
    print()
    print('----------------------------------------------')

    base = B * (1 - zus - ch) - ku
    #print('base: ', base)
    if base < step:
        N = B*(1 - zus - ch)*(1 - z - r_1) + ku*r_1 + kw
    elif B <= limit_zus:
        #N = B*((1 - zus - ch)*(1 - z)) -r_2*((1 - zus - ch)*B - ku - step) - tax_1 + kw
        N = B*(1 - zus - ch)*(1 - z - r_2) + (ku + step)*r_2 - tax_1 + kw
        #N = B*(1 - zus - ch)*(1 - z - r_2) + r_2*step*(1 - zus - ch) - tax_1 + kw
    else:
        #N = (B-limit_zus)*(1 - ch)*(1 - z - r_2) + (ku + step)*r_2
        N = gross_net(limit_zus) + (B - limit_zus)*(1 - ch)*(1 - z - r_2)
    return round(N, 2)

print('netto: ', gross_net(24000)) 
#print('step', gross_net(step))
#print('limit_zus', gross_net(limit_zus))
#print(gross_net(20000*12))

def net_gross(N):
    base = N/(1-r_1) + ku
    B = (N - ku*r_1 - kw) / ((1 - zus - ch)*(1 - z - r_1))
    return round(B, 2)

print('brutto: ', net_gross(17519.32))

print(gross_net(net_gross(20000)))
