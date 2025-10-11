"""
Football Manager 2017 - Player Attributes Analysis
Explanatory analysis of player attributes including distributions and correlations
"""

import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse

# Add db-setup directory to path to import database_abc
script_dir = Path(__file__).parent
db_setup_dir = script_dir.parent / "db-setup"
sys.path.insert(0, str(db_setup_dir))

from database_abc import create_database_connection  # type: ignore


def load_player_data(db_path: Path) -> pd.DataFrame:
    """
    Load player data from database
    
    Args:
        db_path: Path to SQLite database
        
    Returns:
        DataFrame with player attributes
    """
    # Create database connection using abstract interface
    db_conn = create_database_connection('sqlite', db_path=str(db_path))
    
    try:
        db_conn.connect()
        
        # Query for player attributes
        query = """
        SELECT
            name,
            age,
            acceleration,
            pace,
            passing,
            finishing,
            tackling,
            vision,
            strength,
            stamina,
            technique,
            dribbling
        FROM players
        """
        
        # Execute query and fetch results
        results = db_conn.execute_query(query)
        
        # Convert to DataFrame
        columns = [
            'name', 'age', 'acceleration', 'pace', 'passing', 
            'finishing', 'tackling', 'vision', 'strength', 
            'stamina', 'technique', 'dribbling'
        ]
        df = pd.DataFrame(results, columns=columns)
        
    finally:
        db_conn.disconnect()
    
    return df


def load_player_data_by_position(db_path: Path, position: str) -> pd.DataFrame:
    """
    Load player data for players who have a specific position code in the positions table.

    Args:
        db_path: Path to SQLite database
        position: position code (string or numeric) as stored in positions.position

    Returns:
        DataFrame with player attributes for players matching the position
    """
    db_conn = create_database_connection('sqlite', db_path=str(db_path))
    try:
        db_conn.connect()
        query = """
        SELECT p.name, p.age, p.acceleration, p.pace, p.passing, p.finishing,
               p.tackling, p.vision, p.strength, p.stamina, p.technique, p.dribbling
        FROM players p
        JOIN positions ps ON ps.player_id = p.player_id
        WHERE ps.position = ?
        """
        results = db_conn.execute_query(query, (str(position),))
        columns = [
            'name', 'age', 'acceleration', 'pace', 'passing',
            'finishing', 'tackling', 'vision', 'strength',
            'stamina', 'technique', 'dribbling'
        ]
        df = pd.DataFrame(results, columns=columns)
    finally:
        db_conn.disconnect()

    return df


def plot_attribute_distributions(df: pd.DataFrame, attributes: list):
    """Plot histograms for attribute distributions"""
    df[attributes].hist(bins=20, figsize=(14, 10), edgecolor="black")
    plt.suptitle("Distribution of Player Attributes (All Players)", fontsize=16)
    plt.tight_layout()
    plt.show()


def plot_correlation_heatmap(df: pd.DataFrame, attributes: list):
    """Plot correlation heatmap for attributes"""
    plt.figure(figsize=(10, 8))
    sns.heatmap(df[attributes].corr(), annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Attribute Correlation Heatmap (All Players)", fontsize=14)
    plt.show()


def main():
    """Main analysis function with optional per-position analysis"""
    parser = argparse.ArgumentParser(description='FM2017 attribute analysis')
    parser.add_argument('--position', help='Position code to filter by (e.g. 1, 2, etc.). If omitted, runs analysis on all players')
    parser.add_argument('--db-path', help='Path to database file (overrides default)')
    args = parser.parse_args()

    # Path to database (relative to this script) or overridden by --db-path
    if args.db_path:
        db_path = Path(args.db_path)
    else:
        db_path = script_dir.parent / "db-setup" / "fm.db"

    if not db_path.exists():
        print(f"ERROR: Database not found at {db_path}")
        print("Please run setup_database.py first to create the database.")
        return 1

    print("="*60)
    print("FM2017 Player Attributes Analysis")
    print("="*60)
    print(f"Database: {db_path}")
    print("="*60 + "\n")

    # Define attributes to analyze
    attributes = [
        "acceleration", "pace", "passing", "finishing", "tackling",
        "vision", "strength", "stamina", "technique", "dribbling"
    ]

    if args.position:
        print(f"Loading player data for position: {args.position} ...")
        df = load_player_data_by_position(db_path, args.position)
        print(f"✓ Loaded {len(df)} players for position {args.position}\n")
        if df.empty:
            print("No players found for this position. Exiting.")
            return 0
        print("Basic Statistics:")
        print(df[attributes].describe())
        print()
        print("Generating attribute distribution plots for position {0}...".format(args.position))
        plot_attribute_distributions(df, attributes)
        print("Generating correlation heatmap for position {0}...".format(args.position))
        plot_correlation_heatmap(df, attributes)
    else:
        print("Loading player data from database (all players)...")
        df = load_player_data(db_path)
        print(f"✓ Loaded {len(df)} players\n")
        print("Basic Statistics:")
        print(df[attributes].describe())
        print()
        print("Generating attribute distribution plots (all players)...")
        plot_attribute_distributions(df, attributes)
        print("Generating correlation heatmap (all players)...")
        plot_correlation_heatmap(df, attributes)

    print("\n Analysis complete!")
    return 0


if __name__ == "__main__":
    exit(main())

