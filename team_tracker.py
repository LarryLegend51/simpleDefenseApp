import tkinter as tk
from tkinter import simpledialog
import tkinter.messagebox as messagebox
import csv
import os

#Get name of team
user_name = ""

def get_user_name():
    global user_name
    while not user_name:
        user_name = simpledialog.askstring("Enter Name", "Please enter opponent team name:")
        if not user_name:
            messagebox.showwarning("Invalid Input", "Name cannot be empty. Please try again.")
#GUI
root = tk.Tk()
root.title("Basketball Stats Tracker")
root.geometry("400x600")

defense_type = tk.StringVar(value="Zone")
play_result = tk.StringVar(value="Make")

#Dictonary
stats = {
    "possessions_zone": 0, "FG_att_zone": 0, "FG_makes_zone": 0, "points_zone": 0,
    "turnovers_zone": 0, "FT_att_zone": 0, "FT_makes_zone": 0, "ThreeFG_att_zone": 0,
    "ThreeFG_makes_zone": 0, "TwoFG_att_zone": 0, "TwoFG_makes_zone": 0,
    "possessions_man": 0, "FG_att_man": 0, "FG_makes_man": 0, "points_man": 0,
    "turnovers_man": 0, "FT_att_man": 0, "FT_makes_man": 0, "ThreeFG_att_man": 0,
    "ThreeFG_makes_man": 0, "TwoFG_att_man": 0, "TwoFG_makes_man": 0,
}

stats_display = tk.StringVar()

frame1 = tk.Frame(root, padx=10, pady=10)
frame1.pack(fill="x")
tk.Label(frame1, text="Defense Type:").pack(anchor="w")

defense_radio_zone = tk.Radiobutton(frame1, text="Zone", variable=defense_type, value="Zone")
defense_radio_zone.pack(anchor="w")
defense_radio_man = tk.Radiobutton(frame1, text="Man", variable=defense_type, value="Man")
defense_radio_man.pack(anchor="w")

frame2 = tk.Frame(root, padx=10, pady=10)
frame2.pack(fill="x")
tk.Label(frame2, text="Play Result:").pack(anchor="w")

play_radio_make = tk.Radiobutton(frame2, text="Make", variable=play_result, value="Make")
play_radio_make.pack(anchor="w")
play_radio_miss = tk.Radiobutton(frame2, text="Miss", variable=play_result, value="Miss")
play_radio_miss.pack(anchor="w")
play_radio_foul = tk.Radiobutton(frame2, text="Foul", variable=play_result, value="Foul")
play_radio_foul.pack(anchor="w")
play_radio_turnover = tk.Radiobutton(frame2, text="Turnover", variable=play_result, value="Turnover")
play_radio_turnover.pack(anchor="w")

frame3 = tk.Frame(root, padx=10, pady=10)
frame3.pack(fill="x")

submit_button = tk.Button(frame3, text="Submit Play",
                          command=lambda: submit_play(defense_type.get(), play_result.get()))
submit_button.pack(side="left", padx=5)

report_button = tk.Button(frame3, text="Generate Report", command=lambda: generate_report())
report_button.pack(side="right", padx=5)

frame4 = tk.Frame(root, padx=10, pady=10)
frame4.pack(fill="both", expand=True)
stats_label = tk.Label(frame4, textvariable=stats_display, anchor="nw", justify="left", wraplength=350)
stats_label.pack(fill="both", expand=True)

#Input
def submit_play(defense, result):
    '''Enters Data'''
    if defense == "Zone":
        stats_prefix = "zone"
    else:
        stats_prefix = "man"

    stats[f"possessions_{stats_prefix}"] += 1

    if result == "Make":
        points = simpledialog.askinteger("Points Scored", "Points scored (2 or 3):", minvalue=2, maxvalue=3)
        if points is not None:
            stats[f"FG_makes_{stats_prefix}"] += 1
            stats[f"FG_att_{stats_prefix}"] += 1
            stats[f"points_{stats_prefix}"] += points
            if points == 3:
                stats[f"ThreeFG_makes_{stats_prefix}"] += 1
                stats[f"ThreeFG_att_{stats_prefix}"] += 1
            else:
                stats[f"TwoFG_makes_{stats_prefix}"] += 1
                stats[f"TwoFG_att_{stats_prefix}"] += 1

        messagebox.showinfo("Made Shot Recorded", "The made shot has been recorded.")
    elif result == "Miss":
        stats[f"FG_att_{stats_prefix}"] += 1
        shot_type = simpledialog.askstring("Shot Type", "Missed shot (2 or 3):")
        if shot_type == '2':
            stats[f"TwoFG_att_{stats_prefix}"] += 1
        elif shot_type == '3':
            stats[f"ThreeFG_att_{stats_prefix}"] += 1
        else:
            messagebox.showwarning("Invalid Input", "Please enter '2' for a 2-point shot or '3' for a 3-point shot.")
            return

        messagebox.showinfo("Shot Missed", "The missed shot has been recorded.")
    elif result == "Foul":
        FT_att = simpledialog.askinteger("Free Throws Attempted", "Free throws attempted:", minvalue=1, maxvalue=3)
        FT_makes = simpledialog.askinteger("Free Throws Made", "Free throws made:", minvalue=0, maxvalue=FT_att)
        if FT_att is not None and FT_makes is not None:
            stats[f"FT_att_{stats_prefix}"] += FT_att
            stats[f"FT_makes_{stats_prefix}"] += FT_makes
            stats[f"points_{stats_prefix}"] += FT_makes
        messagebox.showinfo("Free Throws Recorded", "The Free Throws have been recorded.")
    elif result == "Turnover":
        stats[f"turnovers_{stats_prefix}"] += 1
        messagebox.showinfo("Turnover Recorded", "The turnover has been recorded.")

