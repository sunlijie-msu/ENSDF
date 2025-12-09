import sys
from fractions import Fraction

def calc(target, particle):
    """
    Calculates allowed final angular momenta (J) and parity (π) 
    by coupling a target nucleus with a particle and orbital angular momentum L.
    
    Selection Rules:
    1. Channel Spin S: |Jt - sp| <= S <= Jt + sp
    2. Final Spin J: |S - L| <= J <= S + L
    3. Parity: πf = πt * πp * (-1)^L
    """
    
    # Parse inputs (e.g., "0+" -> spin="0", parity=1)
    try:
        if not (target.endswith('+') or target.endswith('-')):
             raise ValueError("Target parity missing (use + or - at end)")
        if not (particle.endswith('+') or particle.endswith('-')):
             raise ValueError("Particle parity missing (use + or - at end)")

        Jt = Fraction(target[:-1])
        pit = 1 if target.endswith('+') else -1
        
        sp = Fraction(particle[:-1])
        pip = 1 if particle.endswith('+') else -1
    except ValueError as e:
        print(f"Error parsing input: {e}")
        print("Usage example: python angular_momentum_coupling.py 3/2- 1/2+")
        return

    print(f"\nTarget: J={Jt} π={'+' if pit>0 else '-'} | Particle: s={sp} π={'+' if pip>0 else '-'}")
    
    # Channel spins S = |Jt - sp| ... Jt + sp
    min_S = abs(Jt - sp)
    max_S = Jt + sp
    
    # Generate S values (step is 1)
    S_values = []
    curr_S = min_S
    while curr_S <= max_S:
        S_values.append(curr_S)
        curr_S += 1
    
    # Explanation for S
    explanation = f"from |{Jt} - {sp}| to {Jt} + {sp}"
    print(f"Channel Spins S: {', '.join(map(str, S_values))} ({explanation})")
    
    # Table Header
    # Requested Order: Wave, L, s, Jπ
    print("-" * 70)
    print(f"{'Wave':<6} {'L':<4} {'s':<6} {'Final Jπ'}")
    print("-" * 70)
    
    # Orbital angular momentum L from 0 to 6 (s to i)
    waves = {0:'s', 1:'p', 2:'d', 3:'f', 4:'g', 5:'h', 6:'i'}
    
    for l in range(7): # l = 0 to 6
        wave_name = waves.get(l, '?')
        
        # Parity selection: pi_f = pi_t * pi_p * (-1)^l
        pif = pit * pip * ((-1)**l)
        parity_str = '+' if pif > 0 else '-'
        
        for S in S_values:
            # Final J = |S - l| ... S + l
            min_J = abs(S - l)
            max_J = S + l
            
            current_Js = []
            curr = min_J
            while curr <= max_J:
                current_Js.append(curr)
                curr += 1
            
            # Format J values with parity
            Jpi_list = [f"{j}{parity_str}" for j in sorted(current_Js)]
            Jpi_str = ", ".join(Jpi_list)
            
            print(f"{wave_name:<6} {l:<4} {str(S):<6} {Jpi_str}")
        
        # Separator between L groups
        print("-" * 70)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        calc(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python angular_momentum_coupling.py <Target> <Particle>")
        print("Example: python angular_momentum_coupling.py 3/2- 1/2+")
        # Default example run for demonstration
        calc("3/2-", "1/2+")
