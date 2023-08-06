# Requierements
import pandas as pd
import numpy as np
from numpy import arange
import time
import random

import os

import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import RandomForestRegressor

from sdv.tabular import CopulaGAN, GaussianCopula
from sdv.constraints import FixedCombinations
from sdv.metrics.tabular import BNLikelihood, BNLogLikelihood, GMLogLikelihood, LogisticDetection, SVCDetection, MLPRegressor
from sdv.evaluation import evaluate
from sdv.metrics.relational import KSComplement

class split_data:
    '''
    split_data contains a single function that splits a DataFrame into train and test sets. 

    '''

    def __init__(self, df: pd.DataFrame, train_size: float, x_column_names: list, y_column_name):
        self.df = df
        self.train_size = train_size
        self.df = df
        self.x_column_names = x_column_names
        self.y_column_name = y_column_name

    def split_train_test(self):

        '''
        Split a DataFrame into train and test sets in order to create a model. 

        df: DataFrame to be entered
        train_size: size of the training set
        x_column_names: List of predictor variable names.
        y_column_name: Name of the predictor variable. 

        '''
        X = self.df[self.x_column_names].values
        y = self.df[self.y_column_name].values
        train = self.df.sample(int(len(self.df) * self.train_size))
        test = self.df[~self.df.index.isin(train.index)]
        return train, test



