class RuleBasedSystem:
    def __init__(self):
        self.facts = set()
        self.rules = []
    
    def add_rule(self, antecedent, consequent):
        self.rules.append((antecedent, consequent))
    
    def add_fact(self, fact):
        self.facts.add(fact)
    
    def evaluate_condition(self, condition):
        if isinstance(condition, str):
            return condition in self.facts
        elif isinstance(condition, list):
            if "OR" in condition:
                or_index = condition.index("OR")
                left = condition[:or_index]
                right = condition[or_index + 1:]
                left_result = self.evaluate_condition(left[0]) if len(left) == 1 else self.evaluate_condition(left)
                right_result = self.evaluate_condition(right[0]) if len(right) == 1 else self.evaluate_condition(right)
                return left_result or right_result
            else:
                return all(self.evaluate_condition(item) for item in condition)
        return False
    
    def forward_chain(self):
        new_fact_found = True
        iteration = 0
        
        print("\nStarting inference process...")
        print(f"Initial facts: {sorted(self.facts)}")
        
        while new_fact_found and iteration < 100:
            new_fact_found = False
            iteration += 1
            
            for ante, cons in self.rules:
                if self.evaluate_condition(ante) and cons not in self.facts:
                    self.facts.add(cons)
                    new_fact_found = True
                    print(f"Inferred new fact: {cons}")
        
        print("\nInference complete. Final facts:")
        for fact in sorted(self.facts):
            print(f" - {fact}")

def interactive_demo():
    system = RuleBasedSystem()
    
    system.add_rule("has_fur", "is_mammal")
    system.add_rule("has_feathers", "is_bird")
    system.add_rule(['is_mammal', "eats_meat"], "is_carnivore")
    system.add_rule(['is_carnivore', "has_tawny_color", "has_dark_spots"], "is_cheetah")
    system.add_rule(['is_carnivore', "has_tawny_color", "has_black_stripes"], "is_tiger")
    system.add_rule('is_bird', "is_animal")
    system.add_rule('is_mammal', "is_animal")
    system.add_rule(["has_wings", "OR", "can_fly"], "can_fly_creature")
    system.add_rule(["has_feathers", "OR", "has_wings"], "is_bird")

    print("RULE-BASED INFERENCE SYSTEM")
    
    while True:
        system.facts.clear()
        
        print("\nEnter simple facts about an animal:")
        print("Examples: has_fur, eats_meat, has_tawny_color, has_dark_spots")
        print("Press Enter twice when finished")
        print("-" * 40)
        
        fact_count = 0
        while True:
            fact = input("Enter fact: ").strip()
            if not fact:
                if fact_count == 0:
                    print("Please enter at least one fact")
                    continue
                else:
                    break
            
            system.add_fact(fact)
            fact_count += 1
            print(f"  Added: {fact}")
        
        print("\n" + "="*40)
        print("RUNNING INFERENCE...")
        print("="*40)
        
        system.forward_chain()
        
        while True:
            response = input("\nIdentify another animal? (y/n): ").strip().lower()
            if response in ['y', 'yes']:
                break
            elif response in ['n', 'no']:
                print("Goodbye!")
                return
            else:
                print("Please enter 'y' or 'n'")

if __name__ == "__main__":
    interactive_demo()