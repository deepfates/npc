
def get_available_tools(self):
    """Get the list of tools available in the game."""
    tools = [
        Tool(
            name="Look",
            description="Check the description of the current room.",
            func=lambda x: format_scene(self.world.state)
        ),
        Tool(
            name="Inventory",
            description="Check your inventory",
            func=lambda x: self.world.state.inventory
        ),
        Tool(
            name="Score",
            description="Check your score",
            func=lambda x: f"{self.world.state.score}/{self.world.state.max_score}"
        ),
        # Tool(
        #     name="Play",
        #     description="Send a command to the game and receive feedback.",
        #     func=lambda x: format_scene(self.step_world(x))
        # ),
        Tool(
            name="Check notes",
            description="Send an empty string here to get your notes from last round.",
            func=lambda x: self.notes
        ),
        Tool(
            name="Think",
            description="Think about your goals and the world. Use this when you can't find a valid tool",
            func=lambda x: "What should I do?"
        )
    ]
    return tools