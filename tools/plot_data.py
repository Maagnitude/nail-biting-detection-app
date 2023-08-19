import matplotlib.pyplot as plt
import csv

class PlotData():
    
    def __init__(self):
        self.time_stamps = []
        self.biting_durations = []
    
    
    def plot_data(self, hand_in_mouth_region):
        if self.biting_durations.__len__() > 0 and self.time_stamps.__len__() > 0 and not hand_in_mouth_region:
            # Displaying the timestamp/nail-biting count chart
            plt.clf()
            plt.plot(self.time_stamps, self.biting_durations, marker='o')
            plt.xlabel('Time')
            plt.ylabel('Biting Duration')
            plt.title('Nail Biting Detection Chart')
            plt.xticks(rotation=45)
            plt.tight_layout()
            # Show the chart in a separate window
            plt.pause(0.01)
        
            # Save data to CSV
            with open("nail_biting_data.csv", "w", newline="") as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(["Time", "Biting Durations"])
                for t, count in zip(self.time_stamps, self.biting_durations):
                    csv_writer.writerow([t, count])