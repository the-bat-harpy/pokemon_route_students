import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

'''
Cria um sistema Fuzzy que recebe como input a diferença dos niveis
e o efeito do ataque e devolve como input a probabilidade de ganhar
'''
def calculate_prob(level_input, effect_input):
    
#definição universo diferença níveis
    diff_levels = ctrl.Antecedent(np.arange(-20, 21, 1), 'diff_levels')
#definição universo efeito do ataque
    attack_effect = ctrl.Antecedent(np.arange(0, 4.1, 0.1), 'attack_effect')
#definição universo probabilidade de ganhar
    prob_win = ctrl.Consequent(np.arange(0, 1.01, 0.01), "prob_win")
    
#funções de pertença diferença níveis
    diff_levels['low'] = fuzz.trimf(diff_levels.universe, [-20, -20, 0])
    diff_levels['medium'] = fuzz.trimf(diff_levels.universe, [-5, 0, 5])
    diff_levels['high'] = fuzz.trimf(diff_levels.universe, [0, 20, 20])
    
#funções de pertença efeito ataque
    attack_effect['ineffective'] = fuzz.trimf(attack_effect.universe, [0, 0, 1])
    attack_effect['normal'] = fuzz.trimf(attack_effect.universe, [0.5, 1, 2])
    attack_effect['effective'] = fuzz.trimf(attack_effect.universe, [1, 4, 4])

