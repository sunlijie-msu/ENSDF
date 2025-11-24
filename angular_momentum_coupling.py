import sys
from fractions import Fraction

def calc(target, particle):
    # Parse inputs (e.g., "0+" -> spin="0", parity=1)
    try:
        Jt, pit = Fraction(target[:-1]), 1 if target.endswith('+') else -1
        sp, pip = Fraction(particle[:-1]), 1 if particle.endswith('+') else -1
    except ValueError:
        print("Invalid format. Use e.g., '0+' or '5/2-'")
        return

    print(f"\nTarget: J={Jt} π={'+' if pit>0 else '-'} | Particle: s={sp} π={'+' if pip>0 else '-'}")
    
    # Channel spins S = |Jt - sp| ... Jt + sp
    min_S, max_S = abs(Jt - sp), Jt + sp
    S_values = [min_S + i for i in range(int(max_S - min_S) + 1)]
    
    # Explanation for S
    explanation = f"from |{Jt} - {sp}| to {Jt} + {sp}"
    print(f"Channel Spins S: {', '.join(map(str, S_values))}: {explanation}")
    
    print("-" * 80)
    print(f"{'L':<3} {'Wave':<5} {'Parity':<8} {'s':<5} {'Final Jπ'}")
    print("-" * 80)
    
    waves = {0:'s', 1:'p', 2:'d', 3:'f', 4:'g', 5:'h', 6:'i'}
    
    for l in range(5): # l = 0 to 4
        # Parity selection: pi_f = pi_t * pi_p * (-1)^l
        pif = pit * pip * ((-1)**l)
        parity_str = '+' if pif > 0 else '-'
        
        for S in S_values:
            # Final J = |S - l| ... S + l
            min_J, max_J = abs(S - l), S + l
            current_Js = []
            curr = min_J
            while curr <= max_J:
                current_Js.append(curr)
                curr += 1
            
            Jpi_str = ", ".join(f"{j}{parity_str}" for j in sorted(current_Js))
            
            print(f"{l:<3} {waves.get(l,'?'):<5} {parity_str:<8} {str(S):<5} {Jpi_str}")
        print("-" * 80)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        calc(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python angular_momentum_coupling.py <Target> <Particle>")
        print("Example: python angular_momentum_coupling.py 3/2- 1/2+")
        calc("3/2-", "1/2+")
