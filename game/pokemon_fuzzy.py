import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def calculate_prob(level_input, effect_input):
    # definição universo
    diff_levels = ctrl.Antecedent(np.arange(-20, 21, 5), 'diff_levels') 
    attack_effect = ctrl.Antecedent(np.arange(0, 4.1, 1.0), 'attack_effect') 
    prob_win = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'prob_win') 

    # funções de pertença
        #diff_levels
    diff_levels['low'] = np.array([
        1.0,  # -20
        0.8,  # -15
        0.6,  # -10
        0.3,  # -5
        0.0,  # 0
        0.0,  # 5
        0.0,  # 10
        0.0,  # 15
        0.0   # 20
    ])

    diff_levels['medium'] = np.array([
        0.0,  # -20
        0.2,  # -15
        0.5,  # -10
        0.8,  # -5
        1.0,  # 0
        0.8,  # 5
        0.5,  # 10
        0.2,  # 15
        0.0   # 20
    ])

    diff_levels['high'] = np.array([
        0.0,  # -20
        0.0,  # -15
        0.0,  # -10
        0.0,  # -5
        0.0,  # 0
        0.3,  # 5
        0.6,  # 10
        0.8,  # 15
        1.0   # 20
    ])
        #attack_effect
    attack_effect['inef'] = np.array([
        1.0,  # 0.0
        0.5,  # 1.0
        0.0,  # 2.0
        0.0,  # 3.0
        0.0   # 4.0
    ])

    attack_effect['norm'] = np.array([
        0.0,  # 0.0
        0.5,  # 1.0
        1.0,  # 2.0
        0.5,  # 3.0
        0.0   # 4.0
    ])

    attack_effect['eff'] = np.array([
        0.0,  # 0.0
        0.0,  # 1.0
        0.3,  # 2.0
        0.7,  # 3.0
        1.0   # 4.0
    ])
        #prob_win
    prob_win['vlow'] = np.array([
        1.0,  # 0.0
        0.7,  # 0.1
        0.3,  # 0.2
        0.0,  # 0.3
        0.0,  # 0.4
        0.0,  # 0.5
        0.0,  # 0.6
        0.0,  # 0.7
        0.0,  # 0.8
        0.0,  # 0.9
        0.0   # 1.0
    ])

    prob_win['low'] = np.array([
        0.3,  # 0.0
        0.6,  # 0.1
        1.0,  # 0.2
        0.6,  # 0.3
        0.3,  # 0.4
        0.0,  # 0.5
        0.0,  # 0.6
        0.0,  # 0.7
        0.0,  # 0.8
        0.0,  # 0.9
        0.0   # 1.0
    ])

    prob_win['med'] = np.array([
        0.0,  # 0.0
        0.0,  # 0.1
        0.3,  # 0.2
        0.6,  # 0.3
        1.0,  # 0.4
        0.6,  # 0.5
        0.3,  # 0.6
        0.0,  # 0.7
        0.0,  # 0.8
        0.0,  # 0.9
        0.0   # 1.0
    ])

    prob_win['high'] = np.array([
        0.0,  # 0.0
        0.0,  # 0.1
        0.0,  # 0.2
        0.0,  # 0.3
        0.0,  # 0.4
        0.3,  # 0.5
        0.6,  # 0.6
        1.0,  # 0.7
        0.6,  # 0.8
        0.3,  # 0.9
        0.0   # 1.0
    ])

    prob_win['vhigh'] = np.array([
        0.0,  # 0.0
        0.0,  # 0.1
        0.0,  # 0.2
        0.0,  # 0.3
        0.0,  # 0.4
        0.0,  # 0.5
        0.0,  # 0.6
        0.3,  # 0.7
        0.7,  # 0.8
        1.0,  # 0.9
        1.0   # 1.0
    ])

    # definição regras
    rules = [
        ctrl.Rule(diff_levels['low'] & attack_effect['inef'], prob_win['vlow']),
        ctrl.Rule(diff_levels['low'] & attack_effect['norm'], prob_win['low']),
        ctrl.Rule(diff_levels['low'] & attack_effect['eff'], prob_win['med']),
        ctrl.Rule(diff_levels['medium'] & attack_effect['inef'], prob_win['low']),
        ctrl.Rule(diff_levels['medium'] & attack_effect['norm'], prob_win['med']),
        ctrl.Rule(diff_levels['medium'] & attack_effect['eff'], prob_win['high']),
        ctrl.Rule(diff_levels['high'] & attack_effect['inef'], prob_win['med']),
        ctrl.Rule(diff_levels['high'] & attack_effect['norm'], prob_win['high']),
        ctrl.Rule(diff_levels['high'] & attack_effect['eff'], prob_win['vhigh'])
    ]

    # passo 1: valor de verdade das proposições atómicas
    l_pos = np.where(diff_levels.universe == level_input)[0][0]
    e_pos = np.where(attack_effect.universe == effect_input)[0][0]

    mu_l_lo = diff_levels['low'].mf[l_pos]
    mu_l_md = diff_levels['medium'].mf[l_pos]
    mu_l_hi = diff_levels['high'].mf[l_pos]
    mu_e_in = attack_effect['inef'].mf[e_pos]
    mu_e_no = attack_effect['norm'].mf[e_pos]
    mu_e_ef = attack_effect['eff'].mf[e_pos]

    # passo 2: determinação dos valores de verdade das condições lógicas, através do método min
    rule1_and = min(mu_l_lo, mu_e_in)
    rule2_and = min(mu_l_lo, mu_e_no)
    rule3_and = min(mu_l_lo, mu_e_ef)
    rule4_and = min(mu_l_md, mu_e_in)
    rule5_and = min(mu_l_md, mu_e_no)
    rule6_and = min(mu_l_md, mu_e_ef)
    rule7_and = min(mu_l_hi, mu_e_in)
    rule8_and = min(mu_l_hi, mu_e_no)
    rule9_and = min(mu_l_hi, mu_e_ef)

    # passo 3: determinação das contribuições das regras, através do método shrink
    act1 = np.minimum(rule1_and, prob_win['vlow'].mf)
    act2 = np.minimum(rule2_and, prob_win['low'].mf)
    act3 = np.minimum(rule3_and, prob_win['med'].mf)
    act4 = np.minimum(rule4_and, prob_win['low'].mf)
    act5 = np.minimum(rule5_and, prob_win['med'].mf)
    act6 = np.minimum(rule6_and, prob_win['high'].mf)
    act7 = np.minimum(rule7_and, prob_win['med'].mf)
    act8 = np.minimum(rule8_and, prob_win['high'].mf)
    act9 = np.minimum(rule9_and, prob_win['vhigh'].mf)

    # passo 4: else-link, através do método OR-link
    aggregated = np.maximum(act1, np.maximum(act2, np.maximum(act3, 
                 np.maximum(act4, np.maximum(act5, np.maximum(act6, 
                 np.maximum(act7, np.maximum(act8, act9))))))))

    # passo 5: desfuzzification

    #para prevenir erro de divisão por zero
    if np.sum(aggregated) == 0: return 0.5

    prob_output = fuzz.defuzz(
        prob_win.universe, 
        aggregated, 
        "centroid"
    )
    
    return prob_output
