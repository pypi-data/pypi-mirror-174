import pandas as pd
import numpy as np
from numpy import arange
import random
from cv2 import fitEllipse
import time

import matplotlib.pyplot as plt

from sdv.tabular import GaussianCopula, CopulaGAN
from sdv.metrics.tabular import LogisticDetection, SVCDetection
from sdv.metrics.relational import KSComplement
from sdv.constraints import FixedCombinations
from sdv.evaluation import evaluate
from sdv.metrics.tabular import MLPRegressor

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import load_iris


# Configuración warnings
import warnings
warnings.filterwarnings('ignore')

# Trabajo
class split_data():
    '''
    El objetivo de esta clase es particionar datos para conseguir un mejor entrenamiento y testeo de los futuros modelos a realizar. 
    Esta clase nos devuelve el conjunto de datos para entrenamiento y el mismo para testeo a partir del dataframe original.
    Elementos:
        df: dataframe desbalanceado
        train_size: tamaño del conjunto de entrenamiento
        x_column_names: nombres de las columnas predictoras
        y_column_name: nombre de la columna a predecir
    '''
    def __init__(self, df: pd.DataFrame, train_size: float, x_column_names: list, y_column_name):
        self.df = df
        self.train_size = train_size
        self.df = df
        self.x_column_names = x_column_names
        self.y_column_name = y_column_name
    
    def split_train_test(self):
        X = self.df[self.x_column_names].values
        y = self.df[self.y_column_name].values
        train = self.df.sample(int(len(self.df) * self.train_size))
        test = self.df[~self.df.index.isin(train.index)]
        return train, test  

