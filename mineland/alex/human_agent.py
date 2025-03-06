import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
from mineland import Action, LowLevelAction

class HumanGUI:
    def __init__(self, root, width=320, height=180):
        self.root = root
        self.width = width
        self.height = height

        # Main frame to hold the camera feed
        self.frame = tk.Frame(self.root)
        self.frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.canvas = tk.Canvas(self.frame, width=self.width, height=self.height)
        self.canvas.pack()

        # Chat history (read-only text area)
        self.chat_history = tk.Text(self.root, height=10, width=50)
        self.chat_history.pack(side=tk.TOP, padx=10, pady=5)

        # Chat input box
        self.chat_input = tk.Entry(self.root, width=50)
        self.chat_input.pack(side=tk.TOP, padx=10, pady=5)

        # Inventory display
        self.inventory_label = tk.Label(self.root, text="Inventory: []")
        self.inventory_label.pack(side=tk.TOP, padx=10, pady=5)

        # Buttons for movement / actions
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.BOTTOM, padx=10, pady=10)

        tk.Button(self.button_frame, text="Forward", command=self.move_forward).grid(row=0, column=1)
        tk.Button(self.button_frame, text="Left",    command=self.move_left).grid(row=1, column=0)
        tk.Button(self.button_frame, text="Right",   command=self.move_right).grid(row=1, column=2)
        tk.Button(self.button_frame, text="Back",    command=self.move_back).grid(row=2, column=1)
        tk.Button(self.button_frame, text="Jump",    command=self.jump).grid(row=1, column=1)
        tk.Button(self.button_frame, text="Attack",  command=self.attack).grid(row=3, column=1)
        tk.Button(self.button_frame, text="Use",     command=self.use).grid(row=4, column=1)

        # Store the action the user clicked on
        self.current_action = Action(LowLevelAction.NO_OP)

    def update_image(self, obs):
        """Update the camera feed in the Tkinter Canvas."""
        # obs.rgb is shape (3, H, W). Let's transpose to (H, W, 3) and convert to PIL Image
        rgb = np.transpose(obs.rgb, (1, 2, 0))  # shape(H, W, 3)
        image = Image.fromarray(rgb)
        image = image.resize((self.width, self.height))
        self.photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

    def update_inventory(self, inventory):
        """Display the inventory in a label."""
        self.inventory_label.config(text=f"Inventory: {inventory}")

    def update_chat(self, chat_messages):
        """Display the chat history."""
        self.chat_history.delete("1.0", tk.END)
        for msg in chat_messages:
            self.chat_history.insert(tk.END, msg + "\n")

    # --- Action button callbacks ---
    def move_forward(self):
        self.current_action = Action(LowLevelAction.MOVE_FORWARD)

    def move_back(self):
        self.current_action = Action(LowLevelAction.MOVE_BACK)

    def move_left(self):
        self.current_action = Action(LowLevelAction.MOVE_LEFT)

    def move_right(self):
        self.current_action = Action(LowLevelAction.MOVE_RIGHT)

    def jump(self):
        self.current_action = Action(LowLevelAction.JUMP)

    def attack(self):
        self.current_action = Action(LowLevelAction.ATTACK)

    def use(self):
        self.current_action = Action(LowLevelAction.USE)

    def get_action(self):
        """Return the current action, then reset to NO_OP."""
        action = self.current_action
        self.current_action = Action(LowLevelAction.NO_OP)
        return action


class HumanAgent:
    """A human-controlled agent with a Tkinter GUI."""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Human Minecraft Interface")
        self.gui = HumanGUI(self.root)

    def run(self, obs, code_info, done, task_info, verbose=False):
        """
        Called every time-step by the main loop:
          obs: observation dict
          code_info: debug info from environment
          done: whether the episode is done
          task_info: additional info about the current task
        """
        # 1. Update the GUI with the latest observation
        self.gui.update_image(obs)
        self.gui.update_inventory(obs["inventory"])
        self.gui.update_chat(obs["chat"])

        # 2. Let Tkinter process events (e.g. button clicks)
        self.root.update_idletasks()
        self.root.update()

        # 3. Return whichever action the user triggered
        action = self.gui.get_action()
        return action
