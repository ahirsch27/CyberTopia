CyberTopia: Neon Protocol

  CyberTopia: Neon Protocol is a tactical, cyberpunk-themed roguelike battler built in Python using the Pygame engine. 
  Players command "Combat Daemons" to infiltrate corporate mainframes, battle security sentinels, and archive data to 
  level up their kernel in an endless, high-stakes combat loop.

Technical Highlights

This project was built with a focus on Game Feel (Juice) and Data Persistence, utilizing several advanced programming concepts:
  - Dynamic Glitch Engine: Implements a coordinate-offset matrix that triggers screen-shake based on damage intensity, creating
    visceral visual feedback for every "Malware Upload" (attack).
  - Dual-Layer Data Persistence:
      Session Save: Serializes player state (Level, XP, Stats) into save_data.json for persistent progression.
      Global Hall of Fame: Maintains a high_score.json file to track the "Global Best Streak" across all independent sessions.
  - Procedural Animation: Uses trigonometric sine-wave functions ($y = \sin(t) \times \text{amplitude}$) to simulate "breathing" 
  and "hovering" effects for 2D sprites, ensuring the UI feels alive.
  - Finite State Machine (FSM): The game architecture manages transitions between SELECT, BATTLE, and GAME_OVER states to ensure 
  clean logic flow and prevent input conflicts.
  - Scaling Difficulty Algorithm: Enemy "Sentinels" are procedurally generated with stats that scale relative to the player's 
  current level, ensuring a consistent challenge curve.

How to Play

  1. Choose Your Daemon
  Select your starter protocol based on your playstyle:
    GLITCH_CAT: Balanced stats for versatile hacking.
    CYBER_HOUND: High attack velocity, low structural integrity (Glass Cannon).
    NEON_TOAD: Massive HP buffers, lower damage output (The Tank).

  2. Combat Protocol
    [A] Attack: Upload malware to the enemy sentinel.
    [S] Repair: Heal your Daemon once it has low HP
    [R] Reboot: (Only on Game Over) Wipe current save and restart from the selection screen.
    [ESC] Disconnect: Safely close the game and sync your data to the grid.

  3. Leveling & Progression
  Defeating enemies grants 60 XP. Reaching 100 XP triggers a Kernel Upgrade: "Level Up!"
     Max HP increases.
     Attack power increases.
     System Full Restore (HP heal).

Installation & Setup

  Prerequisites
    Python 3.x
    Pygame Library (pip install pygame)

  Setup Instructions
    Clone the Repository:
      git clone [https://github.com/yourusername/cybertopia-neon-protocol.git](https://github.com/yourusername/cybertopia-neon-protocol.git)
      cd cybertopia-neon-protocol
    Add Your Assets:
      Place your .png files in the root folder:
        bg.png: Your neon-city background.
        player.png: Your player daemon sprite.
        enemy.png: The corporate sentinel sprite. 
        (Note: The game will default to procedural grid rendering if images are missing.)
  Run the Game:
    python main.py

File Structure

  main.py: Core game engine and rendering logic.
  save_data.json: Non-volatile memory for player stats. (Note: this is created after initial run.)
  high_score.json: Persistent record of the highest global streak.

Developer Credits

  Developed for JagHacks 2026.
  Developer Note: This project demonstrates the power of Python for rapid prototyping in game development, 
  focusing on responsive UI, data serialization, and mathematical animations.
