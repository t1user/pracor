
emerytalna = 0.0976
rentowa = 0.015
chorobowa = 0.0245
zdrowotna = 0.09
zdrowotna_podatek = 0.0775
koszty_uzyskania_przychodu = 111.25 * 12
kwota_wolna_od_podatku = 556.02
rate_1 = 0.18
rate_2 = 0.32
step = 85528
limit_zus = 127890


def gross_to_net(gross):
    if gross > step:
        pass
        #kwota_wolna_od_podatku = 0
    zus = (emerytalna + rentowa) * min(gross, limit_zus)
    chorobowe = chorobowa * gross
    zus = zus + chorobowe
    podstawa_zdrowotne = gross - zus
    zdrowotne_do_zaplaty = zdrowotna * podstawa_zdrowotne
    zdrowotne_od_podatku = zdrowotna_podatek * podstawa_zdrowotne

    podstawa_PIT = round(gross - koszty_uzyskania_przychodu - zus, 0)
    podstawa_PIT_step_1 = min(podstawa_PIT, step)
    podstawa_PIT_step_2 = max(0, podstawa_PIT - podstawa_PIT_step_1)

    PIT_1 = round(rate_1 * podstawa_PIT_step_1, 0)
    PIT_2 = round(rate_2 * podstawa_PIT_step_2)
    PIT = round(PIT_1 + PIT_2 - kwota_wolna_od_podatku - zdrowotne_od_podatku, 0)

    net = round(gross - zus - zdrowotne_do_zaplaty - PIT, 2)
    print('zus', zus)
    print('chorobowe', chorobowe)
    print('podstawa zdrowotne:', podstawa_zdrowotne)
    print('zdrowotne do zaplaty', zdrowotne_do_zaplaty)
    print('zdrowotne od podatku', zdrowotne_od_podatku)
    print('prog 1', podstawa_PIT_step_1)
    print('prog 2', podstawa_PIT_step_2)
    print('PIT 1', PIT_1, 'PIT 2', PIT_2)
    print('PIT', PIT)    
    return net

print(gross_to_net(2000*12))


def net_to_gross(value):

    numerator = (value - rate_1 * koszty_uzyskania_przychodu + kwota_wolna_od_podatku)
    denominator = 1 - (emerytalna + rentowa) * (1 - zdrowotna_podatek - rate_1 - zdrowotna) - zdrowotna_podatek - rate_1 - zdrowotna + chorobowa * (zdrowotna + zdrowotna_podatek + rate_1)

    gross = numerator / denominator
    print('numerator: ', numerator, ' denominator: ', denominator)
    return gross

#print(net_to_gross(17513))

#print(gross_to_net(net_to_gross(17513)))
