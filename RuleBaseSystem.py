class RuleBasedSystem:
    def __init__(self):
        self.facts = set()
        self.rules = []

    def add_rule(self, antecedent, consequent):
        self.rules.append((antecedent, consequent))

    def add_fact(self, fact):
        self.facts.add(fact)

    def evaluate(self, condition):
        if isinstance(condition, list):
            if "OR" in condition:
                left, _, right = condition
                return (left in self.facts) or (right in self.facts)

            if "NOT" in condition:
                _, fact = condition
                return fact not in self.facts

            return all(c in self.facts for c in condition)

        return condition in self.facts

    def forward_chain(self):
        new_fact_found = True
        while new_fact_found:
            new_fact_found = False
            for ante, cons in self.rules:
                if isinstance(ante, list) and not ("OR" in ante or "NOT" in ante):
                    condition_met = all(self.evaluate(c) for c in ante)
                else:
                    condition_met = self.evaluate(ante)

                if condition_met and cons not in self.facts:
                    self.facts.add(cons)
                    new_fact_found = True
                    print(f"Inferred new fact: {cons}")

        print("\nInference complete. Final facts:")
        for fact in self.facts:
            print("-", fact)


if __name__ == "__main__":
    system = RuleBasedSystem()

    system.add_rule("has_fur", "is_mammal")
    system.add_rule("is_mammal", "is_animal")
    system.add_rule(["is_mammal", "eats_meat"], "is_carnivore")
    system.add_rule(["is_mammal", "has_tawny_color", "has_dark_spots"], "is_cheetah")
    system.add_rule(["is_mammal", "has_tawny_color", "has_black_stripes"], "is_tiger")
    system.add_rule(["is_mammal", "has_long_neck", "has_long_legs"], "is_giraffe")


    system.add_fact("has_fur")
    system.add_fact("eats_meat")
    system.add_fact("has_tawny_color")
    system.add_fact("has_black_stripes")

    system.forward_chain()
