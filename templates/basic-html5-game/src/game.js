// Basic HTML5 Canvas Game Template
// This is a starting point for a simple 2D game

class Game {
    constructor() {
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.score = 0;
        this.scoreElement = document.getElementById('score');
        
        // Game state
        this.isRunning = false;
        this.lastTime = 0;
        
        // Player object
        this.player = {
            x: this.canvas.width / 2,
            y: this.canvas.height / 2,
            width: 30,
            height: 30,
            speed: 200, // pixels per second
            color: '#0f0'
        };
        
        // Input handling
        this.keys = {};
        this.setupInput();
        
        // Start the game
        this.start();
    }
    
    setupInput() {
        // Store event handlers for cleanup
        this.handleKeyDown = (e) => {
            this.keys[e.key.toLowerCase()] = true;
        };
        
        this.handleKeyUp = (e) => {
            this.keys[e.key.toLowerCase()] = false;
        };
        
        window.addEventListener('keydown', this.handleKeyDown);
        window.addEventListener('keyup', this.handleKeyUp);
    }
    
    // Cleanup method to remove event listeners
    destroy() {
        this.isRunning = false;
        window.removeEventListener('keydown', this.handleKeyDown);
        window.removeEventListener('keyup', this.handleKeyUp);
    }
    
    start() {
        this.isRunning = true;
        this.lastTime = performance.now();
        requestAnimationFrame((time) => this.gameLoop(time));
    }
    
    gameLoop(currentTime) {
        if (!this.isRunning) return;
        
        // Calculate delta time in seconds
        const deltaTime = (currentTime - this.lastTime) / 1000;
        this.lastTime = currentTime;
        
        // Update game state
        this.update(deltaTime);
        
        // Render
        this.render();
        
        // Continue the loop
        requestAnimationFrame((time) => this.gameLoop(time));
    }
    
    update(deltaTime) {
        // Handle player movement with normalized diagonal movement
        let moveX = 0;
        let moveY = 0;
        
        if (this.keys['arrowleft'] || this.keys['a']) {
            moveX -= 1;
        }
        if (this.keys['arrowright'] || this.keys['d']) {
            moveX += 1;
        }
        if (this.keys['arrowup'] || this.keys['w']) {
            moveY -= 1;
        }
        if (this.keys['arrowdown'] || this.keys['s']) {
            moveY += 1;
        }
        
        // Normalize diagonal movement to prevent faster diagonal speed
        if (moveX !== 0 && moveY !== 0) {
            const length = Math.sqrt(moveX * moveX + moveY * moveY);
            moveX /= length;
            moveY /= length;
        }
        
        // Apply movement
        this.player.x += moveX * this.player.speed * deltaTime;
        this.player.y += moveY * this.player.speed * deltaTime;
        
        // Keep player in bounds
        this.player.x = Math.max(0, Math.min(this.canvas.width - this.player.width, this.player.x));
        this.player.y = Math.max(0, Math.min(this.canvas.height - this.player.height, this.player.y));
        
        // Add your game logic here
        // - Collision detection
        // - Enemy updates
        // - Scoring
        // - etc.
    }
    
    render() {
        // Clear canvas
        this.ctx.fillStyle = '#000';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw player
        this.ctx.fillStyle = this.player.color;
        this.ctx.fillRect(this.player.x, this.player.y, this.player.width, this.player.height);
        
        // Add your rendering code here
        // - Draw enemies
        // - Draw particles
        // - Draw UI elements
        // - etc.
    }
    
    updateScore(points) {
        this.score += points;
        this.scoreElement.textContent = this.score;
    }
}

// Initialize the game when the page loads
window.addEventListener('load', () => {
    const game = new Game();
});
