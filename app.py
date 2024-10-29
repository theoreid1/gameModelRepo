import random

import streamlit as st
from config import Config
from classes import Contract,Lootbox,Player,Dungeon,Game

# Function to create a Streamlit sidebar for user input
def user_input():
    st.sidebar.header("Game Configuration")

    # Add simulation settings
    with st.sidebar.expander("Simulation Settings", expanded=False):
        rounds_per_day = st.slider("Rounds Per Day", 1, 20, 10)
        simulation_days = st.slider("Number of Days", 1, 30, 10)

    # Input fields for Contract drop chances
    with st.sidebar.expander("Contract Drop Chances", expanded=False):
        contract_material_drop_epic = st.slider("Contract: Epic Material Drop Chance", 0.0, 1.0, 0.11)
        contract_material_drop_rare = st.slider("Contract: Rare Material Drop Chance", 0.0, 1.0, 0.89)

    # Input fields for Lootbox drop chances
    with st.sidebar.expander("Lootbox Drop Chances", expanded=False):
        lootbox_loot_drop_legendary = st.slider("Lootbox: Legendary Drop Chance", 0.0, 1.0, 0.02)
        lootbox_loot_drop_epic = st.slider("Lootbox: Epic Drop Chance", 0.0, 1.0, 0.09)
        lootbox_loot_drop_rare = st.slider("Lootbox: Rare Drop Chance", 0.0, 1.0, 0.15)
        lootbox_loot_drop_uncommon = st.slider("Lootbox: Uncommon Drop Chance", 0.0, 1.0, 0.74)
        lootbox_loot_drop_common = st.slider("Lootbox: Common Drop Chance", 0.0, 1.0, 0.0)
    # Base completion rates per tier
    with st.sidebar.expander("Base Completion Rates", expanded=False):
        base_completion_rates = {
            1: st.slider("Tier 1 Base Completion Rate", 0.0, 1.0, 0.8),
            2: st.slider("Tier 2 Base Completion Rate", 0.0, 1.0, 0.6),
            3: st.slider("Tier 3 Base Completion Rate", 0.0, 1.0, 0.3)
        }
        
    # Gear bonus values in separate dropdown
    with st.sidebar.expander("Gear Bonus Values", expanded=False):
        gear_bonus_values = {
            'legendary': st.slider("Legendary Gear Bonus", 0.0, 0.25, 0.05),
            'epic': st.slider("Epic Gear Bonus", 0.0, 0.20, 0.03),
            'rare': st.slider("Rare Gear Bonus", 0.0, 0.15, 0.02),
            'uncommon': st.slider("Uncommon Gear Bonus", 0.0, 0.10, 0.01)
        }

    # Input fields for Dungeon drop chances
    st.sidebar.subheader("Dungeon Drop Chances")
    
    # Dungeon Material Drop Chances per Tier
    dungeon_material_drop_chances = {}
    for tier in [1, 2, 3]:
        with st.sidebar.expander(f"Tier {tier} Material Drop Chances", expanded=False):
            dungeon_material_drop_chances[tier] = {
                'legendary': st.slider(f"T{tier} Material: Legendary", 0.0, 1.0, 0.02),
                'epic': st.slider(f"T{tier} Material: Epic", 0.0, 1.0, 0.09),
                'rare': st.slider(f"T{tier} Material: Rare", 0.0, 1.0, 0.15),
                'uncommon': st.slider(f"T{tier} Material: Uncommon", 0.0, 1.0, 0.74),
                'common': st.slider(f"T{tier} Material: Common", 0.0, 1.0, 0.0)
            }

    # Dungeon Loot Drop Chances per Tier
    dungeon_loot_drop_chances = {}
    for tier in [1, 2, 3]:
        with st.sidebar.expander(f"Tier {tier} Loot Drop Chances", expanded=False):
            dungeon_loot_drop_chances[tier] = {
                'legendary': st.slider(f"T{tier} Loot: Legendary", 0.0, 1.0, 0.02),
                'epic': st.slider(f"T{tier} Loot: Epic", 0.0, 1.0, 0.09),
                'rare': st.slider(f"T{tier} Loot: Rare", 0.0, 1.0, 0.15),
                'uncommon': st.slider(f"T{tier} Loot: Uncommon", 0.0, 1.0, 0.74),
                'common': st.slider(f"T{tier} Loot: Common", 0.0, 1.0, 0.0)
            }

    
    return {
        'simulation_settings': {
            'rounds_per_day': rounds_per_day,
            'simulation_days': simulation_days
        },
        'contract_material_drop_chances': {
            'epic': contract_material_drop_epic,
            'rare': contract_material_drop_rare
        },
        'lootbox_loot_drop_chances': {
            'legendary': lootbox_loot_drop_legendary,
            'epic': lootbox_loot_drop_epic,
            'rare': lootbox_loot_drop_rare,
            'uncommon': lootbox_loot_drop_uncommon,
            'common': lootbox_loot_drop_common
        },
        'dungeon_material_drop_chances': dungeon_material_drop_chances,
        'dungeon_loot_drop_chances': dungeon_loot_drop_chances,
        'gear_bonus_values': gear_bonus_values,
        'dungeon_win_probabilities': base_completion_rates
    }

def main():
    st.title("Dungeon Game Simulator")

    # Get user input
    user_config = user_input()
    
    # Create Config object with user-defined parameters
    config = Config()
    config.contract_material_drop_chances = user_config['contract_material_drop_chances']
    config.lootbox_loot_drop_chances = user_config['lootbox_loot_drop_chances']
    config.dungeon_material_drop_chances = user_config['dungeon_material_drop_chances']
    config.dungeon_loot_drop_chances = user_config['dungeon_loot_drop_chances']
    config.gear_bonus_values = user_config['gear_bonus_values']
    config.dungeon_win_probabilities = user_config['dungeon_win_probabilities']

    players = [Player("Alice", config), Player("Bob", config)]
    game = Game(players, config, rounds_per_day=user_config['simulation_settings']['rounds_per_day'])

    if st.button("Run Simulation"):
        game.run(days=user_config['simulation_settings']['simulation_days'])
        game.display_stats()
        game.plot_stats()

if __name__ == "__main__":
    main()