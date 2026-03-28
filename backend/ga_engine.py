import random
import copy
from typing import List, Optional, Tuple
from models import Student, RoomConfig, SeatingSeat

class GeneticAlgorithm:
    def __init__(self, students: List[Student], room_config: RoomConfig, 
                 pop_size: int = 50, mutation_rate: float = 0.1, max_generations: int = 100):
        self.students = students
        self.room_config = room_config
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate
        self.max_generations = max_generations
        self.rows = room_config.rows
        self.cols = room_config.cols
        self.total_seats = self.rows * self.cols
        self.num_students = len(students)
        
        # If too many students, we'll only place as many as seats
        if self.num_students > self.total_seats:
            self.students = self.students[:self.total_seats]
            self.num_students = self.total_seats

    def create_individual(self) -> List[Optional[Student]]:
        """Individual is a flat list of size rows*cols containing Student or None."""
        individual = [None] * self.total_seats
        indices = list(range(self.total_seats))
        random.shuffle(indices)
        
        for i, s in enumerate(self.students):
            individual[indices[i]] = s
        return individual

    def calculate_fitness(self, individual: List[Optional[Student]]) -> Tuple[float, int]:
        """
        Fitness score: Higher is better. 
        Penalize for: Same subject students sitting adjacent or diagonally.
        """
        clashes = 0
        grid = [individual[i:i+self.cols] for i in range(0, self.total_seats, self.cols)]
        
        for r in range(self.rows):
            for c in range(self.cols):
                s1 = grid[r][c]
                if s1 is None:
                    continue
                
                # Check neighbors (8-connectivity)
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            s2 = grid[nr][nc]
                            if s2 and s1.subject == s2.subject:
                                clashes += 1
        
        # We want to minimize clashes. Max possible clashes is around 8 * total_seats.
        # fitness = max_clashes - clashes
        # Let's use a simpler inverse:
        fitness = 1000 - clashes 
        return float(max(0, fitness)), clashes // 2 # Divide by 2 as each clash is counted twice

    def crossover(self, parent1: List[Optional[Student]], parent2: List[Optional[Student]]) -> List[Optional[Student]]:
        """Uniform crossover while preserving set of students."""
        # Simple swap-based crossover to maintain student count
        # Step 1: Pick a random range to keep from parent 1
        child = [None] * self.total_seats
        start, end = sorted(random.sample(range(self.total_seats), 2))
        
        # Copy from parent 1
        for i in range(start, end):
            child[i] = parent1[i]
            
        # Fill remaining with parent 2, avoiding duplicates
        # But wait, same students exist in both parents. We need to maintain the exact student list.
        # Better approach: OX (Order Crossover) variant for seating.
        # Actually, let's use a simpler approach:
        # 1. Randomly pick seats from parent1.
        # 2. Fill the rest by looking at parent2 and picking students not yet placed.
        
        placed_student_ids = {s.id for s in child if s}
        p2_idx = 0
        for i in range(self.total_seats):
            if child[i] is None:
                # Find next student in parent2 not yet placed
                while p2_idx < self.total_seats:
                    s = parent2[p2_idx]
                    p2_idx += 1
                    if s and s.id not in placed_student_ids:
                        child[i] = s
                        placed_student_ids.add(s.id)
                        break
        return child

    def mutate(self, individual: List[Optional[Student]]):
        """Swap two random seats."""
        if random.random() < self.mutation_rate:
            i, j = random.sample(range(self.total_seats), 2)
            individual[i], individual[j] = individual[j], individual[i]

    def run(self):
        population = [self.create_individual() for _ in range(self.pop_size)]
        fitness_history = []
        best_overall = None
        best_fitness_overall = -1
        min_clashes_overall = 99999
        
        for gen in range(self.max_generations):
            # Evaluate
            scores = [self.calculate_fitness(ind) for ind in population]
            fitnesses = [s[0] for s in scores]
            clashes_list = [s[1] for s in scores]
            
            gen_best_fitness = max(fitnesses)
            fitness_history.append(gen_best_fitness)
            
            # Keep track of best
            best_idx = fitnesses.index(gen_best_fitness)
            if gen_best_fitness > best_fitness_overall:
                best_fitness_overall = gen_best_fitness
                best_overall = copy.deepcopy(population[best_idx])
                min_clashes_overall = clashes_list[best_idx]
            
            # Selection & Reproduce
            new_population = [best_overall] # Elitism
            
            while len(new_population) < self.pop_size:
                # Tournament Selection
                p1 = self.tournament_select(population, fitnesses)
                p2 = self.tournament_select(population, fitnesses)
                
                child = self.crossover(p1, p2)
                self.mutate(child)
                new_population.append(child)
                
            population = new_population
            
        # Convert flat best to SeatingSeat list
        final_seating = []
        for i, student in enumerate(best_overall):
            final_seating.append(SeatingSeat(
                row=i // self.cols,
                col=i % self.cols,
                student=student
            ))
            
        return final_seating, fitness_history, min_clashes_overall

    def tournament_select(self, population, fitnesses, k=3):
        indices = random.sample(range(len(population)), k)
        best_idx = max(indices, key=lambda i: fitnesses[i])
        return population[best_idx]