class RLGeneticAlgorithm(split_data):
    '''
    RLGeneticAlgorithm contains 11 functions which, when combined, build a single-objective genetic algorithm created to identify the distributions of the variables. 
    
    '''

    def __init__(self, df: pd.DataFrame, tournament_size_per: float, max_generations: int, population_size: int,  verbose_model: bool, train_size: float, x_column_names: list, y_column_name: list, train: pd.DataFrame, test: pd.DataFrame, augmentation_method : str):
        super().__init__(df, train_size, x_column_names, y_column_name)
        self.total_inds = {}
        self.tournament_size_per = tournament_size_per
        self.max_generations = max_generations
        self.population_size = population_size
        self.solutions_list = []
        self.generation = 0
        self.verbose_model = verbose_model
        self.train = train
        self.test = test
        self.df = df
        self.augmentation_method = augmentation_method


    def funcion_individuo(self, df: pd.DataFrame):
        '''
        Generates an individual by randomly selecting a distribution for each variable

        df: Dataframe to be entered

        '''
        columns = df.columns.tolist()
        distributions = [random.choice(
            ['gamma', 'student_t', 'beta', 'gaussian', 'gaussian_kde', 'truncated_gaussian']) for k in range(0, len(columns))]
        return distributions


    def funcion_poblacion(self, tamaño_poblacion: int, df: pd.DataFrame):
        '''
        Generates a population of N individuals

        population_size: Size of the population that will be created.
        df: DataFrame to be inserted

        '''
        poblacion = []
        for k in range(0, tamaño_poblacion):
            poblacion.append(self.funcion_individuo(df))
        return poblacion


    def funcion_fitness(self, individuo: list):

        '''
        Calculation of the fitness for an individual. Being Fitness the prediction metric generated through the prediction generated with the synthesized data.  
        
        individual: Individual for whom the fitness is calculated. 

        '''

        imbalanced_class = self.df[self.y_column_name].value_counts().sort_values().reset_index()['index'][0]
        imbalance_df = self.df[self.df[self.y_column_name] == imbalanced_class]
        a = zip(imbalance_df.columns.tolist(), individuo)
        distribution_dic = dict(a)

        if self.augmentation_method == 'Gan': 
            model = CopulaGAN(field_distributions=distribution_dic)
        else:          
            model = GaussianCopula(field_distributions=distribution_dic)
        
        model.fit(imbalance_df)
        new_data = model.sample(num_rows=len(imbalance_df))
        train_mas_new_data = pd.concat([self.train, new_data], axis=0)
        fitness = MLPRegressor.normalize(MLPRegressor.compute(
            self.test, train_mas_new_data, target=self.y_column_name))
        return fitness


    def funcion_fitness_poblacion(self, poblacion: list[list]):
        '''
        Calculate the fitness for a complete population. 

        population: population for which the fitness is calculated.  

        '''
        fitness_poblacion = []
        for k in poblacion:
            fitness_poblacion.append(self.funcion_fitness(k))
        return fitness_poblacion


    def funcion_rank_poblacion(self, poblacion: list[list], fitness_poblacion: list[float]):
        '''
        
        Sorts a population in descending order according to the fitness of the individuals that compose it. 

        population: Population to sort. 
        fitness_population: Fitness of the population to sort. 
        
        '''
        df = pd.DataFrame(
            {'poblacion': poblacion, 'fitness': fitness_poblacion})
        df = df.sort_values('fitness', ascending=False)
        return df.poblacion.to_list(), df.fitness.tolist()


    def funcion_crossover(self, parent1: list, parent2: list):
        '''
        Generates a crossover between two individuals. Randomly selects a type if n-point crossover. 

        parent1: First individual used to generate the crossover. 
        parent2: Second individual used to generate the crossover. 

        '''
        crossover_type = random.choice([1, 2, 3, 4])
        numbers = list(arange(5))
        positions = [random.choice(range(0, 5))]
        numbers.remove(positions[0])
        positions.append(random.choice(numbers))
        numbers.remove(positions[1])
        positions.append(random.choice(numbers))

        last = max(positions)
        first = min(positions)
        positions.remove(last)
        positions.remove(first)
        middle = positions[0]

        if crossover_type == 1:  # 3-point crossover
            child1, child2 = parent1[:first] + parent2[first:middle] + parent1[middle:last] + \
                parent2[last:], parent2[:first] + parent1[first:middle] + \
                parent2[middle:last] + parent1[last:]
        if crossover_type == 2:  # 2-point crossover
            child1, child2 = parent1[:first] + parent2[first:last] + \
                parent1[last:], parent2[:first] + \
                parent2[first:last] + parent2[last:]
        if crossover_type == 3:  # swap fist part
            child1, child2 = parent1[:first] + \
                parent2[first:], parent2[:first] + parent2[first:]
        if crossover_type == 4:  # swap last part
            child1, child2 = parent1[:last] + \
                parent2[last:], parent2[:last] + parent1[last:]
        return child1, child2



    def funcion_mutation(self, individuo: list):
        '''
        Performs a mutation on an individual. It randomly selects N variables and modifies their defined distribution. 

        individual: Individual to which the mutation will be generated. 

        '''
        numero_mutaciones = round(random.uniform(1, 3))
        posiciones_mutaciones = [round(random.uniform(
            0, len(individuo)-1)) for k in range(0, numero_mutaciones)]
        for k in posiciones_mutaciones:
            individuo[k] = random.choice(
                ['gamma', 'student_t', 'beta', 'gaussian', 'gaussian_kde', 'truncated_gaussian'])
        return individuo


    def funcion_tournament_selection(self, rank_poblacion: list[list]):
        '''
        Selects an individual to be the parent in the crossover operator. 

        rank_population: Population sorted according to the fitness of the individuals. 

        '''
        tournament_size = max(
            1, int(len(rank_poblacion) * self.tournament_size_per))
        random_pos = sorted(random.sample(
            range(len(rank_poblacion)), tournament_size))
        return rank_poblacion[random_pos[0]]


    def funcion_replacement(self, rank_poblacion: list[list], rank_fitness: list[int], pop_size: int):
        '''
        Selects the individuals of a population that become part of the next generation. 

        rank_population: Population ordered according to the fitness of the individuals. 
        rank_fitness: Ranked fitness of the population. 
        pop_size: Proportion of the population that we select for the next generation. 

        '''
        return rank_poblacion[:pop_size], rank_fitness[:pop_size]


    def create_next_generation(self, population: list[list], cross_prob: float = 1.0, mut_prob: float = .1, elitism: bool = True, elite_proportion: float = .1):
        '''
        Combining the above functions generates the following population: 

        population: Initial population 
        cross_prob: Probability of a crossover between two selected individuals.  
        mut_pron: Probability that an individual will mutate. 
        elitism: Defines if there is elitism or not. 
        elite_proportion: In case of elitism, the proportion of elitism. 
        
        '''
        fitness_population = self.funcion_fitness_poblacion(
            poblacion=population)
        ranked_pop, ranked_fit = self.funcion_rank_poblacion(
            poblacion=population, fitness_poblacion=fitness_population)

        if elitism:
            elite_size = max(1, int(len(population)*elite_proportion))
            elite = ranked_pop[:elite_size]
            fitness_elite = ranked_fit[:elite_size]
            no_elite = ranked_pop[elite_size:]
            fitness_noelite = ranked_fit[elite_size:]
        else:
            elite_size = 0
            no_elite = population
            fitness_noelite = ranked_fit

        new_population = []
        while len(new_population) < len(no_elite):
            parent1 = self.funcion_tournament_selection(
                rank_poblacion=ranked_pop)
            parent2 = self.funcion_tournament_selection(
                rank_poblacion=ranked_pop)
            cross = random.random() <= cross_prob
            mut = random.random() <= mut_prob
            if cross:
                child1, child2 = self.funcion_crossover(
                    parent1=parent1, parent2=parent2)
            if mut:
                child1 = self.funcion_mutation(individuo=child1)
                child2 = self.funcion_mutation(individuo=child2)

            new_population.append(child1)
            new_population.append(child2)

        new_population_fitness = self.funcion_fitness_poblacion(
            poblacion=new_population)
        new_population_ranked, new_population_fitness = self.funcion_rank_poblacion(
            poblacion=no_elite + new_population, fitness_poblacion=fitness_noelite + new_population_fitness)
        final_new_population, final_new_fitness = self.funcion_replacement(
            rank_poblacion=new_population_ranked, rank_fitness=new_population_fitness, pop_size=self.population_size-elite_size)

        if elitism:
            next_population = elite + final_new_population
            next_population_fitness = fitness_elite + final_new_fitness
        else:
            next_population = final_new_population
            next_population_fitness = final_new_fitness

        return next_population, next_population_fitness

    def run(self, df: pd.DataFrame, cross_prob: float = 1.0, mut_prob: float = .1, elitism: bool = True, elite_proportion: float = .1, population: list = None) -> None:
        '''
        Starts the genetic algorithm. 
        
        df: DataFrame to be inserted. 
        population: Initial population 
        cross_prob: Probability of a crossover between two selected individuals.  
        mut_pron: Probability that an individual is going to mutate. 
        elitism: Defines if there is elitism or not. 
        elite_proportion: In case of elitism, the proportion of elitism. 

        '''
        if population is None:
            population = self.funcion_poblacion(
                tamaño_poblacion=self.population_size, df=self.df)
        while self.generation < self.max_generations:
            try:
                start_gen = time.perf_counter()
                print(f'Generation: {self.generation}')

                if self.verbose_model:
                    print(f'Generation: {self.generation}')
                    population, pop_fit = self.create_next_generation(
                        population=population, cross_prob=cross_prob, mut_prob=mut_prob, elitism=elitism, elite_proportion=elite_proportion)
                    end_gen = time.perf_counter()
                    print(
                        f'Total time generation: {end_gen - start_gen}. Best overall fitness is: {max(pop_fit)}')
                    print(
                        '----------------------------------------------------------------------\n')
                else:
                    population, pop_fit = self.create_next_generation(
                        population=population, cross_prob=cross_prob, mut_prob=mut_prob, elitism=elitism, elite_proportion=elite_proportion)
                    end_gen = time.perf_counter()

                population_array, pop_fit_array = np.array(
                    population), np.array(pop_fit).reshape(-1, 1)
                solution_array = np.concatenate(
                    (population_array, pop_fit_array), axis=1)
                self.solutions_list.append(solution_array.tolist())
                self.generation += 1
            except KeyboardInterrupt:
                exit_signal = input(
                    'Exit signal requested, are you sure you want to stop the program? [y]/n')
                while not exit_signal in ['y', 'n', '', 'q']:
                    exit_signal = input(
                        'Exit signal requested, are you sure you want to stop the program? [y]/n: ')
                if exit_signal in ['y', '', 'q']:
                    print(
                        'Confirmed exit signal. Stopping program and saving results...')
                    self.generation = np.inf
                else:
                    print(
                        f'Exit signal rejected, re-running execution of generation {self.generation}.')
                continue
        if self.generation == self.max_generations:
            return population, pop_fit


