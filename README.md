# Flappy Bird with AI

A Python implementation of Flappy Bird featuring both player-controlled and AI-powered gameplay using the NEAT (NeuroEvolution of Augmenting Topologies) algorithm.

## Description

This project contains two versions of Flappy Bird:
1. **Player Version**: A classic implementation where you control the bird using keyboard inputs
2. **AI Version**: An AI-powered version where birds learn to play the game using the NEAT algorithm

## Features

- Classic Flappy Bird gameplay mechanics
- Smooth bird animations and physics
- Score tracking
- Infinite procedurally generated pipes
- Neural network visualization (AI version)
- Generation tracking (AI version)

## Requirements

- Python 3.x
- Pygame
- NEAT-Python

Install the required packages using: `pip install neat-python pygame`

## Project Structure
flappy-bird/
├── flappy_player.py # Player-controlled version
├── flappy_AI.py # AI-powered version
├── config-feedforward.txt # NEAT configuration file
└── images/
├── bird1.png
├── bird2.png
├── bird3.png
├── base.png
├── pipe.png
└── bg.png

## How to Play

### Player Version
1. Run `python flappy_player.py`
2. Press any key to make the bird jump
3. Navigate through pipes without hitting them
4. Score increases as you pass through pipes
5. Game ends if you hit a pipe or the ground

### AI Version
1. Run `python flappy_AI.py`
2. Watch as the AI learns to play through multiple generations
3. Each generation improves upon the last using the NEAT algorithm
4. The display shows current generation and score

## NEAT Algorithm

The AI version uses the NEAT algorithm which:
- Creates a population of birds with random neural networks
- Each bird's fitness is evaluated based on survival time and pipes passed
- The best performing birds are selected for breeding
- New generations inherit and mutate traits from successful parents
- Over time, the AI learns optimal playing strategies

## Controls

### Player Version
- Any key: Make bird jump
- Close window to exit

### AI Version
- Close window to stop training
- Watch as birds evolve automatically

## Credits

This implementation is based on the classic Flappy Bird game, with added AI capabilities using the NEAT-Python library.

## License

This project is open source and available under the MIT License.