class RLGeneticAlgorithm(split_data):
    '''
    Esta clase hereda de la anterior y, tiene como objetivo optimizar una lista de las distribuciones de las variables. 
    Para ello, se hace uso de un algoritmo genético mono objetivo.
    Elementos:
        df: 
            dataframe desbalanceado
        tournament_size_per: 
            El método de selección por torneos es una forma de elegir un invididuo de la población. Este método hace "torneos" 
            entre una serie de individuos elegidos aleatoriamente de la población. El ganador de los torneos será el seleccionado
             para haer un crossover.
            Cuando este parámetro es pequeño, el método nos da la oportunidad de seleccionar a todos los individuos para ser 
            seleccionados y esto hace que la diversidad se mantenga, aunque puede que el costo computacional sea mayor.
        max_generations: 
            Este parámetro define el número máximo de iteraciones, es decir, el número de veces que el proceso se va a repetir.
        population_size:
            Número de individuos que van a conformar la población.
        verbose_model:
            False: El modelo no devuelve información en cada generación.
            True: El modelo devuelve información en cada generación.
        train_size: 
            Tamaño el conjunto de entrenamiento.
        x_column_names:
            Nombres de las columnas predictoras.
        y_column_name:
            Nombres de las columnas a predecir.
        train:
            Conjunto de entrenamiento.
        test:
            Conjunto para probar los resultados. Se predice sobre este conjunto.
    '''
    def __init__(self, df: pd.DataFrame, tournament_size_per: float, max_generations: 5, population_size: 10,  verbose_model: bool, train_size: float, 
    x_column_names: list , y_column_name: list, train: pd.DataFrame, test: pd.DataFrame):
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

    @property
    def max_generations(self):
        return self.__max_generations

    @max_generations.setter
    def max_generations(self, max_generations):
        self.__max_generations = max_generations

    def funcion_individuo(self, df: pd.DataFrame): 
        columns = df.columns.tolist()
        distributions = [random.choice(['gamma','student_t','beta','gaussian']) for k in range(0,len(columns))]
        return distributions

    def funcion_poblacion(self, tamaño_poblacion: int, df: pd.DataFrame):
        poblacion = []
        for k in range(0,tamaño_poblacion):
            poblacion.append(self.funcion_individuo(df))
        return poblacion

    def funcion_fitness(self, individuo: list):
        # Filtramos la clase
        imbalanced_class = self.df[self.y_column_name].value_counts().sort_values().reset_index()['index'][0]
        imbalance_df = self.df[self.df[self.y_column_name] == imbalanced_class]
        a = zip(imbalance_df.columns.tolist(), individuo)
        distribution_dic = dict(a)
        model = GaussianCopula(field_distributions=distribution_dic)
        model.fit(imbalance_df)
        new_data = model.sample(num_rows=len(imbalance_df))

        # Unimos los datos
        train_mas_new_data = pd.concat([self.train, new_data], axis = 0)
        fitness = MLPRegressor.normalize(MLPRegressor.compute(self.test, train_mas_new_data, target= self.y_column_name ))
        return fitness

    def funcion_fitness_poblacion(self, poblacion: list[list]):
        fitness_poblacion = []
        for k in poblacion:
            fitness_poblacion.append(self.funcion_fitness(k))
        return fitness_poblacion

    def funcion_rank_poblacion(self, poblacion: list[list], fitness_poblacion:list[float]):
        df = pd.DataFrame({'poblacion':poblacion, 'fitness':fitness_poblacion})
        df = df.sort_values('fitness', ascending=False)
        return df.poblacion.to_list(), df.fitness.tolist()

    def funcion_crossover(self, parent1:list , parent2: list):
        crossover_type = random.choice([1,2,3,4])
        numbers = list(arange(5))
        positions = [random.choice(range(0,5))]
        numbers.remove(positions[0])
        positions.append(random.choice(numbers))
        numbers.remove(positions[1])
        positions.append(random.choice(numbers))

        last = max(positions)
        first = min(positions)
        positions.remove(last)
        positions.remove(first)
        middle = positions[0]

        if crossover_type == 1: #3-point crossover
            child1, child2 = parent1[:first] + parent2[first:middle] + parent1[middle:last] + parent2[last:] , parent2[:first] + parent1[first:middle] + parent2[middle:last] + parent1[last:]
        if crossover_type == 2: #2-point crossover
            child1, child2 = parent1[:first] + parent2[first:last] + parent1[last:]  , parent2[:first] + parent2[first:last] + parent2[last:] 
        if crossover_type ==3: #swap fist part
            child1, child2 = parent1[:first] + parent2[first:] , parent2[:first] + parent2[first:] 
        if crossover_type == 4: #swap last part
            child1, child2 = parent1[:last] + parent2[last:] , parent2[:last] + parent1[last:]
        return child1, child2    

    def funcion_mutation(self, individuo: list):
        numero_mutaciones = round(random.uniform(1,3))
        posiciones_mutaciones = [round(random.uniform(0,len(individuo)-1)) for k in range(0,numero_mutaciones)]
        for k in posiciones_mutaciones:
            individuo[k] = random.choice(['gamma','student_t','beta','gaussian'])
        return individuo 

    def funcion_tournament_selection(self, rank_poblacion: list[list]):
        tournament_size = max(1, int(len(rank_poblacion) * self.tournament_size_per))
        random_pos = sorted(random.sample(range(len(rank_poblacion)), tournament_size))
        return rank_poblacion[random_pos[0]]

    def funcion_replacement(self, rank_poblacion: list[list], rank_fitness: list[int], pop_size: int):
        return rank_poblacion[:pop_size] , rank_fitness[:pop_size]


    def create_next_generation(self, population: list[list], cross_prob: float=1.0, mut_prob: float=.1, elitism: bool=True, elite_proportion: float=.1):
        fitness_population = self.funcion_fitness_poblacion(poblacion=population)
        ranked_pop, ranked_fit = self.funcion_rank_poblacion(poblacion=population, fitness_poblacion=fitness_population)

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
            parent1 = self.funcion_tournament_selection(rank_poblacion=ranked_pop)
            parent2 = self.funcion_tournament_selection(rank_poblacion=ranked_pop)
            cross = random.random() <= cross_prob
            mut = random.random() <= mut_prob
            if cross:
                child1, child2 = self.funcion_crossover(parent1=parent1, parent2=parent2)
            if mut:
                child1 = self.funcion_mutation(individuo = child1)
                child2 = self.funcion_mutation(individuo = child2)

            new_population.append(child1)
            new_population.append(child2)

        new_population_fitness = self.funcion_fitness_poblacion(poblacion=new_population)
        new_population_ranked, new_population_fitness = self.funcion_rank_poblacion(poblacion=no_elite + new_population, fitness_poblacion = fitness_noelite + new_population_fitness)
        final_new_population, final_new_fitness = self.funcion_replacement(rank_poblacion= new_population_ranked, rank_fitness=new_population_fitness, pop_size=self.population_size-elite_size)

        if elitism:
            next_population = elite + final_new_population
            next_population_fitness = fitness_elite + final_new_fitness
        else:
            next_population = final_new_population
            next_population_fitness = final_new_fitness

        return next_population, next_population_fitness


    def run(self, df: pd.DataFrame, cross_prob: float=1.0, mut_prob: float=.1, elitism: bool=True, elite_proportion: float=.1, population: list=None) -> None:
        if population is None: 
            population = self.funcion_poblacion(tamaño_poblacion=self.population_size, df=self.df)
        while self.generation < self.max_generations:
            try: 
                start_gen = time.perf_counter()

                if self.verbose_model:
                    print(f'Generation: {self.generation}')
                    population, pop_fit = self.create_next_generation(population=population, cross_prob=cross_prob, mut_prob=mut_prob, elitism=elitism, elite_proportion=elite_proportion)
                    end_gen = time.perf_counter()
                    print(f'Total time generation: {end_gen - start_gen}. Best overall fitness is: {max(pop_fit)}')
                    print('----------------------------------------------------------------------\n')
                else:
                    population, pop_fit = self.create_next_generation(population=population, cross_prob=cross_prob, mut_prob=mut_prob, elitism=elitism, elite_proportion=elite_proportion)
                    end_gen = time.perf_counter()

                population_array, pop_fit_array = np.array(population), np.array(pop_fit).reshape(-1, 1)
                solution_array = np.concatenate((population_array, pop_fit_array), axis = 1)
                self.solutions_list.append(solution_array.tolist())
                self.generation += 1
            except KeyboardInterrupt:
                exit_signal = input('Exit signal requested, are you sure you want to stop the program? [y]/n')
                while not exit_signal in ['y', 'n', '', 'q']:
                    exit_signal = input('Exit signal requested, are you sure you want to stop the program? [y]/n: ')
                if exit_signal in ['y', '', 'q']:
                    print('Confirmed exit signal. Stopping program and saving results...')
                    self.generation = np.inf 
                else: 
                    print(f'Exit signal rejected, re-running execution of generation {self.generation}.')
                continue
        if self.generation == self.max_generations: 
            return population, pop_fit

