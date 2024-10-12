# Flappy Bird AI with NEAT and Genetic Algorithm

This project showcases the power of **Genetic Algorithms** combined with the **NEAT (NeuroEvolution of Augmenting Topologies)** algorithm to teach an AI how to play the game of Flappy Bird. Over generations, the AI evolves to improve its ability to pass through pipes by making smarter decisions.

## Key Features

- **NEAT Algorithm:** The AI uses the NEAT algorithm to evolve neural networks that control the bird's movement. NEAT allows the structure of the neural networks to grow and change over time, optimizing both the topology and weights of the network.
  
- **Genetic Algorithm:** This project is powered by a genetic algorithm, simulating the process of natural selection. Over multiple generations, the AI learns by keeping the "fittest" birds and allowing them to pass on their traits through mutation and crossover, improving their performance with each iteration.

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
    - Place the bird, pipe, base, and background images in a folder called `imgs` within the project directory. Make sure the files are named:
      - `bird1.png`
      - `bird2.png`
      - `bird3.png`
      - `pipe.png`
      - `base.png`
      - `bg.png`

4. Run the project:

    ```bash
    python main.py
    ```

## How It Works

- **NEAT & Genetic Algorithm:** This project uses NEAT, a genetic algorithm designed to evolve neural networks. The AI birds learn to play Flappy Bird by receiving feedback on their fitness (how far they progress in the game). NEAT evolves these networks by simulating natural selection, favoring birds that survive longer and make smarter decisions.

- **Fitness Function:** Birds are rewarded for staying alive and successfully passing through pipes. Those with the highest fitness scores survive to pass on their traits to the next generation, with occasional mutations introduced to improve performance.

## Configuring NEAT

The `config-feedforward.txt` file contains all the configurations for NEAT, including population size, mutation rates, and other parameters. You can tweak these settings to see how they affect the AI's learning process.

## Credits

This project is based on the **Python Flappy Bird AI Tutorial** created by **Tech with Tim** on YouTube.

You can watch the tutorial series here: [Python Flappy Bird AI Tutorial (with NEAT)](https://www.youtube.com/watch?v=OGHA-elMrxI).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
