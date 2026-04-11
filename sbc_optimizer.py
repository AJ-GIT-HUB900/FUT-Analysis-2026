import itertools
import math

def calculate_sbc_rating(ratings):
    """
    Calculates the EA FC squad rating using the community formula.
    """
    if len(ratings) != 11:
        return 0
        
    # Step 1: Find the true average
    base_avg = sum(ratings) / 11
    
    # Step 2: Calculate the "bonus" for players rated higher than the average
    correction_factor = sum((r - base_avg) for r in ratings if r > base_avg)
    
    # Step 3: Add the rounded down average to the rounded down bonus
    final_rating = math.floor(base_avg) + math.floor(correction_factor / 11)
    return final_rating

def find_cheapest_combinations(target_rating, available_ratings):
    print(f"Finding combinations for an {target_rating}-rated squad...")
    
    valid_combinations = []
    
    # itertools creates every single possible 11-card combination 
    # using the ratings we provide (82, 83, 84, etc.)
    all_possible_combos = itertools.combinations_with_replacement(available_ratings, 11)
    
    for combo in all_possible_combos:
        # Check if this combination hits our target
        if calculate_sbc_rating(combo) == target_rating:
            # Sort it so it looks pretty, and add it to our list
            valid_combinations.append(sorted(combo, reverse=True))
    
    # We only want to show a few examples, not thousands!
    print(f"\nFound {len(valid_combinations)} valid ways to build an {target_rating} squad.")
    print("Here are 5 example combinations:")
    
    for i in range(min(5, len(valid_combinations))):
        print(f"Option {i+1}: {valid_combinations[i]}")

if __name__ == "__main__":
    # Let's say we have fodder ranging from 82 to 86 in our club
    my_fodder_ratings = [82, 83, 84, 85, 86]
    
    # We want to complete an 84-rated SBC
    find_cheapest_combinations(target_rating=84, available_ratings=my_fodder_ratings)