class data_augmentation(RLGeneticAlgorithm):
    def __init__(self, df: pd.DataFrame, tournament_size_per: float, max_generations: int, population_size: int,  verbose_model: bool, train_size: float, 
    x_column_names: list , y_column_name: list, train: pd.DataFrame, test: pd.DataFrame, distribution: list):
        super().__init__(df, x_column_names, y_column_name, tournament_size_per, max_generations, population_size,  verbose_model, train_size, train, test)
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

    
    def GaussianCopula_augmentation(self):
        list_of_distribution = zip(self.df.columns.tolist(), self.distribution)
        distribution_dic = dict(list_of_distribution)
        model = GaussianCopula(field_distributions= distribution_dic)
        model.fit(self.df)
        new_data = model.sample(num_rows=len(self.df))
        X = self.df[self.x_column_names].values
        y = self.df[self.y_column_name].values
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
        train = self.df.sample(int(len(self.df) * self.train_size))
        test = self.df[~self.df.index.isin(train.index)]
        train_mas_new_data = pd.concat([train, new_data], axis = 0)

        # MLPRegressor
        print('MLPRegressor')
        print('Predict original data with synthetic data:', MLPRegressor.normalize(MLPRegressor.compute(self.df, new_data, target=self.y_column_name)))
        print('Predict original data with a combination of original and synthetic data:', MLPRegressor.normalize(MLPRegressor.compute(test, train_mas_new_data, target=self.y_column_name)))
        print('Predict data using only original data:', MLPRegressor.normalize(MLPRegressor.compute(test, train, target=self.y_column_name)))

        return new_data    

    def plot_new_data_vs_original_data(self, new_data):
        if self.df.shape[1] % 2 == 0:
            nrows = round(self.df.shape[1] / 2)
            ncols = round(self.df.shape[1] / 2)
        else: 
            nrows = round(self.df.shape[1] / 2)
            ncols = (round(self.df.shape[1] / 2)) + 1

        paleta = ['#457b9d', '#1d3557']
        fig, ax = plt.subplots(nrows, ncols, figsize = (20,7))
        ax = ax.ravel()
        i = 0
        for k in self.df.columns:
                try: 
                        new_data[k].plot(kind='hist', ax = ax[i], label = 'New data', color = paleta[0], alpha = 0.5)                
                        self.df[k].plot(kind='hist', ax = ax[i], label = 'Original Data', color = paleta[1], alpha = 0.5)
                        ax[i].legend()
                        ax[i].set_title(k)
                        
                except: 
                        new_data[k].plot(kind='hist', ax = ax[i], label = 'New data', color = paleta[0])                
                        self.df[k].plot(kind='hist', ax = ax[i], label = 'Original Data', color = paleta[1])
                        ax[i].legend()
                        ax[i].set_title(k)
                i += 1
        fig.suptitle('Density: New data using Gaussian Copula vs Original data')
        fig.show()