#funções de pertença probabilidade ganhar

    prob_win['very_low'] = fuzz.trimf(prob_win.universe, [0, 0, 0.3])
    prob_win['low'] = fuzz.trimf(prob_win.universe, [0.1, 0.3, 0.5])
    prob_win['medium'] = fuzz.trimf(prob_win.universe, [0.3, 0.5, 0.7])
    prob_win['high'] = fuzz.trimf(prob_win.universe, [0.5, 0.7, 0.9])
    prob_win['very_high'] = fuzz.trimf(prob_win.universe, [0.7, 1, 1])

   #regras
    rules = [
        # (diff_levels is low AND attack_effect is ineffective) then prob_win is very_low
        ctrl.Rule(diff_levels['low'] & attack_effect['ineffective'], prob_win['very_low']),
        
        # (diff_levels is low AND attack_effect is normal) then prob_win is low
        ctrl.Rule(diff_levels['low'] & attack_effect['normal'], prob_win['low']),
        
        # (diff_levels is low AND attack_effect is effective) then prob_win is medium
        ctrl.Rule(diff_levels['low'] & attack_effect['effective'], prob_win['medium']),

        # (diff_levels is medium AND attack_effect is ineffective) then prob_win is low
        ctrl.Rule(diff_levels['medium'] & attack_effect['ineffective'], prob_win['low']),
        
        # (diff_levels is medium AND attack_effect is normal) then prob_win is medium
        ctrl.Rule(diff_levels['medium'] & attack_effect['normal'], prob_win['medium']),
        
        # (diff_levels is medium AND attack_effect is effective) then prob_win is high
        ctrl.Rule(diff_levels['medium'] & attack_effect['effective'], prob_win['high']),

        # (diff_levels is high AND attack_effect is ineffective) then prob_win is medium
        ctrl.Rule(diff_levels['high'] & attack_effect['ineffective'], prob_win['medium']),
        
        # (diff_levels is high AND attack_effect is normal) then prob_win is high
        ctrl.Rule(diff_levels['high'] & attack_effect['normal'], prob_win['high']),
        
        # (diff_levels is high AND attack_effect is effective) then prob_win is very_high
        ctrl.Rule(diff_levels['high'] & attack_effect['effective'], prob_win['very_high'])
    ]

    # 4. Control System Simulation
    prob_ctrl = ctrl.ControlSystem(rules)
    simulation = ctrl.ControlSystemSimulation(prob_ctrl)

    simulation.input['diff_levels'] = level_input
    simulation.input['attack_effect'] = effect_input
    
    # Computation (Defuzzification)
    try:
        simulation.compute()
        result = simulation.output['prob_win']
    except:
        # Fallback value if inputs are out of bounds
        result = 0.5
    
    return result

    ###
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def calculate_prob(level_input, effect_input):
    # --- DEFINIÇÃO DOS UNIVERSOS ---
    diff_levels = ctrl.Antecedent(np.arange(-20, 21, 1), 'diff_levels')
    attack_effect = ctrl.Antecedent(np.arange(0, 4.1, 0.1), 'attack_effect')
    prob_win = ctrl.Consequent(np.arange(0, 1.01, 0.01), "prob_win")
    
    # --- FUNÇÕES DE PERTENÇA ---
    diff_levels['low'] = fuzz.trimf(diff_levels.universe, [-20, -20, 0])
    diff_levels['medium'] = fuzz.trimf(diff_levels.universe, [-5, 0, 5])
    diff_levels['high'] = fuzz.trimf(diff_levels.universe, [0, 20, 20])
    
    attack_effect['ineffective'] = fuzz.trimf(attack_effect.universe, [0, 0, 1])
    attack_effect['normal'] = fuzz.trimf(attack_effect.universe, [0.5, 1, 2])
    attack_effect['effective'] = fuzz.trimf(attack_effect.universe, [1, 4, 4])

    prob_win['very_low'] = fuzz.trimf(prob_win.universe, [0, 0, 0.3])
    prob_win['low'] = fuzz.trimf(prob_win.universe, [0.1, 0.3, 0.5])
    prob_win['medium'] = fuzz.trimf(prob_win.universe, [0.3, 0.5, 0.7])
    prob_win['high'] = fuzz.trimf(prob_win.universe, [0.5, 0.7, 0.9])
    prob_win['very_high'] = fuzz.trimf(prob_win.universe, [0.7, 1, 1])

    # --- PASSO 1: Fuzzificação (Valor de verdade das proposições) ---
    # Encontrar os graus de pertença para os inputs atuais
    l_low = fuzz.interp_membership(diff_levels.universe, diff_levels['low'].mf, level_input)
    l_med = fuzz.interp_membership(diff_levels.universe, diff_levels['medium'].mf, level_input)
    l_high = fuzz.interp_membership(diff_levels.universe, diff_levels['high'].mf, level_input)

    e_inef = fuzz.interp_membership(attack_effect.universe, attack_effect['ineffective'].mf, effect_input)
    e_norm = fuzz.interp_membership(attack_effect.universe, attack_effect['normal'].mf, effect_input)
    e_eff = fuzz.interp_membership(attack_effect.universe, attack_effect['effective'].mf, effect_input)

    # --- PASSO 2 e 3: Ativação das Regras (Inferência de Mamdani) ---
    # Calculamos o AND (mínimo) e aplicamos ao consequente (mínimo/shrink)
    
    # Regras para Nível Baixo
    r1_act = np.minimum(min(l_low, e_inef), prob_win['very_low'].mf)
    r2_act = np.minimum(min(l_low, e_norm), prob_win['low'].mf)
    r3_act = np.minimum(min(l_low, e_eff), prob_win['medium'].mf)

    # Regras para Nível Médio
    r4_act = np.minimum(min(l_med, e_inef), prob_win['low'].mf)
    r5_act = np.minimum(min(l_med, e_norm), prob_win['medium'].mf)
    r6_act = np.minimum(min(l_med, e_eff), prob_win['high'].mf)

    # Regras para Nível Alto
    r7_act = np.minimum(min(l_high, e_inef), prob_win['medium'].mf)
    r8_act = np.minimum(min(l_high, e_norm), prob_win['high'].mf)
    r9_act = np.minimum(min(l_high, e_eff), prob_win['very_high'].mf)

    # --- PASSO 4: Agregação (Else-link / OR-link) ---
    # Usamos o máximo para agregar todas as áreas resultantes
    aggregated = np.fmax(r1_act, 
                 np.fmax(r2_act, 
                 np.fmax(r3_act, 
                 np.fmax(r4_act, 
                 np.fmax(r5_act, 
                 np.fmax(r6_act, 
                 np.fmax(r7_act, 
                 np.fmax(r8_act, r9_act))))))))

    # --- PASSO 5: Desfuzzificação ---
    # Se a área agregada for zero (nenhuma regra ativada), retorna 0.5 por defeito
    if np.sum(aggregated) == 0:
        return 0.5

    result = fuzz.defuzz(prob_win.universe, aggregated, 'centroid')
    
    return result
###-