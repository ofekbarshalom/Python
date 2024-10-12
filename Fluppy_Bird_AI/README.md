# Flappy Bird AI with NEAT and Genetic Algorithm

This project demonstrates the use of **Genetic Algorithms** and the **NEAT (NeuroEvolution of Augmenting Topologies)** algorithm to evolve an AI that plays Flappy Bird. The AI learns to improve its gameplay over generations through evolution.

## Key Features

- **NEAT Algorithm:** The AI is powered by NEAT, which evolves neural networks by optimizing both their structure and their weights over time.
  
- **Genetic Algorithm:** The project uses a genetic algorithm to simulate natural selection, where the fittest birds are selected to reproduce and pass on their traits to the next generation, improving with each iteration.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-repo/flappy-bird-neat.git
    ```

2. Install the required dependencies:

    ```bash
    pip install pygame neat-python
    ```

3. Add the necessary image files:
    - Create a folder named `imgs` in the project directory and place the following files inside it:
      - `bird1.png`
      - `bird2.png`
      - `bird3.png`
      - `pipe.png`
      - `base.png`
      - `bg.png`

4. Ensure that the **NEAT configuration file** is present. You should have a `config-feedforward.txt` file that contains the NEAT algorithm's parameters.

    Ensure you have this file saved as `config-feedforward.txt` in the same directory as your Python code.

5. Run the project:

    ```bash
    python main.py
    ```

## How It Works

- **Genetic Algorithm & NEAT:** The project employs the NEAT algorithm, which evolves neural networks by adapting both the network's topology and connection weights. The fitness function rewards birds for staying alive longer and successfully passing through pipes. Over time, only the best-performing birds are kept, and their traits are passed on to the next generation.

- **Fitness Function:** Birds earn fitness points for surviving longer and passing through pipes. The fittest birds are selected for the next generation, with mutations introduced to improve performance.

- **NEAT Configuration:** The project uses the `config-feedforward.txt` file to configure how the NEAT algorithm runs. This file includes parameters such as population size, mutation rates, and network structure.

## Configuring NEAT

If you want to tweak the NEAT algorithm, you can modify the settings in the `config-feedforward.txt` file. Some key parameters include:
- **Population Size:** Determines how many birds are simulated in each generation.
- **Mutation Rates:** Controls how frequently mutations occur during the evolution process.
- **Fitness Threshold:** The required fitness level for the algorithm to consider the problem solved.

## Credits

This project is based on the **Python Flappy Bird AI Tutorial** created by **Tech with Tim**. You can watch the tutorial series here: [Python Flappy Bird AI Tutorial (with NEAT)](https://www.youtube.com/watch?v=OGHA-elMrxI).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