def save_stats_to_csv(ts_percentage_zone, efg_percentage_zone, ts_percentage_man, efg_percentage_man):
    '''Saves stats to CSV file named basketball_stats.csv'''
    global user_name
    # Convert to actual percentages
    ts_percentage_zone *= 100
    efg_percentage_zone *= 100
    ts_percentage_man *= 100
    efg_percentage_man *= 100
    data = [
        user_name,
        int(stats["possessions_zone"]), int(stats["FG_att_zone"]), int(stats["FG_makes_zone"]),
        int(stats["points_zone"]), int(stats["turnovers_zone"]), int(stats["FT_att_zone"]),
        int(stats["FT_makes_zone"]), int(stats["ThreeFG_att_zone"]), int(stats["ThreeFG_makes_zone"]),
        int(stats["TwoFG_att_zone"]), int(stats["TwoFG_makes_zone"]),
        ts_percentage_zone, efg_percentage_zone,
        int(stats["possessions_man"]), int(stats["FG_att_man"]), int(stats["FG_makes_man"]),
        int(stats["points_man"]), int(stats["turnovers_man"]), int(stats["FT_att_man"]),
        int(stats["FT_makes_man"]), int(stats["ThreeFG_att_man"]), int(stats["ThreeFG_makes_man"]),
        int(stats["TwoFG_att_man"]), int(stats["TwoFG_makes_man"]),
        ts_percentage_man, efg_percentage_man
    ]

    file_path = 'basketball_stats.csv'
    try:
        if not os.path.exists(file_path):
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    "Team", "Possessions Zone", "FG Att Zone", "FG Makes Zone", "Points Zone", "Turnovers Zone",
                    "FT Att Zone", "FT Makes Zone", "3PT Att Zone", "3PT Makes Zone", "2PT Att Zone", "2PT Makes Zone",
                    "TS % Zone", "EFG % Zone", "Possessions Man", "FG Att Man", "FG Makes Man", "Points Man",
                    "Turnovers Man", "FT Att Man", "FT Makes Man", "3PT Att Man", "3PT Makes Man", "2PT Att Man",
                    "2PT Makes Man", "TS % Man", "EFG % Man"
                ])
        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)


        messagebox.showinfo("Success", "Data saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving the data: {e}")


def generate_report():
    '''When clicked it gives you the stats as well as saves the underlying #'s to a CSV'''
    total_FG_att_zone = stats["FG_att_zone"]
    total_FG_makes_zone = stats["FG_makes_zone"]
    total_points_zone = stats["points_zone"]
    total_FT_att_zone = stats["FT_att_zone"]
    total_turnovers_zone = stats["turnovers_zone"]
    total_3pt_att_zone = stats["ThreeFG_att_zone"]
    total_3pt_makes_zone = stats["ThreeFG_makes_zone"]

    total_FG_att_man = stats["FG_att_man"]
    total_FG_makes_man = stats["FG_makes_man"]
    total_points_man = stats["points_man"]
    total_FT_att_man = stats["FT_att_man"]
    total_turnovers_man = stats["turnovers_man"]
    total_3pt_att_man = stats["ThreeFG_att_man"]
    total_3pt_makes_man = stats["ThreeFG_makes_man"]

    ts_percentage_zone = (total_points_zone / (2 * (total_FG_att_zone + 0.44 * total_FT_att_zone))
                          if (total_FG_att_zone + 0.44 * total_FT_att_zone) > 0 else 0)
    efg_percentage_zone = ((total_FG_makes_zone + 0.5 * total_3pt_makes_zone) / total_FG_att_zone
                           if total_FG_att_zone > 0 else 0)

    ts_percentage_man = (total_points_man / (2 * (total_FG_att_man + 0.44 * total_FT_att_man))
                         if (total_FG_att_man + 0.44 * total_FT_att_man) > 0 else 0)
    efg_percentage_man = ((total_FG_makes_man + 0.5 * total_3pt_makes_man) / total_FG_att_man
                          if total_FG_att_man > 0 else 0)

    # Generates the report
    report = (
        f"--- Zone Defense ---\n"
        f"Total Points: {total_points_zone}\n"
        f"Total Possessions: {int(stats['possessions_zone'])}\n"
        f"True Shooting Percentage: {ts_percentage_zone:.2%}\n"
        f"Effective Field Goal Percentage: {efg_percentage_zone:.2%}\n"
        f"Turnovers: {total_turnovers_zone}\n"
        f"--- Man Defense ---\n"
        f"Total Points: {total_points_man}\n"
        f"Total Possessions: {int(stats['possessions_man'])}\n"
        f"True Shooting Percentage: {ts_percentage_man:.2%}\n"
        f"Effective Field Goal Percentage: {efg_percentage_man:.2%}\n"
        f"Turnover: {total_turnovers_man}\n"
    )

    stats_display.set(report)

    # Saves stats
    save_stats_to_csv(ts_percentage_zone, efg_percentage_zone, ts_percentage_man, efg_percentage_man)

get_user_name()
root.mainloop()