class data_augmentation(RLGeneticAlgorithm):
    '''
    data_augmentation generates synthetic data using Gaussian and Gan copulas. It allso allows to compare differences between the original data and the synthesized data. 

    '''
    
    def __init__(self, df: pd.DataFrame, tournament_size_per: float, max_generations: int, population_size: int,  verbose_model: bool, train_size: float,
                 x_column_names: list, y_column_name: list, train: pd.DataFrame, test: pd.DataFrame, distribution: list, augmentation_method : str):
        super().__init__(df, x_column_names, y_column_name, tournament_size_per,
                         max_generations, population_size,  verbose_model, train_size, train, test, augmentation_method)
        self.total_inds = {}
        self.tournament_size_per = tournament_size_per
        self.max_generations = max_generations
        self.population_size = population_size
        self.solutions_list = []
        self.generation = 0
        self.verbose_model = verbose_model
        self.train = train
        self.test = test
        self.df = df
        self.train_size = train_size
        self.x_column_names = x_column_names
        self.y_column_name = y_column_name
        self.distribution = distribution
        self.augmentation_method = augmentation_method

    def CopulaGAN_augmentation(self):
        '''
        Generates de data augmentation. 

        '''
        list_of_distribution = zip(self.df.columns.tolist(), self.distribution)
        distribution_dic = dict(list_of_distribution)
        if self.augmentation_method == 'Gan': 
            model = CopulaGAN(field_distributions=distribution_dic)
        else:          
            model = GaussianCopula(field_distributions=distribution_dic)
        model.fit(self.df)
        new_data = model.sample(num_rows=len(self.df))
        X = self.df[self.x_column_names].values
        y = self.df[self.y_column_name].values
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, random_state=1)
        train = self.df.sample(int(len(self.df) * self.train_size))
        test = self.df[~self.df.index.isin(train.index)]
        train_mas_new_data = pd.concat([train, new_data], axis=0)

        # MLPRegressor
        print('MLPRegressor')
        print('Predict original data with synthetic data:', MLPRegressor.normalize(
            MLPRegressor.compute(self.df, new_data, target=self.y_column_name)))
        print('Predict original data with a combination of original and synthetic data:', MLPRegressor.normalize(
            MLPRegressor.compute(test, train_mas_new_data, target=self.y_column_name)))
        print('Predict data using only original data:', MLPRegressor.normalize(
            MLPRegressor.compute(test, train, target=self.y_column_name)))

        return new_data

    def plot_new_data_vs_original_data_h(self, new_data):
        '''
        Visualizes the difference between the original and synthetic data by means of histograms. 

        new_data: Synthetic data. 
        '''

        if self.df.shape[1] % 2 == 0:
            nrows = round(self.df.shape[1] / 2)
            ncols = round(self.df.shape[1] / 2)
        else:
            nrows = round(self.df.shape[1] / 2)
            ncols = (round(self.df.shape[1] / 2)) + 1

        paleta = ['#457b9d', '#1d3557']
        fig, ax = plt.subplots(nrows, ncols, figsize=(20, 7))
        ax = ax.ravel()
        i = 0
        for k in self.df.columns:
            try:
                new_data[k].plot(kind='hist', ax=ax[i],
                                 label='New data', color=paleta[0], alpha=0.5)
                self.df[k].plot(kind='hist', ax=ax[i],
                                label='Original Data', color=paleta[1], alpha=0.5)
                ax[i].legend()
                ax[i].set_title(k)

            except:
                new_data[k].plot(kind='hist', ax=ax[i],
                                 label='New data', color=paleta[0])
                self.df[k].plot(kind='hist', ax=ax[i],
                                label='Original Data', color=paleta[1])
                ax[i].legend()
                ax[i].set_title(k)
            i += 1
        fig.suptitle(
            'Historam: New data using CopulaGAN vs Original data')
        fig.show()



    def plot_new_data_vs_original_data_d(self, new_data):

        '''
        Visualize the difference between the original and synthetic data by means of density plots. 

        new_data: Synthetic data. 
        
        '''
        
        if self.df.shape[1] % 2 == 0:
            nrows = round(self.df.shape[1] / 2)
            ncols = round(self.df.shape[1] / 2)
        else:
            nrows = round(self.df.shape[1] / 2)
            ncols = (round(self.df.shape[1] / 2)) + 1

        paleta = ['#457b9d', '#1d3557']
        fig, ax = plt.subplots(nrows, ncols, figsize=(20, 7))
        ax = ax.ravel()
        i = 0
        for k in self.df.columns:
            try:
                new_data[k].plot(kind='density', ax=ax[i],
                                 label='New data', color=paleta[0], alpha=0.5)
                self.df[k].plot(kind='density', ax=ax[i],
                                label='Original Data', color=paleta[1], alpha=0.5)
                ax[i].legend()
                ax[i].set_title(k)

            except:
                new_data[k].plot(kind='hist', ax=ax[i],
                                 label='New data', color=paleta[0])
                self.df[k].plot(kind='hist', ax=ax[i],
                                label='Original Data', color=paleta[1])
                ax[i].legend()
                ax[i].set_title(k)
            i += 1
        fig.suptitle(
            'Density: New data using Copula GAN vs Original data')
        fig.show()