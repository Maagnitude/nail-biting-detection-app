from tools.sound_controller import SoundController

class Reward():
    
    def __init__(self):  
        self.reward_intervals = {
            10: "Nail Biting Rookie",   # 10 seconds without biting
            20: "Biting Avoider",       # 20 seconds without biting
            30: "Iron finger",          # 30 seconds without biting
            40: "Nail Guardian"         # 40 seconds without biting
        }
        self.reward_sounds = {
            "Nail Biting Rookie": "resources/rookie.mp3",
            "Biting Avoider": "resources/avoider.mp3",
            "Iron finger": "resources/iron_finger.mp3",
            "Nail Guardian": "resources/guardian.mp3"
        }  
        self.earned_rewards = []
        
    
    def check_for_rewards(self, time_since_last_bite):
        sound_controller = SoundController()
        for interval, reward in self.reward_intervals.items():
            if time_since_last_bite >= interval and reward not in self.earned_rewards and not sound_controller.is_playing():
                self.earned_rewards.append(reward)
                # Print the reward and play a sound
                print(f"Congratulations! You earned the reward: {reward}")
                sound_controller.play_sound(self.reward_sounds[reward])